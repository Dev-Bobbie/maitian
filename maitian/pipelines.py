# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymongo
from scrapy import Item

class MongoDBPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        cls.DB_URI = crawler.settings.get('MONGO_DB_URI' , 'mongodb://localhost:27017/')
        cls.DB_NAME = crawler.settings.get('SCRAPY_DATA' , 'MONGO_DB_NAME')
        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URI)
        self.db = self.client[self.DB_NAME]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        post = dict(item) if isinstance(item, Item) else item
        try:
            collection.insert(post)
            # 记录成功插入的数据总量
            spider.crawler.stats.inc_value('Success_InsertedInto_MySqlDB')
        except Exception as e:
            logging.error("Failed Insert Into, Reason: {}".format(e.args))
            # 记录插入失败的数据总量
            spider.crawler.stats.inc_value('Failed_InsertInto_DB')
        return item
