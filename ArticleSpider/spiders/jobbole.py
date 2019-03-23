# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1.获取文章列表页中的文章 url 并交给 scrapy 下载后并进行解析
        2.获取下一页 url 并交给 scrapy 进行下载，下载完成后交给parse
        """

        # 解析列表页的所有文章 url 并交给 scrapy 下载后进行解析
        # 利用::attr()伪类选择器获得对应元素的属性值
        post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()
        for post_url in post_urls:
            # 利用Request方法提交请求获取对应url内容
            # url表示访问的url(parse.urljoin是借助urllib将当前url与请求url进行拼接,从而获取到真实的url),callback表示回调的函数
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

        # 提交下一页并交给scrapy进行下载
        # 两个类之间有空格则表示子元素,两个类中间没空格则表示同时满足两个类的元素
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    # 提取文章的具体字段
    def parse_detail(self, response):
        title = response.css(".entry-header h1::text").extract()[0]
        print(title)
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "").strip()
        # 点赞数
        praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        # 收藏数
        fav_nums = response.css('span.bookmark-btn::text').extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        else:
            fav_nums = 0

        # 评论数
        comment_nums = response.css('a[href="#article-comment"] span::text').extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)
        else:
            comment_nums = 0

        # 获得文章内容
        content = response.css("div.entry").extract()[0]
        # 获得标签
        tags = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag = [element for element in tags if not element.strip().endswith("评论")]
        tags = ",".join(tag)
