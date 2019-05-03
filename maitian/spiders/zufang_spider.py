# -*- coding: utf-8 -*-
import scrapy


class ZufangSpiderSpider(scrapy.Spider):
    name = 'zufang_spider'
    allowed_domains = ['http://bj.maitian.cn/zfall/PG1']
    start_urls = ['http://http://bj.maitian.cn/zfall/PG1/']

    def parse(self, response):
        pass
