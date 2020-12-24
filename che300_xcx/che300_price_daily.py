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

pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=15)
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

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(Che300PriceDailySpider, self).__init__(**kwargs)
        self.counts = 0
        # print("*"*100)
        # print(os.path.abspath('./'))
        # self.font = TTFont('./tools/font/base.woff')  # 读取woff文件
        # 'projects/che300_new/tools/font/base.woff'
        # 'projects/che300_new/che300_new/spiders/che300_price_daily.py'
        # self.num_list = ['uniF3F3', 'uniF142', 'uniE722', 'uniF3EB', 'uniF83F', 'uniEFFD', 'uniE2AA', 'uniE517', 'uniF588', 'uniF790', 'uniE0C8']
        # self.num_dict = {'uniF3F3': 0, 'uniF142': 1, 'uniE722': 2, 'uniF3EB': 3, 'uniF83F': 4, 'uniEFFD': 5, 'uniE2AA': 6, 'uniE517': 7, 'uniF588': 8, 'uniF790': 9, 'uniE0C8': '.'}
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
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'REDIS_URL': 'redis://192.168.2.149:6379/15',
        'DOWNLOAD_TIMEOUT': 5,
        'RETRY_ENABLED': False,
        'RETRY_TIMES': 1,
        'COOKIES_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            # 'che300_new.middlewares.MoGuProxyMiddleware': 543,
            'che300_new.middlewares.Che300NewProxyMiddleware': 400,
            'che300_new.middlewares.Che300NewUserAgentMiddleware': 100,
            # 'che300_new.middlewares.MyproxiesSpiderMiddleware': 500,
        }

    }

    # def string_to_file(self, string):
    #     file_like_obj = tempfile.NamedTemporaryFile()
    #     file_like_obj.write(string)
    #     # 确保string立即写入文件
    #     file_like_obj.flush()
    #     # 将文件读取指针返回到文件开头位置
    #     file_like_obj.seek(0)
    #     return file_like_obj
    #
    # def parse_front_html(self, tmpe_file, html):
    #     new_font_dict = dict()
    #     font1 = TTFont(tmpe_file)
    #     # font1 = TTFont('./font/new_base.woff')  # 读取新的woff文件
    #     ff_list = font1.getGlyphNames()  # 返回一个对象
    #     ff_news = font1.getGlyphOrder()
    #     for fo in ff_news:
    #         fo2 = font1['glyf'][fo]
    #         for fff1 in self.num_list:
    #             fo3 = self.font['glyf'][fff1]
    #             if fo2 == fo3:
    #                 k = fo.replace("uni", "&#x").lower()
    #                 v = self.num_dict[fff1]
    #                 new_font_dict[fo.replace("uni", "&#x").lower()] = self.num_dict[fff1]
    #     #             html = html.replace(k, str(v))
    #     # for k, v in new_font_dict.items():
    #     #     html = html.replace(k, str(v))
    #     return new_font_dict

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
        # meta['mile'] = 0.1
        # meta['city'] = 3
        # meta['prov'] = 3
        meta['mile'] = mile
        meta['city'] = city
        meta['prov'] = prov
        return meta

    # def start_requests(self):
    #     url = "https://www.che300.com/partner/result.php?prov=10&city=10&brand=14&series=221&model=2940&registerDate=2011-12&mileAge=17&intention=0&partnerId=douyin&unit=1&sn=3a0b24fad548603ae422daf5590609a8&sld=heb"
    #     yield scrapy.Request(
    #             url=url,
    #             headers=self.headers)

    def parse(self, response):
        # font_url = re.findall('url\("(.*?)"\) format\("woff"\);', response.text, re.M)[0]
        # font = requests.get(font_url, headers=self.headers)
        # tmpe_file = self.string_to_file(font.content)
        # new_font_dict = self.parse_front_html(tmpe_file, response.text)
        # print(new_font_dict)
        response_ = response.text
        # 替换字体
        # for k, v in new_font_dict.items():
        #     if k in response_:
        #         response_ = response_.replace(k, str(v))
        # html = etree.HTML(response_)
        meta = self.structure_http(response.url)
        item = dict()
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        # item["price1"] = html.xpath("//li[@class='dealer_low_buy_price stonefont']/text()")[0]
        # item["price2"] = html.xpath("//div[@class='dealer_buy_price stonefont']/text()")[0]
        # item["price3"] = html.xpath("//li[@class='individual_low_sold_price stonefont']/text()")[0]
        # item["price4"] = html.xpath("//div[@class='individual_price stonefont']/text()")[0]
        # item["price5"] = html.xpath("//li[@class='dealer_low_sold_price stonefont']/text()")[0]
        # item["price6"] = html.xpath("//div[@class='dealer_price stonefont']/text()")[0]
        # item["price7"] = html.xpath("//li[@class='dealer_high_sold_price stonefont']/text()")[0]
        item["brand"] = meta["brand"]
        item["series"] = meta["series"]
        item["salesdescid"] = meta["model"]
        item["regDate"] = meta["registerDate"]
        item["cityid"] = meta["city"]
        item["prov"] = meta["prov"]
        item["mile"] = meta["mile"]
        evalResult = json.loads(re.findall("evalResult='(.*?)';", response_.replace(' ', ''))[0])[0]
        for k, v in evalResult.items():
            item[k] = v

        # item["statusplus"] = response.url
        # item["status"] = item["statusplus"]
        # if item["price1"]:
        yield item
            # print(item)
        # else:
        #     self.c.rpush('che300_price_daily:start_urls', response.url)
        # print(item)
        next_url = self.c.lpop('che300_price_daily:start_urls')
        if next_url:
            start_url = bytes.decode(next_url)
            yield scrapy.Request(
                url=start_url,
                callback=self.parse,
                # headers=self.headers
            )

        # else:
        #     cur.execute("update che300_detection set che300_price_daily_update_test=1 WHERE che300_price_daily_update_test=0")
        #     dbconn.commit()