# -*- coding: utf-8 -*-
import scrapy
from bbt_climb_plus.items import JingdongRecommendItem
# 本爬虫用于爬取京东推荐页面的商品内容


class Jingdong_recomendSpider(scrapy.Spider):
    name = "jingdong_rec"
    allowed_domains = ["tuijian.jd.com"]

    def start_requests(self):
        url = 'http://tuijian.jd.com'
        yield scrapy.Request(url, dont_filter=True)

    def parse(self, response):

        sel = scrapy.Selector(response)
        sites = sel.xpath('//div[@class="seckill"]/div/div/ul/li[re:test(@class, "item fore\d")]')
        # 截取每个商品的信息

        '''
        for site in sites:
            print site.extract()
        '''

        def set_title(content):
            title_temp = content.xpath('div[@class="p-name"]/a/@title').extract()
            item['title'] = ''.join(title_temp[0])

        def set_idcode(content):
            idcode_temp = content.xpath('div[@class="p-price"]/span/@data-price-id').extract()
            item['idcode'] = idcode_temp[0]

        def set_link(content):
            link_temp = content.xpath('div[@class="p-name"]/a/@href').extract()
            item['link'] = link_temp[0]


        def set_image(content):
            image_temp = content.xpath('div[@class="p-img"]/a/img/@src').extract()
            item['image'] = image_temp[0]

        def set_keyword(content):
            # item['keyword'] = self.key()
            pass

        for site in sites:
            item = JingdongRecommendItem()
            set_title(site)
            set_idcode(site)
            set_link(site)
            set_image(site)
            print item['title']
            print item['idcode']
            print item['link']
            print item['image']
            print
            yield item
