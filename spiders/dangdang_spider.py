# -*- coding: utf-8 -*-
import scrapy
from bbt_climb_plus.items import DangdangItem


class DangdangSpider(scrapy.Spider):
    name = "dangdang"
    start_urls = []
    allowed_domains = ["search.dangdang.com"]

    def start_requests(self):
        key = raw_input("Enter the keyword you want:")
        page = input("Enter the number of pages you want:")
        url_head = "http://search.dangdang.com/?key=%s&act=input&page_index=%d"
        # key=后接关键词 page_index=后接页码数
        if page == 1:
            self.start_urls.append(url_head % (key, page))
        elif page > 1:
            for i in range(page):
                self.start_urls.append(url_head % (key, i+1))
        elif page <= 0:
            page = input("Invalid input, please enter a positive page number:")
            while page <= 0:
                page = input("Invalid input, please enter a positive page number:")

        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True)

    def parse(self, response):

        sel = scrapy.Selector(response)
        sites = sel.xpath('//li[re:test(@class, "line\d")]')  # 截取每个商品的信息，从line1一直到line60...
        '''
        for site in sites:
            print site.extract()
        '''

        def set_title(content):
            title_temp = content.xpath('a/@title').extract()
            item['title'] = ''.join(title_temp[0]).strip()  # 去除空格

        def set_idcode(content):
            id_temp = content.xpath('@id').extract()
            item['idcode'] = id_temp[0]

        def set_link(content):
            link_temp = content.xpath('a/@href').extract()
            item['link'] = link_temp[0]

        def set_price(content):
            price_temp = content.xpath('p[@class="price"]/span/text()|'
                                       'div/p[@class="price"]/span/text()').extract()
            item['price'] = price_temp[0][1:]  # 去除￥符号

        def set_image(content):
            image_temp = content.xpath('a/img/@src|a/img/@data-original').extract()
            item['image'] = image_temp[0]

        def set_comment(content):
            comment_temp = content.xpath('p[@class="star"]/a/text()|'
                                         'p[@class="search_star_line"]/a/text()').extract()
            item['comment'] = comment_temp[0][:-3]  # 去掉“条评论”

        def set_keyword(content):
            # item['keyword'] = self.key()
            pass

        for site in sites:
            item = DangdangItem()
            set_title(site)
            set_idcode(site)
            set_link(site)
            set_price(site)
            set_image(site)
            set_comment(site)
            print item['title']
            print item['idcode']
            print item['link']
            print item['price']
            print item['image']
            print item['comment']
            print
