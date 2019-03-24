import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()  # scrapy可以使用Field表示任意类型
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()  # 对url进行编码
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()
