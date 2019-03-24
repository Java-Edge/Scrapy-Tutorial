# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse

# 引入item
from ArticleSpider.items import JobBoleArticleItem

from ArticleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']  # 放入想爬取的所有url

    def parse(self, response):

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
        # 获得meta中的front_image_url,文章封面图
        front_image_url = response.meta.get("front_image_url", "")
        # 获得title
        title = response.css(".entry-header h1::text").extract()[0]
        print(title)
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "").strip()
        # 点赞数
        praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        # 收藏数
        collect = response.css('span.bookmark-btn::text').extract()[0]
        match_re = re.match(".*?(\d+).*", collect)
        if match_re:
            collect = match_re.group(1)
        else:
            collect = 0
        # 评论数
        comment = response.css('a[href="#article-comment"] span::text').extract()[0]
        match_re = re.match(".*?(\d+).*", comment)
        if match_re:
            comment = match_re.group(1)
        else:
            comment = 0
        # 获得文章内容
        content = response.css("div.entry").extract()[0]
        # 获得标签
        tags = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag = [element for element in tags if not element.strip().endswith("评论")]
        tags = ",".join(tag)

        # 填充item
        article_item["url_object_id"] = get_md5(response.url)
        article_item['title'] = title
        article_item['url'] = response.url
        article_item['create_date'] = create_date
        article_item['front_image_url'] = [front_image_url]
        article_item['praise_nums'] = praise_nums
        article_item['comment_nums'] = comment
        article_item['fav_nums'] = collect
        article_item['tags'] = tags
        article_item['content'] = content

        yield article_item  # 将item传递到pipeline中
