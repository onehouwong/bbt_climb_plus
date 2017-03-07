# -*- coding: utf-8 -*-
import scrapy
from bbt_climb_plus.items import GomeRecommendItem


class GomeSpider(scrapy.Spider):
    name = "gome_rec"
    allowed_domains = ["gome.com.cn"]

    def start_requests(self):
        url = "http://www.gome.com.cn/"
        yield scrapy.Request(url, dont_filter=True)

    def parse(self, response):

        sel = scrapy.Selector(response)
        sites = sel.xpath('//div[@class="choice_right"]')
        '''
        for site in sites:
            print site.extract()
        '''
        for site in sites:
            links = site.xpath('a/@href').extract()
            images = site.xpath('a/img/@src').extract()
            for x in range(links.__len__()):
                item = GomeRecommendItem()
                item['link'] = links[x]
                item['image'] = images[x]
                print item['link']
                print item['image']
                print
                yield item
