# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import json
import traceback

# import MySQLdb
# import MySQLdb.cursors
import dj_database_url
import txmongo
from scrapy import Item
import dj_redis_url
import txredisapi

from scrapy.exceptions import NotConfigured
from twisted.enterprise import adbapi
from twisted.internet import defer



class MongoDBPipeline(object):

    def __init__(self, host, port, db, collection):
        self.host = host
        self.port = port or 27017
        self.db = db
        self.collection = collection

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get("MONGOHOST") or "127.0.0.1"
        port = crawler.settings.get("MONGOPORT") or 27017
        db = crawler.settings.get("DB")  # database
        collection = crawler.settings.get("COLLECTION")  # collection
        return cls(host, port, db, collection)

    def open_spider(self, spider):
        self.mongo = txmongo.MongoConnection(self.host, self.port, pool_size=10)
        self.col_instance = self.mongo[self.db][self.collection]

    def close_spider(self, spider):
        self.mongo.disconnect()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        item = dict(item) if isinstance(item, Item) else item
        yield self.col_instance.update_one(
            {'title': item.get("title"),
             'price': item.get("price")},
            {'$set': item},
            upsert=True)
        defer.returnValue(item)


class RedisPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):

        redis_url = crawler.settings.get('REDIS_PIPELINE_URL', None)
        if not redis_url:
            raise NotConfigured

        return cls(crawler, redis_url)

    def __init__(self, crawler, redis_url):

        self.redis_url = redis_url
        self.report_connection_error = True

        args = RedisPipeline.parse_redis_url(redis_url)
        self.connection = txredisapi.lazyConnectionPool(connectTimeout=5,
                                                        replyTimeout=5,
                                                        **args)
    @defer.inlineCallbacks
    def process_item(self, item, spider):
        logger = spider.logger
        try:
            yield self.connection.lpush("maitian", json.dumps(item,ensure_ascii=False))

        except txredisapi.ConnectionError:
            if self.report_connection_error:
                logger.error("Can't connect to Redis: %s" % self.redis_url)
                self.report_connection_error = False
        defer.returnValue(item)

    @staticmethod
    def parse_redis_url(redis_url):
        params = dj_redis_url.parse(redis_url)
        conn_kwargs = {}
        conn_kwargs['host'] = params['HOST']
        conn_kwargs['password'] = params['PASSWORD']
        conn_kwargs['dbid'] = params['DB']
        conn_kwargs['port'] = params['PORT']
        # Remove items with empty values
        conn_kwargs = dict((k, v) for k, v in conn_kwargs.items() if v)

        return conn_kwargs

    @staticmethod
    def get_md5(url):
        if isinstance(url, str):
            url = url.encode("utf-8")
        m = hashlib.md5()
        m.update(url)
        return m.hexdigest()


class MysqlPipline(object):
    def __init__(self, dbpool,mysql_url):
        self.dbpool = dbpool
        self.report_connection_error = True
        self.mysql_url = mysql_url

    @classmethod
    def from_settings(cls, settings):
        mysql_url = settings.get("MYSQL_PIPELINE_URL")
        dbparms = MysqlPipline.parse_mysql_url(mysql_url)
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool,mysql_url)

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行

        logger = spider.logger

        try:
            yield self.dbpool.runInteraction(self.do_insert, item)
        except MySQLdb.OperationalError:
            if self.report_connection_error:
                logger.error("Can't connect to MySQL: %s" % self.mysql_url)
                self.report_connection_error = False
        except:
            print(traceback.format_exc())

        defer.returnValue(item)


    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """INSERT INTO zufang (title, price, area, district)
                   VALUES (%s,%s,%s,%s)"""
        params = (
            item["title"],
            item["price"],
            item["area"],
            item["district"]
        )
        cursor.execute(insert_sql, params)
        # self.db.commit()   adbapi会自动提交数据的插入事实

    def close_spider(self, spider):
        """Discard the database pool on spider close"""
        self.dbpool.close()


    @staticmethod
    def parse_mysql_url(mysql_url):
        """
        Parses mysql url and prepares arguments for
        adbapi.ConnectionPool()
        """

        params = dj_database_url.parse(mysql_url)

        conn_kwargs = {}
        conn_kwargs['host'] = params['HOST']
        conn_kwargs['user'] = params['USER']
        conn_kwargs['passwd'] = params['PASSWORD']
        conn_kwargs['db'] = params['NAME']
        conn_kwargs['port'] = params['PORT']
        conn_kwargs['charset'] = 'utf8'
        conn_kwargs['cursorclass'] = MySQLdb.cursors.DictCursor
        conn_kwargs['use_unicode'] = True

        # Remove items with empty values
        conn_kwargs = dict((k, v) for k, v in conn_kwargs.items() if v)

        return conn_kwargs
