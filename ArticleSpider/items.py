import datetime
import scrapy
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader


class ArticlespiderItem(scrapy.Item):
    pass


# 处理的函数,value表示input的值,即初始值
def add_jobbole(value):
    return value + "-jobbole"


# 处理时间函数
def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


# 获得字符串中数字
def get_nums(value):
    # 对收藏数和评论数的正则处理
    match_re = re.match('.*?(\d+).*', value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


# 去掉含有评论的tag
def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


# 什么都不做的函数,用于覆盖default_output_processor
def return_value(value):
    return value


# 很多item的字段都是取list的第一个，是否需要在每个Field中都添加output_processor呢
# 可以通过自定义itemloader来解决,通过重载这个类，设置默认的输出处理设置，就可以统一处理了
class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),  # Mapcompose表示可以对传入的内容调用多个函数进行预处理
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()  # 对url进行编码
    front_image_url = scrapy.Field(
        # 不会修改image的值,且覆盖default_output_processor
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,front_image_path,comment_nums,fav_nums,praise_nums,tags,content)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params = (self["title"], self["url"], self["create_date"], self["fav_nums"],
                  self["front_image_url"], self["front_image_path"], self["praise_nums"], self["comment_nums"],
                  self["tags"], self["content"])
        return insert_sql, params
