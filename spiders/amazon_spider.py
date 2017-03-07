# -*- coding: utf-8 -*-
import scrapy
from bbt_climb_plus.items import AmazonItem


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    start_urls = []
    allowed_domains = ["amazon.cn"]

    def start_requests(self):
        key = raw_input("Enter the keyword you want:")
        page = input("Enter the number of pages you want:")
        url_head = "http://www.amazon.cn/s/ref=sr_pg_2?rh=i%%3Aaps%%2Ck%%3Akindle&page=%d&keywords=%s&ie=UTF8&qid=1459266578"
        # 注意百分号
        # keywords=后接关键词 page=后接页码数
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
        sites = sel.xpath('//div[@class="s-item-container"]')
        '''
        for site in sites:
            print site.extract()
        '''
        def set_title(content):
            title_temp = content.xpath('div/div/a[@class="a-link-normal s-access-detail-page  a-text-normal"]/@title').extract()[0]
            # 检测Kindle电子书 这一多余选项并删除
            if title_temp == u"Kindle电子书":
                return
            else:
                item['title'] = title_temp

        def set_links(content):
            link_temp = content.xpath('div/div/div/a[@class="a-link-normal a-text-normal"]/@href').extract()[0]
            '''去除以/s?开头的多余项，并去除相邻的多余项
            for i in range(link_temp.__len__()):
                if not link_temp[i].startswith('/s?'):
                    if not link_temp[i].__eq__(link_temp[i-1 if i > 0 else 0]):
                        links.append(link_temp[i])'''
            item['link'] = link_temp

        def set_price(content):
            price_temp = content.xpath('div/div/a/span[@class="a-size-base a-color-price s-price a-text-bold"]/text()'
                                       '|div/a/span[@class="a-size-base a-color-price s-price a-text-bold"]/text()'
                                       '|div/div/a/span[@class="a-size-base a-color-price a-text-bold"]/text()').extract()
            # 对于一些暂时无货的商品 并不会有价格 用个-1的值做标记 以便后面处理item的时候丢弃
            if price_temp == []:
                price_temp = "-1"
                item['price'] = price_temp
            else:
                item['price'] = price_temp[0][1:].replace(',', '')

        def set_image(content):
            image_temp = content.xpath('div/div/div/a/img[@class="s-access-image cfMarker"]/@src').extract()[0]
            item['image'] = image_temp

        for site in sites:
            item = AmazonItem()
            set_title(site)
            set_links(site)
            set_price(site)
            set_image(site)
            if item['price'] != '-1':
                print item['title']
                print item['link']
                print item['price']
                print item['image']
                print
                yield item
