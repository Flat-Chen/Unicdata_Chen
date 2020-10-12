# -*- coding: utf-8 -*-
import scrapy
import time
import json
import redis
import pymongo
import pandas as pd
import datetime
import re
from scrapy_redis.spiders import RedisSpider

pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=2)
con = redis.Redis(connection_pool=pool)


class DasoucheGzSpider(RedisSpider):
    name = 'dasouche_gz'
    allowed_domains = ['souche.com']
    # start_urls = ['https://aolai.souche.com//v2/evaluateApi/getEvaluateInfo.json?modelCode=229472&regDate=2020-01&mile=0.1&cityCode=00022']
    redis_key = "dasouche_gz_4city:start_urls"

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(DasoucheGzSpider, self).__init__(**kwargs)
        self.counts = 0
        self.c = con.client()

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.2.149',
        'MYSQL_DB': 'autohome',
        'MYSQL_TABLE': 'autohome_gz',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'dasouche',
        'MONGODB_COLLECTION': 'dasouche_gz',
        'CrawlCar_Num': 800000,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'DOWNLOAD_TIMEOUT': 10,
        'LOG_LEVEL': 'DEBUG',
        'COOKIES_ENABLED': True,
        'REDIS_URL': 'redis://192.168.2.149:6379/2',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse(self, response):
        data = response.text
        json_data = json.loads(data)
        normal = json_data['data']['normal']['evaluateValue']
        good = json_data['data']['good']['evaluateValue']
        excellent = json_data['data']['excellent']['evaluateValue']
        future_price = []
        for i in json_data['data']['good']['trends']:
            future_price.append(i['eval_price'])
        url = response.url
        vehicle_id = re.findall(r'modelCode=(.*?)&regDate', url)[0]
        redDate = re.findall(r'regDate=(.*?)&mile=', url)[0]
        mile = re.findall(r'&mile=(.*?)&cityCode=', url)[0]
        citycode = url[-5:]
        city = ''
        if citycode in '00002':
            city = '北京'
        elif citycode in '00022':
            city = '上海'
        elif citycode in '01978':
            city = '广州'
        elif citycode in '02273':
            city = '成都'
        # print(vehicle_id, redDate, mile, city, normal, good, excellent, future_price)
        item = {}
        item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['vehicle_id'] = vehicle_id
        item['redDate'] = redDate
        item['mile'] = mile
        item['city'] = city
        item['normal'] = normal
        item['good'] = good
        item['excellent'] = excellent
        item['future_price'] = future_price
        item['url'] = url
        item['status'] = url + '-' + str(datetime.datetime.now().year) + str(datetime.datetime.now().month)
        yield item
