# -*- coding: utf-8 -*-
import time
import re
import os
import redis
import json
import scrapy
import tempfile
import requests
import logging
from lxml import etree
from fontTools.ttLib import TTFont
from scrapy_redis.spiders import RedisSpider

from scrapy_redis.utils import bytes_to_str

pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=8)
con = redis.Redis(connection_pool=pool)

website = 'che300_21price_sh'


# class Che30021PriceShSpider(RedisSpider):
class Che30021PriceShSpider(scrapy.Spider):
    name = website
    redis_key = "che300_21price:start_urls"

    # allowed_domains = ['che300.com']
    # start_urls = ['http://che300.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(Che30021PriceShSpider, self).__init__(**kwargs)
        self.c = con.client()
        print(os.path.abspath('./'))
        self.font = TTFont('./tools/font/base.woff')  # 读取woff文件
        # 'projects/che300_new/tools/font/base.woff'
        # 'projects/che300_new/che300_new/spiders/che300_price_daily.py'
        self.num_list = ['uniF3F3', 'uniF142', 'uniE722', 'uniF3EB', 'uniF83F', 'uniEFFD', 'uniE2AA', 'uniE517',
                         'uniF588', 'uniF790', 'uniE0C8']
        self.num_dict = {'uniF3F3': 0, 'uniF142': 1, 'uniE722': 2, 'uniF3EB': 3, 'uniF83F': 4, 'uniEFFD': 5,
                         'uniE2AA': 6, 'uniE517': 7, 'uniF588': 8, 'uniF790': 9, 'uniE0C8': '.'}
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            # "Referer": "https://m.che300.com/wechat_01",
        }

    def make_request_from_data(self, data):
        url = bytes_to_str(data, self.redis_encoding)
        return self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        """ This method is deprecated. """
        return scrapy.Request(url, headers=self.headers, dont_filter=True)

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'che300',
        'MYSQL_TABLE': 'che300_21price_sh',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'che300',
        'MONGODB_COLLECTION': 'che300_21price_sh',
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'REDIS_URL': 'redis://192.168.2.149:6379/8',
        'DOWNLOAD_TIMEOUT': 8,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,
        'DOWNLOADER_MIDDLEWARES': {
            'che300_xcx.middlewares.Che300XcxUserAgentMiddleware': 543,
            'che300_xcx.middlewares.Che300XcxProxyMiddleware': 400,
            # 'che300_new.middlewares.Che300NewUserAgentMiddleware': 100,
            # 'che300_xcx.middlewares.Captcha21Middleware': 500,
        }

    }

    def start_requests(self):
        while 1:
            url = con.lpop('che300_21price:start_urls')
            print(url)
            url = bytes.decode(url)
            yield scrapy.Request(str(url), meta={'requests_url': url})

    def string_to_file(self, string):
        file_like_obj = tempfile.NamedTemporaryFile()
        file_like_obj.write(string)
        # 确保string立即写入文件
        file_like_obj.flush()
        # 将文件读取指针返回到文件开头位置
        file_like_obj.seek(0)
        return file_like_obj

    def parse_front_html(self, tmpe_file, html):
        new_font_dict = dict()
        font1 = TTFont(tmpe_file)
        # font1 = TTFont('./font/new_base.woff')  # 读取新的woff文件
        ff_list = font1.getGlyphNames()  # 返回一个对象
        ff_news = font1.getGlyphOrder()
        for fo in ff_news:
            fo2 = font1['glyf'][fo]
            for fff1 in self.num_list:
                fo3 = self.font['glyf'][fff1]
                if fo2 == fo3:
                    k = fo.replace("uni", "&#x").lower()
                    v = self.num_dict[fff1]
                    new_font_dict[fo.replace("uni", "&#x").lower()] = self.num_dict[fff1]
        #             html = html.replace(k, str(v))
        # for k, v in new_font_dict.items():
        #     html = html.replace(k, str(v))
        return new_font_dict

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
        if 'forbidden' in response.url:
            con.rpush('che300_21price:start_urls', response.meta['requests_url'])
            logging.warning('出现验证码了，重新将URL加入到redis队列尾部')
        else:
            try:
                font_url = re.findall('url\("(.*?)"\) format\("woff"\);', response.text, re.M)[0]
                font = requests.get(font_url, headers=self.headers)
                tmpe_file = self.string_to_file(font.content)
                new_font_dict = self.parse_front_html(tmpe_file, response.text)
                # print(new_font_dict)

                response_ = response.text
                # 替换字体
                for k, v in new_font_dict.items():
                    if k in response_:
                        response_ = response_.replace(k, str(v))
                html = etree.HTML(response_)
                meta = self.structure_http(response.url)
                item = dict()
                item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
                item["url"] = response.url
                item["normal_price1"] = \
                    html.xpath("//div[@id='car-normal']//li[@class='dealer_low_buy_price stonefont']/text()")[0]
                item["normal_price2"] = \
                    html.xpath("//div[@id='car-normal']//div[@class='dealer_buy_price stonefont']/text()")[0]
                item["normal_price3"] = \
                    html.xpath("//div[@id='car-normal']//li[@class='individual_low_sold_price stonefont']/text()")[0]
                item["normal_price4"] = \
                    html.xpath("//div[@id='car-normal']//div[@class='individual_price stonefont']/text()")[0]
                item["normal_price5"] = \
                    html.xpath("//div[@id='car-normal']//li[@class='dealer_low_sold_price stonefont']/text()")[0]
                item["normal_price6"] = html.xpath("//div[@id='car-normal']//div[@class='dealer_price stonefont']/text()")[
                    0]
                item["normal_price7"] = \
                    html.xpath("//div[@id='car-normal']//li[@class='dealer_high_sold_price stonefont']/text()")[0]

                item["good_price1"] = \
                    html.xpath("//div[@id='car-good']//li[@class='dealer_low_buy_price stonefont']/text()")[0]
                item["good_price2"] = html.xpath("//div[@id='car-good']//div[@class='dealer_buy_price stonefont']/text()")[
                    0]
                item["good_price3"] = \
                    html.xpath("//div[@id='car-good']//li[@class='individual_low_sold_price stonefont']/text()")[0]
                item["good_price4"] = html.xpath("//div[@id='car-good']//div[@class='individual_price stonefont']/text()")[
                    0]
                item["good_price5"] = \
                    html.xpath("//div[@id='car-good']//li[@class='dealer_low_sold_price stonefont']/text()")[0]
                item["good_price6"] = html.xpath("//div[@id='car-good']//div[@class='dealer_price stonefont']/text()")[0]
                item["good_price7"] = \
                    html.xpath("//div[@id='car-good']//li[@class='dealer_high_sold_price stonefont']/text()")[0]

                item["excellent_price1"] = \
                    html.xpath("//div[@id='car-excellent']//li[@class='dealer_low_buy_price stonefont']/text()")[0]
                item["excellent_price2"] = \
                    html.xpath("//div[@id='car-excellent']//div[@class='dealer_buy_price stonefont']/text()")[0]
                item["excellent_price3"] = \
                    html.xpath("//div[@id='car-excellent']//li[@class='individual_low_sold_price stonefont']/text()")[0]
                item["excellent_price4"] = \
                    html.xpath("//div[@id='car-excellent']//div[@class='individual_price stonefont']/text()")[0]
                item["excellent_price5"] = \
                    html.xpath("//div[@id='car-excellent']//li[@class='dealer_low_sold_price stonefont']/text()")[0]
                item["excellent_price6"] = \
                    html.xpath("//div[@id='car-excellent']//div[@class='dealer_price stonefont']/text()")[0]
                item["excellent_price7"] = \
                    html.xpath("//div[@id='car-excellent']//li[@class='dealer_high_sold_price stonefont']/text()")[0]

                # item["evalResult"] = str(re.findall("evalResult='(.*?)';", response_.replace(' ', ''))[0])
                item["evalResult"] = json.dumps(
                    (json.loads(re.findall("evalResult='(.*?)';", response_.replace(' ', ''))[0])), ensure_ascii=False)

                item["brand"] = meta["brand"]
                item["series"] = meta["series"]
                item["salesdescid"] = meta["model"]
                item["regDate"] = meta["registerDate"]
                item["cityid"] = meta["city"]
                item["prov"] = meta["prov"]
                item["mile"] = meta["mile"]
                # item["statusplus"] = response.url
                # item["status"] = item["statusplus"]
                # print(item)
                if r'\u' not in str(item):
                    yield item
                else:
                    logging.warning('验证码过去了，价格是乱码，舍弃，不存')
                    con.rpush('che300_21price:start_urls', response.url)
            except:
                con.rpush('che300_21price:start_urls', response.meta['requests_url'])
                logging.warning('页面出现错误，重新将URL加入到redis队列尾部')

        next_url = con.lpop('che300_21price:start_urls')
        url = bytes.decode(next_url)
        yield scrapy.Request(str(url), meta={'requests_url': url}, callback=self.parse)
