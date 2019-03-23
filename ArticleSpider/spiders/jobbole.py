# -*- coding: utf-8 -*-
import scrapy
import re


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/114610/']  # 放入想爬取的所有url

    def parse(self, response):
        title = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "").strip()
        # 点赞数
        praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        # 收藏数
        collect = response.css('span.bookmark-btn::text').extract()[0]
        match_re = re.match(".*?(\d+).*", collect)
        if match_re:
            collect = match_re.group(1)
        # 评论数
        comment = response.css('a[href="#article-comment"] span::text').extract()[0]
        match_re = re.match(".*?(\d+).*", comment)
        if match_re:
            comment = match_re.group(1)
        # 获得文章内容
        content = response.css("div.entry").extract()[0]
        # 获得标签
        tags = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag = [element for element in tags if not element.strip().endswith("评论")]
        tags = ",".join(tag)
        pass
