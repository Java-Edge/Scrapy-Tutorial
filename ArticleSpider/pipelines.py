# 处理获取下载到本地的图片的保存路径

import codecs
import json
import MySQLdb

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        # item传递到pipline后，可以进行很多操作，比如保存到数据库，drop该item，主要做数据存储
        return item


# 将数据保存到json的pipeline
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    # 保存到json文件，首先就要打开json文件，可以在初始化的时候就打开文件，先将需要写入的文件打开
    # 用到python开发包codecs，与普通打开文件包open最大的区别在于文件的编码

    def process_item(self, item, spider):
        # 完成item的写入，首先将item转化为字符串
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # ensure_ascii设为False，不然写入中文是会报错的，会直接把unicode编码写入文章中
        self.file.write(lines)
        return item

    # 内置的函数，spider关闭函数，同时将文件关闭
    def spider_closed(self, spider):
        self.file.close()


# 调用scrapy提供的json exporter导出json文件
class JsonExporterPipeline(object):
    # 一个关键的地方，在init时，可以直接使用open方法，并且需要传递exporter
    def __init__(self):
        self.file = open('articleexporter.json', 'wb')
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
        insert_sql = """
            insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,front_image_path,comment_nums,fav_nums,praise_nums,tags,content)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["url_object_id"], item["front_image_url"],item["front_image_path"], item["comment_nums"], item["fav_nums"], item["praise_nums"], item["tags"],item["content"]))
        self.conn.commit()

# 到了这一个pipeline，需要做的就是跟数据库或者文件打交道，比如将数据保存到mysql，mangodb，或者本地文件，或者发送到es上面去

# scrapy中的imagepipline只有下载图片的功能，但是我们想将图片在本地保存的地址绑定在一起，并且传到item中
# 定制自己的pipeline，去继承setting中配置的imagespipeline，让里面的某些功能变得可以定制
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        # 文件最后下载完成的保存路径是存放在results里面的，通过断点调试可以查看这个results是个list，其中每个元素是一个tuple，存放了状态等信息
        for ok, value in results:
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path
        return item
