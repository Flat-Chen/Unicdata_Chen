# -*- coding: utf-8 -*-

# Scrapy settings for carbuisness_new project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'carbuisness_new'

SPIDER_MODULES = ['carbuisness_new.spiders']
NEWSPIDER_MODULE = 'carbuisness_new.spiders'

""" mysql """
MYSQL_SERVER = "192.168.1.94"
MYSQL_USER = "dataUser94"
MYSQL_PWD= "94dataUser@2020"
MYSQL_PORT = 3306
MYSQL_DB = "people_zb"
MYSQL_TABLE = ""

""" mongodb """
# MONGODB_SERVER = "192.168.1.94"
# MONGODB_SERVER = "192.168.1.241"
MONGODB_SERVER = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DB = "usedcar"
MONGODB_COLLECTION = "xcar"
CrawlCar_Num = 2000000

# 出现错误吗,重新请求
RETRY_HTTP_CODES = [502, 503, 504, 400, 403, 404, 408]
# 是否开启重试
RETRY_ENABLED = True
# 重试次数
RETRY_TIMES = 3


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'carbuisness_new (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'carbuisness_new.middlewares.CarbuisnessNewSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'carbuisness_new.middlewares.CarbuisnessNewDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    # 'carbuisness.rotate_useragent.RotateUserAgentMiddleware': 543,  #543
    # 'carbuisness_new.rotate_useragent.SeleniumMiddleware': 400,
    # 'carbuisness.middlewares.MyproxiesSpiderMiddleware':None,
    'carbuisness_new.middlewares.MyproxiesSpiderMiddleware': 301,
    'carbuisness_new.middlewares.ProxyMiddleware': 300,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}
HTTPERROR_ALLOWED_CODES = []
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

ITEM_PIPELINES = {
   'carbuisness_new.pipelines.CarbuisnessNewPipeline': 300,
   # 'carbuisness_new.pipelines.MasterPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# RETRY_TIMES = 8

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

BLM_PATH = "/home/usedcar/blm/"
PHANTOMJS_PATH = "/root/phantomjs/bin/phantomjs"
CHROME_PATH = "/root/chromedriver"
FIREFOX_PATH = "D:/geckodriver.exe"

# RETRY_HTTP_CODES = [403, 503]
# REDIRECT_ENABLED = False

WEIXIN = "neshidai"

# 使用布隆过滤器
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
#
# # 增加调度配置
SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"

# Number of Hash Functions to use, defaults to 6
BLOOMFILTER_HASH_NUMBER = 6

# Redis Memory Bit of Bloomfilter Usage, 30 means 2^30 = 128MB, defaults to 30
BLOOMFILTER_BIT = 30

# 配置调度器持久化, 爬虫结束, 要不要清空Redis中请求队列和去重指纹的set。如果True, 就表示要持久化存储, 否则清空数据
SCHEDULER_PERSIST = False
#redis配置(下面有两种方式)
#方式一：没有密码
# REDIS_HOST = '192.168.1.241'
# REDIS_PORT = 6379
REDIS_URL = 'redis://192.168.1.241:6379/15'
FEED_EXPORT_ENCODING = 'utf-8'


#方式二：有密码
# REDIS_URL = 'redis://user:pass@hostname:6379'

# MYEXT_ENABLED: 是否启用扩展，启用扩展为 True， 不启用为 False
# IDLE_NUMBER: 关闭爬虫的持续空闲次数，持续空闲次数超过IDLE_NUMBER，爬虫会被关闭。默认为 360 ，也就是30分钟，一分钟12个时间单位
MYEXT_ENABLED = False      # 开启扩展
IDLE_NUMBER = 360           # 配置空闲持续时间单位为 360个 ，一个时间单位为5s
# # 在 EXTENSIONS 配置，激活扩展
EXTENSIONS = {
    'carbuisness_new.extensions.RedisSpiderSmartIdleClosedExensions': 500,
}
