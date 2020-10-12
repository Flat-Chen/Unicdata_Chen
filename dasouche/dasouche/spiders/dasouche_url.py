# -*- coding: utf-8 -*-
import scrapy
import scrapy
import time
import json
import pymongo
import pandas as pd
import datetime
import pymysql
import re
from dasouche.items import DasoucheItem

settings = {
    "MONGODB_SERVER": "192.168.2.149",
    "MONGODB_PORT": 27017,
    "MONGODB_DB": "dasouche",
    "MONGODB_COLLECTION": "dasouche_car",
}
uri = f'mongodb://{settings["MONGODB_SERVER"]}:{settings["MONGODB_PORT"]}/'

connection = pymongo.MongoClient(uri)
db = connection[settings['MONGODB_DB']]
collection = db[settings['MONGODB_COLLECTION']]
# 四个城市 北京 上海 广州 成都
city_dic = {'00002', '00022', '01978', '02273'}


class DasoucheUrlSpider(scrapy.Spider):
    name = 'dasouche_url'
    allowed_domains = ['souche.com']

    # start_urls = ['http://souche.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(DasoucheUrlSpider, self).__init__(**kwargs)
        self.counts = 0
        self.data = pd.DataFrame(
            list(collection.find({}, {'vehicle_id': 1, 'family_id': 1, 'year': 1})))
        del self.data["_id"]
        self.data['year'] = self.data['year'].astype('int')
        self.now_year = datetime.datetime.now().year
        now_month = datetime.datetime.now().month
        self.now_month = f"0{str(now_month)}" if now_month < 10 else now_month
        self.now_month = int(self.now_month)

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'residual_value',
        'MYSQL_TABLE': 'autohome_gz',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'dasouche',
        'MONGODB_COLLECTION': 'dasouche_url',
        'CrawlCar_Num': 8000000,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'COOKIES_ENABLED': True,
        'ITEM_PIPELINES': {
            'dasouche.pipelines.MasterPipeline': 300,
        }

    }

    def start_requests(self):
        url = "https://www.baidu.com/"
        yield scrapy.Request(
            url=url,
            dont_filter=True,
        )

    def parse(self, response):
        item = DasoucheItem()
        for city in city_dic:
            for index, rows in self.data.iterrows():
                if self.now_year > rows['year']:
                    if self.now_year - rows['year'] >= 4:
                        year_list = [i for i in range(rows['year'], rows['year'] + 4)]
                    else:
                        year_list = [i for i in range(rows['year'], self.now_year + 1)]
                    for year in year_list:
                        if year == self.now_year:
                            month = self.now_month - 1
                            month = f"0{str(month)}" if month < 10 else month
                            carRegDate = f'{year}-{month}'
                            mileage = 0.1
                            url = f'https://aolai.souche.com//v2/evaluateApi/getEvaluateInfo.json?modelCode={rows["vehicle_id"]}&regDate={carRegDate}&mile={mileage}&cityCode={city}'
                            item['url'] = url
                            yield item
                        else:
                            month = f"0{str(self.now_month)}" if self.now_month < 10 else self.now_month
                            carRegDate = f'{year}-{month}'
                            mileage = (self.now_year - year) * 2
                            url = f'https://aolai.souche.com//v2/evaluateApi/getEvaluateInfo.json?modelCode={rows["vehicle_id"]}&regDate={carRegDate}&mile={mileage}&cityCode={city}'
                            item['url'] = url
                            yield item
                else:
                    month = self.now_month - 1
                    month = f"0{str(month)}" if month < 10 else month
                    carRegDate = f'{self.now_year}-{month}'
                    mileage = 0.1
                    url = f'https://aolai.souche.com//v2/evaluateApi/getEvaluateInfo.json?modelCode={rows["vehicle_id"]}&regDate={carRegDate}&mile={mileage}&cityCode={city}'
                    item['url'] = url
                    yield item
