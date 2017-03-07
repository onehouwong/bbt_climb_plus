# -*- coding: utf-8 -*-
import scrapy
from bbt_climb_plus.items import DangdangRecommendItem


class DangdangRecommendSpider(scrapy.Spider):
    name = "dangdang_rec"
    start_urls = []
    allowed_domains = ["dangdang.com"]

    def start_requests(self):
        url = 'http://z.dangdang.com/index'
        yield scrapy.Request(url, dont_filter=True)

    def parse(self, response):

        sel = scrapy.Selector(response)
        sites = sel.xpath('//a[re:test(@href, "http://z.dangdang.com/zsubject_brand\s*")]')
        # 截取每个商品的信息
        '''
        for site in sites:
            print site.extract()
        '''
        def set_link(content):
            link_temp = content.xpath('@href').extract()
            item['link'] = link_temp[0]

        def set_price(content):
            price_temp = content.xpath('span/span/span[@class="z_money"]/text()').extract()
            item['price'] = str(price_temp[0]) + '元起'

        def set_image(content):
            image_temp = content.xpath('span/img/@data-original').extract()
            item['image'] = image_temp[0]

        def set_discount(content):
            discount_temp = content.xpath('span/span/span[@class="z_manjian"]/text()').extract()
            item['discount'] = discount_temp[0]

        def set_keyword(content):
            # item['keyword'] = self.key()
            pass

        for site in sites:
            item = DangdangRecommendItem()
            set_link(site)
            set_price(site)
            set_image(site)
            set_discount(site)
            print item['link']
            print item['price']
            print item['image']
            print item['discount']
            print
            yield item
