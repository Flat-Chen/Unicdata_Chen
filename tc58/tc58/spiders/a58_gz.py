# -*- coding: utf-8 -*-
import time

import pymongo
import scrapy
from pandas import DataFrame
from _datetime import datetime

settings = {
    "MONGODB_SERVER": "192.168.2.149",
    "MONGODB_PORT": 27017,
    "MONGODB_DB": "58tc",
    "MONGODB_COLLECTION": "58_car",
}
uri = f'mongodb://{settings["MONGODB_SERVER"]}:{settings["MONGODB_PORT"]}/'

connection = pymongo.MongoClient(uri)
db = connection[settings['MONGODB_DB']]
collection = db[settings['MONGODB_COLLECTION']]
model_data = collection.find({}, {"vehicle_id": 1, "year": 1, "_id": 0})

car_msg_list = list(model_data)
car_msg_df = DataFrame(car_msg_list)
car_msg_df_new = car_msg_df.drop_duplicates('vehicle_id')


class A58GzSpider(scrapy.Spider):
    name = '58_gz'
    allowed_domains = ['58.com']
    start_urls = ['http://58.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(A58GzSpider, self).__init__(**kwargs)
        self.counts = 0
        self.car_msg_df_new = car_msg_df_new
        self.localyears = int(datetime.now().year)
        self.localmonth = int(datetime.now().month)

    is_debug = True
    custom_debug_settings = {
        # 'MYSQL_SERVER': '192.168.1.94',
        # 'MYSQL_DB': 'chexiu',
        # 'MYSQL_TABLE': 'chexiu',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': '58tc',
        'MONGODB_COLLECTION': '58_gz',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        localyears = self.localyears
        localmonth = self.localmonth
        citys = ['1', '2', '3', '102']

        for city in citys:
            for index, rows in self.car_msg_df_new.iterrows():
                try:
                    vehicle_id = rows['vehicle_id']
                    years = int(rows['year'][:-1])
                except:
                    continue
                if localyears > years:
                    if localyears - years >= 4:
                        year_list = [i for i in range(years, years + 4)]
                    else:
                        year_list = [i for i in range(years, localyears + 1)]
                    for year in year_list:
                        if year == localyears:
                            month = localmonth - 1
                            month = f"0{str(month)}" if month < 10 else month
                            mile = '0_1'
                            regDate = str(year) + str(month)
                            url = f'https://carprice.58.com/m{vehicle_id}/d{regDate}m{mile}c{city}.html'
                            yield scrapy.Request(url=url, meta={"info": (vehicle_id, regDate, mile, city), 'url': url})
                        else:
                            month = localmonth
                            month = f"0{str(month)}" if month < 10 else month
                            mile = (localyears - year) * 2
                            regDate = str(year) + str(month)
                            url = f'https://carprice.58.com/m{vehicle_id}/d{regDate}m{mile}c{city}.html'
                            yield scrapy.Request(url=url, meta={"info": (vehicle_id, regDate, mile, city), 'url': url})
                else:
                    year = localyears
                    month = localmonth - 1
                    month = f"0{str(month)}" if month < 10 else month
                    regDate = str(year) + str(month)
                    mile = '0_1'
                    url = f'https://carprice.58.com/m{vehicle_id}/d{regDate}m{mile}c{city}.html'
                    yield scrapy.Request(url=url, meta={"info": (vehicle_id, regDate, mile, city), 'url': url})

    def parse(self, response):
        vehicle_id, regDate, mile, city = response.meta.get('info')
        # 检测是否有验证码 出现验证码则重新请求该网页
        if 'antibot' in response.url:
            url = response.meta.get('url')
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta={"info": (vehicle_id, regDate, mile, city), 'url': url})
            # print('出现验证码，重新请求网页', vehicle_id, regDate, city)
        else:
            item = {}
            # vehicle_id, regDate, mile, city = response.meta.get('info')
            gz = response.xpath('//span[@id="pinggujiage"]/text()').extract_first()
            gz1 = gz.split('-')
            low_price = gz1[0]
            high_price = gz1[1][:-1]
            item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['vehicle_id'] = vehicle_id
            item['regDate'] = regDate
            if isinstance(mile, str):
                item['mile'] = 0.1
            else:
                item['mile'] = mile
            if '1' is city:
                item['city'] = '北京'
            elif '2' is city:
                item['city'] = '上海'
            elif '3' is city:
                item['city'] = '广州'
            elif '102' is city:
                item['city'] = '成都'
            item['low_price'] = low_price
            item['high_price'] = high_price
            item['url'] = response.url
            item['status'] = response.url + '-' + str(self.localyears) + str(self.localmonth) + '-' + gz
            print(item)
            # yield item
