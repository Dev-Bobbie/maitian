# -*- coding: utf-8 -*-

# Scrapy settings for maitian project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'maitian'

SPIDER_MODULES = ['maitian.spiders']
NEWSPIDER_MODULE = 'maitian.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'maitian (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'maitian.middlewares.MaitianSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'maitian.middlewares.RandomUserAgentMiddlware':542,
    'maitian.middlewares.ProxyMiddleware': 543,
    'maitian.middlewares.DownloadRetryMiddleware': 544,
    #'maitian.middlewares.MaitianDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'maitian.pipelines.MongoDBPipeline': 300,
    'maitian.pipelines.RedisPipeline': 301,
    # 'maitian.pipelines.MysqlPipline': 302,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


MONGOHOST  = "192.168.33.11"
MONGOPORT = 27017
DB = "maitian"
COLLECTION = 'items'

# 代理服务器
#PROXY_SERVER = "http://http-cla.abuyun.com:9030"
PROXY_SERVER = "http://111.206.6.101:80"
COMMANDS_MODULE = 'maitian.monitor'

## 代理服务器隧道验证信息
# PROXY_USER = "HSAM1367RL55808C"
# PROXY_PASS = "4AE087EF4788C11C"

MYSQL_PIPELINE_URL = 'mysql://root:mysql@192.168.33.11/test'
REDIS_PIPELINE_URL = 'redis://192.168.33.11:6379'
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 400]


DEPLOY_PROJECT = False

if DEPLOY_PROJECT:
    # scrapy-redis 增量爬虫配置
    # 1. 设置请求调度器采用 scrapy-redis 实现方案
    SCHEDULER = "scrapy_redis.scheduler.Scheduler"
    # 2. 设置过滤类，实现去重功能
    DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
    # 3. 配置redis
    REDIS_HOST = '192.168.33.11'
    REDIS_PORT = 6379
    # 4. 设置持久化，当程序结束时是否清空 SCHEDULER_PERSIST 默认 False,如果程序结束自动清空
    SCHEDULER_PERSIST = True