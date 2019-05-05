# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy.mail import MailSender


class ZufangSpiderSpider(scrapy.Spider):
    start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    name = 'zufang'
    start_urls = ['http://bj.maitian.cn/zfall/PG1/']

    def parse(self, response):
        try:
            # 使用Crawl api记录文章详情页请求成功的Request
            self.crawler.stats.inc_value("ArticleDetail_Success_Reqeust")
        except Exception as e:
            _ = e
        for zufang_item in response.xpath('//div[@class="list_title"]'):
            yield {
                'title': zufang_item.xpath('./h1/a/text()').extract_first().strip(),
                'price': zufang_item.xpath('./div[@class="the_price"]/ol/strong/span/text()').extract_first().strip(),
                'area': zufang_item.xpath('./p/span/text()').extract_first().replace('㎡','').strip(),
                'district': zufang_item.xpath('./p//text()').re(r'昌平|朝阳|东城|大兴|丰台|海淀|石景山|顺义|通州|西城')[0]
            }
        next_page_url = response.xpath('//div[@id="paging"]/a[@class="down_page"]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url),callback=self.parse,errback=self.error_back)

    def error_back(self, e):
        """
        使用Crawl API记录失败请求数量并Debug错误原因
        """
        self.logger.debug('Error: %s' % (e.reason))
        self.crawler.stats.inc_value("Failed_Reqeust")
        _ = self


    def close(self, reason):
        """
        爬虫邮件报告状态
        """
        # 结束时间
        fnished = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 创建邮件发送对象
        mail = MailSender.from_settings(self.settings)
        # 邮件内容
        spider_name = self.settings.get('BOT_NAME')
        start_time = self.start
        artice_success_request = self.crawler.stats.get_value("ArticleDetail_Success_Reqeust")
        failed_request = self.crawler.stats.get_value("Failed_Reqeust")
        # 若请求成功, 则默认为0
        if failed_request == None:
            failed_request = 0
        insert_into_success = self.crawler.stats.get_value("Success_InsertedInto_MySqlDB")
        failed_db = self.crawler.stats.get_value("Failed_InsertInto_DB")
        # 若插入成功, 则默认为0
        if failed_db == None:
            failed_db = 0
        fnished_time = fnished
        body = "爬虫名称: {}\n\n 开始时间: {}\n\n 文章请求成功总量：{}\n\n 请求失败总量：{} \n\n 数据库存储总量：{}\n 数据库存储失败总量：{}\n\n 结束时间  : {}\n".format(
            spider_name,
            start_time,
            artice_success_request,
            failed_request,
            insert_into_success,
            failed_db,
            fnished_time)
        try:
            # 发送邮件
            mail.send(to=self.settings.get('RECEIVE_LIST'), subject=self.settings.get('SUBJECT'), body=body)
        except Exception as e:
            self.logger.error("Send Email Existing")