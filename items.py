# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongItem(scrapy.Item):
    idcode = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()


class TmallItem(scrapy.Item):
    idcode = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    sale = scrapy.Field()


class AmazonItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()


class DangdangItem(scrapy.Item):
    title = scrapy.Field()
    idcode = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    comment = scrapy.Field()
    keyword = scrapy.Field()


class SuningItem(scrapy.Item):
    title = scrapy.Field()
    idcode = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    keyword = scrapy.Field()


class GomeItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    comment = scrapy.Field()
    keyword = scrapy.Field()


class YhdItem(scrapy.Item):
    title = scrapy.Field()
    idcode = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    keyword = scrapy.Field()


class JingdongRecommendItem(scrapy.Item):
    idcode = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()


class DangdangRecommendItem(scrapy.Item):
    link = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    discount = scrapy.Field()


class GomeRecommendItem(scrapy.Item):
    link = scrapy.Field()
    image = scrapy.Field()


class SuningRecommendItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    sale_time = scrapy.Field()
    price = scrapy.Field()
