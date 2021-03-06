# -*- coding: utf-8 -*-
import time

import scrapy

from maitian.settings import DEPLOY_PROJECT

if DEPLOY_PROJECT:
    from scrapy_redis.spiders import RedisSpider as Spider
else:
    from scrapy import Spider


class ZufangSpiderSpider(Spider):
    start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    name = 'zufang'
    start_urls = ['http://bj.maitian.cn/zfall/PG1/']

    redis_key = "zufang:maitian:start_url"

    def parse(self, response):
        for zufang_item in response.xpath('//div[@class="list_title"]'):
            from maitian.items import MaitianItem
            item = MaitianItem()

            item['title']= zufang_item.xpath('./h1/a/text()').extract_first().strip()
            item['price']= zufang_item.xpath('./div[@class="the_price"]/ol/strong/span/text()').extract_first().strip()
            item['area']=zufang_item.xpath('./p/span/text()').extract_first().replace('㎡', '').strip()
            item['district'] = zufang_item.xpath('./p//text()').re(r'昌平|朝阳|东城|大兴|丰台|海淀|石景山|顺义|通州|西城')[0]

            yield item
        next_page_url = response.xpath('//div[@id="paging"]/a[@class="down_page"]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url),callback=self.parse)

