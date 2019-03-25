import codecs
import json

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        # item传递到pipline后，可以进行很多操作，比如保存到数据库，drop该item，主要做数据存储
        return item


# 将数据保存到json的pipeline
class JsonWithEncodingPipeline(object):
    def __init__(self):
        # 利用codecs方式打开文件,与open函数不同在于编码,可以省去很多编码方面的繁杂工作
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    # 保存到json文件，首先就要打开json文件，可以在初始化的时候就打开文件，先将需要写入的文件打开
    # 用到python开发包codecs，与普通打开文件包open最大的区别在于文件的编码

    def process_item(self, item, spider):
        # 利用json.dumps函数将item存储成json
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 写入json文件中 ensure_ascii设为False，不然写入中文是会报错的，会直接把unicode编码写入文章中
        self.file.write(lines)
        # process_item函数一定要返回item, 因为下一个pipeline还会使用此item
        return item

    # 在spider close的时候关闭file
    def spider_closed(self, spider):
        self.file.close()


# 调用scrapy提供的json exporter导出json文件
class JsonExporterPipeline(object):
    # 一个关键的地方，在init时，可以直接使用open方法，并且需要传递exporter
    def __init__(self):
        self.file = open('articleexporter.json', 'wb')  # 二进制方式打开
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# 将item存入数据库
class MysqlPipeline(object):
    # 首先连接数据库,执行数据库具体操作是由cursor来完成的
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.do_insert, item)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


# 上述方法(execute和commit操作是同步操作)在后期爬取加解析会快于数据存储到MySQL,会导致阻塞
# 使用twisted框架提供的API可以完成数据的异步写入

# 异步MySQL插入
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # 关键方法，通过classmethod来定义，在定义自己的主键和扩展的时候很有用
    # 这个方法会被scrapy调用，会将setting传递进来，方法名称是固定的
    # cls指的就是MysqlTwistedPipeline这个类
    @classmethod
    def from_settings(cls, settings):
        # dict可变参数
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DB_NAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )

        # 实际上提供的是一个异步容器，有个库去连接MySQL
        # 本身还是使用了mysqldb去连接数据库，twisted只是提供了一个异步容器
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        # 第一个参数dbapiName实际就是mysqldb的模块名,第二个参数即为各种配置，注意这里采用可变化参数dict的传入方式，必须要使里面的变量名和默认的一样
        return cls(dbpool)

    # 接下来直接调用dbpool连接池来做数据插入
    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步操作
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 第一个参数是自己定义的函数，即具体的需要异步操作的动作,item是传入的参数
        # 有时候执行异步操作会有错误，可以直接处理错误，有专门的处理函数,通过返回来的对象的addErrorback()方法，第一个参数仍然是可自定义的错误处理函数
        query.addErrback(self.handle_error)  # 处理异常

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """
                           insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,front_image_path,comment_nums,fav_nums,praise_nums,tags,content)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                       """
        cursor.execute(insert_sql, (
            item["title"], item["create_date"], item["url"], item["url_object_id"], item["front_image_url"],
            item["front_image_path"], item["comment_nums"], item["fav_nums"], item["praise_nums"], item["tags"],
            item["content"]))
        # 不需要commit,会自动进行commit


# scrapy中的imagepipline只有下载图片的功能，但是我们想将图片在本地保存的地址绑定在一起，并且传到item中
# 定制自己的pipeline，去继承setting中配置的 imagepipeline，让里面的某些功能变得可以定制
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            # 文件最后下载完成的保存路径是存放在results里面的，通过断点调试可以查看这个results是个list，其中每个元素是一个tuple，存放了状态等信息
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path
        return item
