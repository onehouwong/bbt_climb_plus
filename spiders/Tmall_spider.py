# -*- coding: utf-8 -*-
import scrapy
from bbt_climb_plus.items import TmallItem


class TmallSpider(scrapy.Spider):
    name = "tmall"
    start_urls = []
    allowed_domains = ["list.tmall.com"]

    def start_requests(self):
        key = raw_input("Enter the keyword you want:")
        page = input("Enter the number of pages you want:")
        url_head = "https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.Dvgaao&s=%d&q=%s&sort=s&style=g&from=.list.pc_1_searchbutton&tmhkmain=0&type=pc#J_Filter"

        # q=后接关键词 s=后接页码数*60（eg：0,60,120等）
        if page == 1:
            self.start_urls.append(url_head % ((page-1)*60, key))
        elif page > 1:
            for i in range(page):
                self.start_urls.append(url_head % (i*60, key))
        elif page <= 0:
            page = input("Invalid input, please enter a positive page number:")
            while page <= 0:
                page = input("Invalid input, please enter a positive page number:")

        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True)

    def parse(self, response):

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

        sel = scrapy.Selector(response)
        sites = sel.xpath('//div[@class="product item-1111 "]|//div[@class="product  "]')
        for site in sites:
            item = TmallItem()
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

