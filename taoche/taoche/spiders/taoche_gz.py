# -*- coding: utf-8 -*-
import datetime
import json
import time

import pandas as pd
import pymongo
import scrapy

settings = {
    "MONGODB_SERVER": "192.168.2.149",
    "MONGODB_PORT": 27017,
    "MONGODB_DB": "taoche",
    "MONGODB_COLLECTION": "taoche_car",
}
uri = f'mongodb://{settings["MONGODB_SERVER"]}:{settings["MONGODB_PORT"]}/'

connection = pymongo.MongoClient(uri)
db = connection[settings['MONGODB_DB']]
collection = db[settings['MONGODB_COLLECTION']]
city_list = ['110100', '310100', '440100', '510100']


class TaocheCarSpider(scrapy.Spider):
    name = 'taoche_gz'
    allowed_domains = ['taoche.com']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(TaocheCarSpider, self).__init__(**kwargs)
        self.counts = 0
        self.data = pd.DataFrame(
            list(collection.find({}, {'vehicle_id': 1, 'makeyear': 1})))
        del self.data["_id"]
        self.now_year = datetime.datetime.now().year
        self.now_month = datetime.datetime.now().month
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Referer": "https://www.taoche.com/pinggu/result.html?t=7&b=2&s=5381&c=129308&y=2019-12-1&m=1&z=2401&token=f7440cc7-b0d3-44b8-a154-2b3eca1f82cc&brname=%25E5%25A5%2594%25E9%25A9%25B0",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

    is_debug = True
    custom_debug_settings = {
        # 'MYSQL_SERVER': '192.168.1.94',
        # 'MYSQL_DB': 'taoche',
        # 'MYSQL_TABLE': 'taoche',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'taoche',
        'MONGODB_COLLECTION': 'taoche_gz',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        url = 'https://proconsumer.taoche.com/c-carsource-consumer/carsource/get-car-eval'
        for city in city_list:
            for index, rows in self.data.iterrows():
                if self.now_year > rows['makeyear']:
                    if self.now_year - rows['makeyear'] >= 4:
                        year_list = [i for i in range(rows['makeyear'], rows['makeyear'] + 4)]
                    else:
                        year_list = [i for i in range(rows['makeyear'], self.now_year + 1)]
                    for year in year_list:
                        if year == self.now_year:
                            month = self.now_month - 1
                            month = f"0{str(month)}" if month < 10 else month
                            carRegDate = f'{year}-{month}-01'
                            mileage = 0.1
                            data = {
                                'carRegDate': carRegDate,
                                'cityId': city,
                                'mileage': mileage,
                                'terminal': 30,
                                'vehicleModelId': rows['vehicle_id'],
                            }
                            data = json.dumps(data)
                            yield scrapy.Request(url=url, method='POST', body=data, headers=self.headers,
                                                 meta={'info': (rows['vehicle_id'], carRegDate, mileage, city)})
                        else:
                            month = f"0{str(self.now_month)}" if self.now_month < 10 else self.now_month
                            carRegDate = f'{year}-{month}-01'
                            mileage = (self.now_year - year) * 2
                            data = {
                                'carRegDate': carRegDate,
                                'cityId': city,
                                'mileage': mileage,
                                'terminal': 30,
                                'vehicleModelId': rows['vehicle_id'],
                            }
                            data = json.dumps(data)
                            yield scrapy.Request(url=url, method='POST', body=data, headers=self.headers,
                                                 meta={'info': (rows['vehicle_id'], carRegDate, mileage, city)})
                else:
                    month = self.now_month - 1
                    month = f"0{str(month)}" if month < 10 else month
                    carRegDate = f'{self.now_year}-{month}-01'
                    mileage = 0.1
                    data = {
                        'carRegDate': carRegDate,
                        'cityId': city,
                        'mileage': mileage,
                        'terminal': 30,
                        'vehicleModelId': rows['vehicle_id'],
                    }
                    data = json.dumps(data)
                    yield scrapy.Request(url=url, method='POST', body=data, headers=self.headers,
                                         meta={'info': (rows['vehicle_id'], carRegDate, mileage, city)})

    def parse(self, response):
        vehicle_id, carRegDate, mileage, city = response.meta.get('info')
        if '"normalMaxPrice":0.0,"betterMinPrice":0.0' in response.text:
            print('               ' + vehicle_id + '没有估值数据')
        else:
            data = response.text
            json_data = json.loads(data)
            salePrice = json_data['data']['salePrice']
            normalMinPrice = json_data['data']['normalMinPrice']
            normalMaxPrice = json_data['data']['normalMaxPrice']
            betterMinPrice = json_data['data']['betterMinPrice']
            betterMaxPrice = json_data['data']['betterMaxPrice']
            bestMinPrice = json_data['data']['bestMinPrice']
            bestMaxPrice = json_data['data']['bestMaxPrice']

            item = {}
            item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['vehicle_id'] = vehicle_id
            item['carRagDate'] = carRegDate
            item['mileage'] = mileage

            if '110100' in city:
                item['city'] = '北京'
            elif '310100' in city:
                item['city'] = '上海'
            elif '440100' in city:
                item['city'] = '广州'
            elif '510100' in city:
                item['city'] = '成都'

            item['salePrice'] = salePrice
            item['normalMinPrice'] = normalMinPrice
            item['normalMaxPrice'] = normalMaxPrice
            item['betterMinPrice'] = betterMinPrice
            item['betterMaxPrice'] = betterMaxPrice
            item['bestMinPrice'] = bestMinPrice
            item['bestMaxPrice'] = bestMaxPrice
            item['status'] = vehicle_id + '-' + city + '-' + carRegDate + '-' + str(self.now_year) + str(self.now_month)
            # print(item)
            yield item
