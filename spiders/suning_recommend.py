# -*- coding: utf-8 -*-
import scrapy
from bbt_climb_plus.items import SuningRecommendItem
import re
# 本爬虫用于爬取京东推荐页面的商品内容


class Suning_recomendSpider(scrapy.Spider):
    name = "suning_rec"
    allowed_domains = ["ju.suning.com"]

    def start_requests(self):
        url = 'http://ju.suning.com/pc/home.html'
        yield scrapy.Request(url, dont_filter=True)

    def parse(self, response):

        sel = scrapy.Selector(response)
        sites = sel.xpath('//script[@type="text/html"]')
        # 截取每个商品的信息
        '''
        for site in sites:
            print site.extract()
        '''
        site = sites[0]
        content_pattern = re.compile(u"<!-- 商品列表 \[\[-->.*?</ul>", re.S)
        contents = content_pattern.findall(site.extract())
        # contents.__delitem__(1)

        titles = []
        links = []
        images = []
        sale_time = []
        prices = []
        for content in contents:
            title_pattern = re.compile('title=".*"')
            title_all = title_pattern.findall(content)
            for title in title_all:
                titles.append(title)

            link_pattern = re.compile('href="\S*"')
            link_all = link_pattern.findall(content)
            for link in link_all:
                links.append(link)

            image_pattern = re.compile('img lazy-src=".*"')
            image_all = image_pattern.findall(content)
            for image in image_all:
                images.append(image)

            saletime_pattern = re.compile(u'<p class="presale-time".*?</span>', re.S)
            saletime_all = saletime_pattern.findall(content)
            for saletime in saletime_all:
                sale_time.append(saletime)

            price_pattern = re.compile('<em>.*?</em>')
            price_all = price_pattern.findall(content)
            for price in price_all:
                prices.append(price)

        for x in range(titles.__len__()):
            item = SuningRecommendItem()
            item['title'] = titles[x][7:-1]
            item['link'] = 'http://ju.suning.com' + links[x][6:-1]
            item['image'] = images[x][14:-1]
            item['sale_time'] = sale_time[x][-16:-7]
            item['price'] = prices[x][4:-5]
            print item['title']
            print item['link']
            print item['image']
            print item['sale_time']
            print item['price']
            print
            yield item
