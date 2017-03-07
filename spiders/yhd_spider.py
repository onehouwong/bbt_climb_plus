# -*- coding: utf-8 -*-
import scrapy
from bbt_climb_plus.items import YhdItem


class YhdSpider(scrapy.Spider):
    name = "yhd"
    start_urls = []
    allowed_domains = ["search.yhd.com"]

    def start_requests(self):
        key = raw_input("Enter the keyword you want:")
        page = input("Enter the number of pages you want:")
        url_head = "http://search.yhd.com/c0-0-0/b/a-s1-v4-p%d-price-d0-f0d-m1-rt0-pid-mid0-k%s/"
        # k后接关键词 p后接页数
        # 一号店搜索页的商品源代码跟爬下来的是不一样的

        if page == 1:
            self.start_urls.append(url_head % (page, key))
        elif page > 1:
            for i in range(page):
                self.start_urls.append(url_head % (i+1, key))
        elif page <= 0:
            page = input("Invalid input, please enter a positive page number:")
            while page <= 0:
                page = input("Invalid input, please enter a positive page number:")

        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True)

    def parse(self, response):

        sel = scrapy.Selector(response)
        sites = sel.xpath('//div[@class="itemBox"]')  # 截取每个商品的信息
        '''
        for site in sites:
            print site.extract()
            print
        '''

        def set_title(content):
            title_temp = content.xpath('p/a/@title').extract()
            item['title'] = ''.join(title_temp[0])

        def set_link(content):
            link_temp = content.xpath('p/a/@href').extract()
            item['link'] = link_temp[0]

        def set_idcode(content):
            idcode_temp = content.xpath('p/a/@pmid').extract()
            item['idcode'] = idcode_temp[0]

        def set_price(content):
            price_temp = content.xpath('p[@class="proPrice"]/em/@yhdprice').extract()
            item['price'] = price_temp[0]

        def set_image(content):
            image_temp = content.xpath('div[@class="proImg"]/a/img/@src|'
                                       'div[@class="proImg"]/a/img/@original').extract()
            item['image'] = image_temp[0]

        '''
        def set_comment(content):
            print content.extract()
            comment_temp = content.xpath('p[@class="proPrice"]/span[@class="comment"]/a/@experienceCount').extract()
            item['comment'] = comment_temp[0]
        '''
        def set_keyword(content):
            # item['keyword'] = self.key()
            pass

        for site in sites:
            item = YhdItem()
            set_title(site)
            set_idcode(site)
            set_link(site)
            set_price(site)
            set_image(site)
            # set_comment(site)
            print item['title']
            print item['idcode']
            print item['link']
            print item['price']
            print item['image']
            # print item['comment']
            print
            yield item
