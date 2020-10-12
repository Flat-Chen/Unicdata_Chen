# -*- coding: utf-8 -*-

# Scrapy settings for tousu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tousu'

SPIDER_MODULES = ['tousu.spiders']
NEWSPIDER_MODULE = 'tousu.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'tousu (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

LOG_LEVEL = 'DEBUG'

""" mysql 配置"""
MYSQL_DB = 'shangqi'
MYSQL_TABLE = 'a315tousu'
MYSQL_PORT = '3306'
MYSQL_SERVER = '192.168.1.94'
MYSQL_USER = "dataUser94"
MYSQL_PWD = "94dataUser@2020"

""" splash 配置 """
SPLASH_URL = 'http://192.168.1.241:8050'
# SPLASH_URL = 'http://127.0.0.1:8050'
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
# 是否调试cookies
# SPLASH_COOKIES_DEBUG = True
# 是否记录400错误
SPLASH_LOG_400 = True

# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
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
# COOKIES_ENABLED = False

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
#    'tousu.middlewares.TousuSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
    # 'tousu.middlewares.TousuDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
    'tousu.middlewares.ProxyMiddleware': 400,
    # 'tousu.middlewares.SeleniumMiddleware': 401,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'tousu.pipelines.TousuPipeline': 300,
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

BRAND_DIC_TAG = {'名爵': '上汽乘用车',
                 '荣威': '上汽乘用车',
                 '斯柯达': '上汽大众',
                 '大众': '上汽大众',
                 '上汽大通': '上汽大通',
                 '别克': '上汽通用',
                 '凯迪拉克': '上汽通用',
                 '雪佛兰': '上汽通用',
                 '宝骏': '上汽通用',
                 '五菱汽车': '上汽通用',
                 '依维柯': '南京依维柯'}

BRAND_URL = {'名爵': 'http://tousu.315che.com/tousulist/serial/5964/0/0/0/1.htm',
             '荣威': 'http://tousu.315che.com/tousulist/serial/5789/0/0/0/1.htm',
             '斯柯达': 'http://tousu.315che.com/tousulist/serial/5974/0/0/0/1.htm',
             '大众': 'http://tousu.315che.com/tousulist/serial/93/0/0/0/1.htm',
             '上汽大通': 'http://tousu.315che.com/tousulist/serial/54/0/0/0/1.htm',
             '别克': 'http://tousu.315che.com/tousulist/serial/55/0/0/0/1.htm',
             '凯迪拉克': 'http://tousu.315che.com/tousulist/serial/105/0/0/0/1.htm',
             '雪佛兰': 'http://tousu.315che.com/tousulist/serial/56/0/0/0/1.htm',
             '宝骏': 'http://tousu.315che.com/tousulist/serial/11744/0/0/0/1.htm',
             '五菱汽车': 'http://tousu.315che.com/tousulist/serial/59/0/0/0/1.htm',
             '依维柯': 'http://tousu.315che.com/tousulist/serial/47/0/0/0/1.htm'}

BRAND_DIC = {'名爵': '上汽乘用车',
             '荣威': '上汽乘用车',
             '斯柯达': '上汽大众',
             '大众': '上汽大众',
             '上汽大通': '上汽大通',
             '别克': '上汽通用',
             '凯迪拉克': '上汽通用',
             '雪佛兰': '上汽通用',
             '宝骏': '上汽通用',
             '五菱汽车': '上汽通用',
             '依维柯': '南京依维柯'}
#
# BRAND_DIC = {
#              '吉利': '竞品',
#              '奇瑞': '竞品',
#              '江淮': '竞品',
#              '哈弗': '竞品',
#              '奔腾': '竞品',
#              '长安': '竞品',
#              '中华': '华晨中华',
#              }

# REDIS_URL = 'redis://192.168.1.92:6379/10'
# FEED_EXPORT_ENCODING = 'utf-8'

# 使用布隆过滤器
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#
# # 增加调度配置
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# # Number of Hash Functions to use, defaults to 6
# BLOOMFILTER_HASH_NUMBER = 6
#
# # Redis Memory Bit of Bloomfilter Usage, 30 means 2^30 = 128MB, defaults to 30
# BLOOMFILTER_BIT = 30

# 配置调度器持久化, 爬虫结束, 要不要清空Redis中请求队列和去重指纹的set。如果True, 就表示要持久化存储, 否则清空数据
# SCHEDULER_PERSIST = True

# 出现错误吗,重新请求
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]
# 是否开启重试
RETRY_ENABLED = True
# 重试次数
RETRY_TIMES = 6
# timeout响应时间
DOWNLOAD_TIMEOUT = 10
