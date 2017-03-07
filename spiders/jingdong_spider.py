#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib2

import scrapy

from bbt_climb_plus.items import JingdongItem


class JingdongSpider(scrapy.Spider):
    name = "jingdong"
    start_urls = []
    allowed_domains = ["jd.com"]

    '''
    def __init__(self, *args, **kwargs):
        super(JingdongSpider, self).__init__(*args, **kwargs)
        self.key = args[0]
    '''
    def start_requests(self):
        key = raw_input("Enter the keyword you want:")
        # key = self.key
        # page = input("Enter the number of pages you want:")
        page = 1
        url_head = "http://search.jd.com/Search?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=%d&click=0"
        if page == 1:
            self.start_urls.append(url_head % (key, page))
        elif page > 1:
            for i in range(page):
                self.start_urls.append(url_head % (key, i + 1))
        elif page <= 0:
            page = input("Invalid input, please enter a positive page number:")
            while page <= 0:
                page = input("Invalid input, please enter a positive page number:")

        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        # 设置公司名
        def set_company(item_content):
            item['company'] = ''

        # 设置关键字
        '''
        def set_keyword(item_content):
            item['keyword'] = self.key
        '''

            # 获取标题
        def set_title(item_content):
            title_temp = item_content.xpath(
                'div/div/div/div[@class="p-name p-name-type-2"]/a/@title|div[@class="p-name p-name-type-2"]/a/@title|div[@class="p-name"]/a/em/font/text()|div[@class="p-name"]/a/em/text()').extract()
            # p-name p-name-type-2是一种类型（iphone的页面），后两种以另一种类型（python书籍的页面）
            item['title'] = ''.join(title_temp)  # title_temp是一个list，把它连接成string。

        def set_idcode(item_content):
            pattern = re.compile(r'(\d)+')
            item['idcode'] = pattern.search(item['link']).group()

        # 设置价格
        def set_price(item_content):
            price_temp = item_content.xpath('div[@class="p-price"]/strong/i/text()').extract()
            if price_temp != []:
                item['price'] = price_temp[0]
            elif self.get_price(item['idcode']):
                item['price'] = self.get_price(item['idcode'])[0]
            else:
                item['price'] = '-1'


        def set_link(item_content):
            item['link'] = item_content.xpath(
                'div[@class="p-name p-name-type-2"]/a/@href|div[@class="p-name"]/a/@href|div/div/div/div[@class="p-name p-name-type-2"]/a/@href').extract()[
                               0][2:]

        def set_image(item_content):
            # 获取图片链接
            item['image'] = \
                item_content.xpath(
                    "div[@class='p-img']/a/img/@src | div[@class='p-img']/a/img/@data-lazy-img").extract()[
                    0][2:]

        # 判断一个商品是否有套装（单件/两件套/三件套）
        def is_suit():
            temp = one_item_content.xpath("div/div/span[@class='item selected']").extract()
            if temp:
                return True
            else:
                return False

        # 设置套装的标题
        def set_suit_title(number):
            title_temp = one_item_content.xpath(
                'div[@class="p-name p-name-type-2"][' + number + ']/a/@title').extract()

        # 处理拥有多个套装的商品。。
        def handle_each(item_content):
            number = 1
            item_content = item_content.xpath("div/div/div[@class='tab-content-item tab-cnt-i-selected']")
            set_title(item_content)
            set_link(item_content)
            set_idcode(item_content)
            set_price(item_content)
            set_image(item_content)
            #set_keyword(item_content)

            item_content = item_content.xpath('div[@class="tab-content-item"][' + str(number) + ']')
            while item_content:
                set_title(item_content)
                set_link(item_content)
                set_idcode(item_content)
                set_price(item_content)
                set_image(item_content)
                #set_keyword(item_content)
                number = number + 1
                item_content = item_content.xpath('div[@class="tab-content-item"][' + str(number) + ']')

        sel = scrapy.Selector(response)
        #     items = []
        #      titles = sel.xpath('//div[@class="p-name p-name-type-2"]/a/@title').extract()
        #      links = sel.xpath('//div[@class="p-name p-name-type-2"]/a/@href').extract()
        # prices = sel.xpath('//div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/i/text()').extract()

        # images = []
        sites = sel.xpath('//div[@class="gl-i-wrap"]')  # 由于不同商品有多个图片 因此需要独立处理

        for one_item_content in sel.xpath('//div[@class="gl-i-wrap"]'):
            # print '********************************************************************'
            # # item_source=sel.xpath('//div[@class="gl-i-wrap"]')
            item = JingdongItem()

            # 判断该商品是否有套装
            if is_suit():
                handle_each(one_item_content)  # 对每一种套装进行处理
            else:
                set_title(one_item_content)
                set_link(one_item_content)
                set_idcode(one_item_content)
                set_price(one_item_content)
                set_image(one_item_content)
                #set_keyword(one_item_content)
                if item['price'] != '-1':
                    yield item


                # for count in range(sites.__len__()):
                #     pattern = re.compile(r'data-lazy-img="//\S*.jpg"')  # \S	匹配任何非空白字符。等价于[^ \f\n\r\t\v]。
                #     images_for_all = pattern.findall(sites[count].extract())
                #     for i in range(images_for_all.__len__()):  # 格式化处字符串
                #         images_for_all[i] = images_for_all[i][15:-1]
                #     images.append(images_for_all)

                # for n in range(titles.__len__()):
                #     item = JingdongItem()
                #     item['title'] = titles[n]
                #     item['link'] = links[n]
                #
                #     # 获取商品id码
                #     pattern = re.compile(r'(\d)+')
                #     match = pattern.search(links[n])
                #     if match:
                #         id = match.group()
                #     item['id'] = id
                #
                #     # 获取商品的价格
                #     # if exist_price():#京东搜索页有的产品会没有价格，如果有价格则直接抓获，没有的要另寻他法
                #     #     pass
                #     # else:
                #     #    set_price(id,get_price(id,item),item)
                #
                #     # item['image'] = images[n]
                #     items.append(item)
                #     yield item

    def get_price(self, id):
        price_link = 'http://p.3.cn/prices/get?skuid=J_' + id
        pattern = re.compile(r'\d+\.\d{2}')  # 获取价格的正则表达式
        response = urllib2.urlopen(price_link)
        html = response.read()
        result = pattern.search(html)
        if result:
            return result.group()
