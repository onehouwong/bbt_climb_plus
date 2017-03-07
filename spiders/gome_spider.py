# -*- coding: utf-8 -*-
import scrapy
from bbt_climb_plus.items import GomeItem
# 国美商品由于翻页时是用JavaScript动态生成，所以只能爬取一页的内容


class GomeSpider(scrapy.Spider):
    name = "gome"
    start_urls = []
    allowed_domains = ["search.gome.com.cn"]

    def start_requests(self):
        key = raw_input("Enter the keyword you want:")
        page = input("Enter the number of pages you want:")
        url_head = "http://search.gome.com.cn/search?question=%s"
        self.start_urls.append(url_head % key)
        # question=后接关键词
        '''
        if page == 1:
            self.start_urls.append(url_head % (key, page))
        elif page > 1:
            for i in range(page):
                self.start_urls.append(url_head % (key, i+1))
        elif page <= 0:
            page = input("Invalid input, please enter a positive page number:")
            while page <= 0:
                page = input("Invalid input, please enter a positive page number:")
        '''
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True)

    def parse(self, response):

        sel = scrapy.Selector(response)
        sites = sel.xpath('//li[@class="product-item"]')  # 截取每个商品的信息
        '''
        for site in sites:
            print site.extract()
        '''

        def set_title(content):
            title_temp = content.xpath('div[@class="item-tab-warp"]/p[@class="item-pic"]/a/img/@alt').extract()
            item['title'] = ''.join(title_temp[0])

        def set_link(content):
            link_temp = content.xpath('div[@class="item-tab-warp"]/p[@class="item-pic"]/a/@href').extract()
            item['link'] = link_temp[0]

        def set_price(content):
            price_temp = content.xpath('div[@class="item-tab-warp"]/div/span/text()').extract()
            item['price'] = price_temp[0][1:]  # 去除￥符号

        def set_image(content):
            image_temp = content.xpath('div[@class="item-tab-warp"]/p[@class="item-pic"]/a/img/@gome-src').extract()
            item['image'] = image_temp[0]

        def set_comment(content):
            comment_temp = content.xpath('div[@class="item-tab-warp"]/p[@class="item-comment-dispatching"]/'
                                         'a/text()').extract()
            item['comment'] = comment_temp[0]

        def set_keyword(content):
            # item['keyword'] = self.key()
            pass

        for site in sites:
            item = GomeItem()
            set_title(site)
            set_link(site)
            set_price(site)
            set_image(site)
            set_comment(site)
            print item['title']
            print item['link']
            print item['price']
            print item['image']
            print item['comment']
            yield item
