# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/114610']

    def parse(self, response):
        re_selector = response.xpath('//div[@class="entry-header"]/h1/text()')

        # 文章title
        title = response.xpath('//*[@id="post-114610"]/div[1]/h1/text()')

        # 文章创建时间
        create_date = response.xpath('//*[@id="post-114610"]/div[2]/p/text()').extract()[0].strip().replace("·",
                                                                                                            "").strip()
        # 通过contains函数选择class中包含vote-post-up的元素，获得点赞数
        praise = response.xpath('//*[contains(@class,"vote-post-up")]/h10/text()').extract()[0]

        # 收藏数
        import re
        match_re = re.match('.*?(\d+).*', ' 收藏')
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        # 正则表达式注意要有？表示非贪婪匹配，可以获取两位数等
        # 还有一点就是老师没有考虑的，如果没有收藏数，即匹配不到数字，说明收藏数为0.

        # 评论数
        comment = response.xpath('//a[@href="#article-comment"]/span/text()').extract()[0]
        match_re = re.match(".*?(\d+).*", comment)
        if match_re:
            comment = match_re.group(1)
        else:
            comment = 0

        # 文章内容
        content = response.xpath('//div[@class="entry"]').extract()[0]

        # 文章标签
        tag_list = response.xpath('//*[@id="post-114610"]/div[2]/p/a/text()').extract()
        # 利用列表生成式过滤携带评论的文章标签
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # 利用join方式将列表拼成一个字符串
        tags = ",".join(tag_list)
        response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]

        pass
