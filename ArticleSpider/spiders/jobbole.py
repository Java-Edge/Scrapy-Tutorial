import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
# 引入md5处理url
from ArticleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1.获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2.获取下一页url并交给scrapy进行下载，下载完成后交给parse
        """
        # 解析列表页的所有文章url并交给scrapy下载后进行解析
        # 利用::attr()伪类选择器获得对应元素的属性值
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")  # 获得图片的src
            post_url = post_node.css("::attr(href)").extract_first("")  # 获得连接的href
            # 利用Request方法提交请求获取对应url内容
            # url表示访问的url(parse.urljoin是借助urllib将当前url与请求url进行拼接,从而获取到真实的url),callback表示回调的函数
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)

        # 提交下一页并交给scrapy进行下载
        # 两个类之间有空格则表示子元素,两个类中间没空格则表示同时满足两个类的元素
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    # 提取文章的具体字段
    def parse_detail(self, response):
        # 实例化item
        article_item = JobBoleArticleItem()

        # jobbole.py 解析字段，使用选择器
        # 首先需要实例化一个ItemLoader类的对象
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)  # 实例化一个对象

        """有三种重要的方法
        item_loader.add_css() # 通过css选择器选择的
        item_loader.add_xpath()
        item_loader.add_value()  # 不是选择器选择的，而是直接填充
        """

        # 通过item loader加载item
        # 获得meta中的front_image_url,文章封面图
        front_image_url = response.meta.get("front_image_url", "")
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("content", "div.entry")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")

        # 获取article_item
        article_item = item_loader.load_item()

        """
        调用默认的load_item()方法有两个问题，第一个问题会将所有的值变成一个list，虽然听起来不合理，但是从另外的角度来看，也是合理的
        因为通过css选择器取出来的极有可能就是一个list，不管是取第0个还是第1个，都是一个list，所以默认情况就是list
        如何解决问题呢，list里面只取第一个，以及对某个字段的list加一些额外的处理过程
        在item.py对字段进行定义，scrapy.Field()里面是有参数的,input_processor表示对输入的值预处理过程，后面MapCompose()类中可以传递很多函数名的参数，表示从左到右依次处理
        title = scrapy.Field(
            input_processor = MapCompose(add_jobbole)
        )
        """

        yield article_item  # 将item传递到pipeline中
