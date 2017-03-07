# -*- coding: utf-8 -*-
import scrapy
from bbt_climb_plus.items import SuningItem


class TmallSpider(scrapy.Spider):
    name = "suning"
    start_urls = []
    allowed_domains = ["search.suning.com"]

    def start_requests(self):
        key = raw_input("Enter the keyword you want:")
        page = input("Enter the number of pages you want:")
        url_head = "http://search.suning.com/%s/&iy=0&cp=%d"
        # /后接关键词 cp=后接页码数（0 1 2 ....）
        if page == 1:
            self.start_urls.append(url_head % (key, page-1))
        elif page > 1:
            for i in range(page):
                self.start_urls.append(url_head % (key, i))
        elif page <= 0:
            page = input("Invalid input, please enter a positive page number:")
            while page <= 0:
                page = input("Invalid input, please enter a positive page number:")

        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True)

    def parse(self, response):

        sel = scrapy.Selector(response)
        sites = sel.xpath('//div[@class="product item-1111 "]|//div[@class="product  "]')

        def set_link(item_content):
            item['link'] = item_content.xpath('div/div[@class="productImg-wrap"]/a/@href').extract()[0][2:]

        def set_idcode(item_content):
            item['idcode'] = item_content.xpath('@data-id').extract()[0]

        def set_price(item_content):
            item['price'] = item_content.xpath('div/p[@class="productPrice"]/em/@title').extract()[0]

        def set_title(item_content):
            temp = item_content.xpath('div/p[@class="productTitle"]/a/@title|'
                                      'div/div[@class="productTitle "]/a/@title|'
                                      'div/div[@class="productTitle productTitle-spu"]/a/@title').extract()
            # title后可以带空格也可以没空格的 这么坑的你见过没有
            item['title'] = ''.join(temp)

        def set_image(item_content):
            images = item_content.xpath('div/div[@class="productImg-wrap"]/a/img/@data-ks-lazyload|'
                                        'div/div[@class="productImg-wrap"]/a/img/@src').extract()[0][2:]
            item['image'] = images

        def set_sale(item_content):
            temp = item_content.xpath('div/p[@class="productStatus"]/span/em/text()').extract()
            item['sale'] = ''.join(temp)
            if item['sale'] == '':
                item['sale'] = '0笔'  # 对于预购商品 是找不到销量的 应设置为0笔


        for site in sites:
            item = SuningItem()
            set_idcode(site)
            set_title(site)
            set_link(site)
            set_price(site)
            set_image(site)
            set_sale(site)
            yield item

            # print item['idcode']
            # print item['title']
            # print item['link']
            # print item['price']
            # print item['sale']
            # print item['image']
            # print
