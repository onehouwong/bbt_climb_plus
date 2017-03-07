# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BbtClimbPlusPipeline(object):
    def __init__(self):
        self.file = open('jd.txt', 'a+')

    def process_item(self, item, spider):
        return item


import pymongo


class MongoPipeline(object):
    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        print 'from_crawler'
        mongo_uri = crawler.settings.get('MONGO_URI'),
        mongo_db = crawler.settings.get('MONGO_DATABASE', 'items')
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        print 'open_spider'
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.client.crawlResult.authenticate('bbt', '12345678', mechanism='SCRAM-SHA-1') #auth
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        print 'closespuder'
        self.client.close()

    def process_item(self, item, spider):
        print 'process_item'
        self.db[self.collection_name].insert(dict(item))
        return item
