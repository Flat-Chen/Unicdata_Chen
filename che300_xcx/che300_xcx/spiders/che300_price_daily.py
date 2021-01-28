# -*- coding: utf-8 -*-
import logging
import time
import re
import os
import redis
import pymysql
import scrapy
import tempfile
import requests
import json

from lxml import etree
from fontTools.ttLib import TTFont
# from che300_new.items import Che300PriceDaily
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str

pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=8)
con = redis.Redis(connection_pool=pool)
# dbconn = pymysql.connect(host="192.168.1.94", database='for_android', user="dataUser94", password="94dataUser@2020",
#                          port=3306, charset='utf8')
# cur = dbconn.cursor()

website = 'che300_price_daily'


# class Che300PriceDailySpider(scrapy.Spider):
class Che300PriceDailySpider(RedisSpider):
    name = website
    allowed_domains = ['che300.com']
    redis_key = "che300_price_daily:start_urls"

    # start_urls = ['https://www.che300.com/partner/result.php?prov=9&city=9&brand=9&series=2233&model=22414&registerDate=2017-1&mileAge=8&intention=0&partnerId=ynhcj&unit=1&sn=624e150569cc97df95e6c2de9fcee043&sld=cc']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(Che300PriceDailySpider, self).__init__(**kwargs)
        self.counts = 0
        self.c = con.client()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        }

    def make_request_from_data(self, data):
        url = bytes_to_str(data, self.redis_encoding)
        return self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        """ This method is deprecated. """
        return scrapy.Request(url, headers=self.headers, dont_filter=True)

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.2.149',
        'MYSQL_DB': 'che300',
        'MYSQL_TABLE': 'che300_price_daily',
        'MYSQL_PWD': 'Datauser@2020',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'che300',
        'MONGODB_COLLECTION': 'che300_price_daily',
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'REDIS_URL': 'redis://192.168.2.149:6379/8',
        'DOWNLOAD_TIMEOUT': 5,
        'RETRY_ENABLED': False,
        'RETRY_TIMES': 1,
        'COOKIES_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            # 'che300_new.middlewares.MoGuProxyMiddleware': 543,
            'che300_xcx.middlewares.Che300XcxProxyMiddleware': 400,
            'che300_xcx.middlewares.Che300XcxUserAgentMiddleware': 200,
            'che300_xcx.middlewares.CaptchaMiddleware': 100,
        }
    }

    def structure_http(self, result):
        # 'https://m.che300.com/partner/result.php?prov=3&city=3&brand=50&series=569&model=23438&registerDate=2015-1&mileAge=0.1&intention=0&partnerId=wechat_01&unit=1&sld=sh'
        meta = dict()
        brand = re.search(r'brand=(.*?)&', result).group(1)
        series = re.search(r'series=(.*?)&', result).group(1)
        model = re.search(r'&model=(.*?)&', result).group(1)
        mile = re.search(r'&mileAge=(.*?)&', result).group(1)
        city = re.search(r'&city=(.*?)&', result).group(1)
        prov = re.search(r'prov=(.*?)&', result).group(1)
        registerDate = re.search(r'registerDate=(.*?)&', result).group(1)
        meta['brand'] = brand
        meta['series'] = series
        meta['model'] = model
        meta['registerDate'] = registerDate
        meta['mile'] = mile
        meta['city'] = city
        meta['prov'] = prov
        return meta

    def parse(self, response):
        response_ = str(response.body)
        #
        try:
            meta = self.structure_http(response.url)
            item = dict()
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            item["brand"] = meta["brand"]
            item["series"] = meta["series"]
            item["salesdescid"] = meta["model"]
            item["regDate"] = meta["registerDate"]
            item["cityid"] = meta["city"]
            item["prov"] = meta["prov"]
            item["mile"] = meta["mile"]
            evalResult = json.loads(re.findall(r"window.evalResult = \\\'(.*?)\\';", response_)[0])[0]
            for k, v in evalResult.items():
                item[k] = v
            yield item
        except Exception as e:
            logging.error('解析数据出错', e)
            con.rpush('che300_price_daily:start_urls', response.url)
            logging.warning('==================url重新添加到redis尾部===================')
