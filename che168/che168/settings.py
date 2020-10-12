# -*- coding: utf-8 -*-

# Scrapy settings for che168 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'che168'

SPIDER_MODULES = ['che168.spiders']
NEWSPIDER_MODULE = 'che168.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'che168 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'che168.middlewares.Che168SpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'che168.middlewares.ProxyMiddleware': 100,
    'che168.middlewares.RotateUserAgentMiddleware': 200,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 800,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'che168.pipelines.UsedcarNewPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


MYSQL_SERVER = "192.168.1.94"
MYSQL_USER = "dataUser94"
MYSQL_PWD = "94dataUser@2020"
MYSQL_PORT = 3306
MYSQL_DB = "usedcar_update"
MYSQL_TABLE = ""

MONGODB_SERVER = "192.168.1.92"
MONGODB_PORT = 27017
MONGODB_DB = "usedcar"
MONGODB_COLLECTION = "xcar"

WEBSITE = ''

PHANTOMJS_PATH = "/usr/local/phantomjs/bin/phantomjs"
CHROME_PATH = "/usr/local/bin/chromedriver"

REDIRECT_ENABLED = False

# 出现错误吗,重新请求
RETRY_HTTP_CODES = [500, 502, 302]
# 是否开启重试
RETRY_ENABLED = True
# 重试次数
RETRY_TIMES = 5

HTTPERROR_ALLOWED_CODES = [301, 302, 503]

REDIS_URL = "redis://192.168.1.92:6379/15"

# 使用布隆过滤器
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# SCHEDULER_PERSIST = True

# 使用布隆过滤器
# DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
# # # 增加调度配置
# SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"

# 配置调度器持久化, 爬虫结束, 要不要清空Redis中请求队列和去重指纹的set。如果True, 就表示要持久化存储, 否则清空数据
SCHEDULER_PERSIST = False
