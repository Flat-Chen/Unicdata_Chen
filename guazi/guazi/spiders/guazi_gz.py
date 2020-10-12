# -*- coding: utf-8 -*-
import json
import time
from _datetime import datetime

import pymongo
import scrapy
from pandas import DataFrame

connection = pymongo.MongoClient('192.168.2.149', 27017)
db = connection["guazi"]
collection = db["guazi_car"]
model_data = collection.find({}, {"vehicle_id": 1, "years": 1, "_id": 0})

car_msg_list = list(model_data)
car_msg_df = DataFrame(car_msg_list)
car_msg_df_new = car_msg_df.drop_duplicates('vehicle_id')


class GuaziGujiaSpider(scrapy.Spider):
    name = 'guazi_gz'
    allowed_domains = ['guazi.com']
    # start_urls = ['http://guazi.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(GuaziGujiaSpider, self).__init__(**kwargs)
        self.counts = 0
        self.car_msg_df_new = car_msg_df_new

    is_debug = True
    custom_debug_settings = {
        # 'MYSQL_SERVER': '192.168.1.94',
        # 'MYSQL_DB': 'chexiu',
        # 'MYSQL_TABLE': 'chexiu',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'guazi',
        'MONGODB_COLLECTION': 'guazi_gz',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        localyears = int(datetime.now().year)
        localmonth = int(datetime.now().month)
        citys = ['12', '13', '16', '45']
        for areaCode in citys:
            for index, rows in self.car_msg_df_new.iterrows():
                vehicle_id = rows['vehicle_id']
                try:
                    years = int(rows['years'])
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
                            mile = 0.1
                            url = f'https://marketing.guazi.com/marketing/evaluate/wapCarEvaluateDirectInfo?cityId={areaCode}&carId={vehicle_id}&licenseYear={year}&licenseMonth={month}&roadHaul={mile}'
                            yield scrapy.Request(url=url, meta={"info": (vehicle_id, year, month, mile, areaCode)})

                        else:
                            month = localmonth
                            mile = (localyears - year) * 2
                            url = f'https://marketing.guazi.com/marketing/evaluate/wapCarEvaluateDirectInfo?cityId={areaCode}&carId={vehicle_id}&licenseYear={year}&licenseMonth={month}&roadHaul={mile}'
                            yield scrapy.Request(url=url, meta={"info": (vehicle_id, year, month, mile, areaCode)})
                else:
                    year = localyears
                    month = localmonth - 1
                    mile = 0.1
                    url = f'https://marketing.guazi.com/marketing/evaluate/wapCarEvaluateDirectInfo?cityId={areaCode}&carId={vehicle_id}&licenseYear={year}&licenseMonth={month}&roadHaul={mile}'
                    yield scrapy.Request(url=url, meta={"info": (vehicle_id, year, month, mile, areaCode)})

    def parse(self, response):
        item = {}
        vehicle_id, year, month, mile, areaCode = response.meta.get('info')
        data = response.text
        json_data = json.loads(data)
        levelA_dealerLowBuyPrice = json_data['data']['assessData']['levelA']['dealerLowBuyPrice']
        levelA_individualHighSoldPrice = json_data['data']['assessData']['levelA']['individualHighSoldPrice']
        levelA_individualLowSoldPrice = json_data['data']['assessData']['levelA']['individualLowSoldPrice']

        levelB_dealerLowBuyPrice = json_data['data']['assessData']['levelB']['dealerLowBuyPrice']
        levelB_individualHighSoldPrice = json_data['data']['assessData']['levelB']['individualHighSoldPrice']
        levelB_individualLowSoldPrice = json_data['data']['assessData']['levelB']['individualLowSoldPrice']

        levelC_dealerLowBuyPrice = json_data['data']['assessData']['levelC']['dealerLowBuyPrice']
        levelC_individualHighSoldPrice = json_data['data']['assessData']['levelC']['individualHighSoldPrice']
        levelC_individualLowSoldPrice = json_data['data']['assessData']['levelC']['individualLowSoldPrice']

        item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['vehicle_id'] = vehicle_id
        item['ragDate'] = str(year) + '-' + str(month)
        item['mile'] = mile
        if '12' in areaCode:
            item['city'] = '北京'
        elif '13' in areaCode:
            item['city'] = '上海'
        elif '16' in areaCode:
            item['city'] = '广州'
        elif '45' in areaCode:
            item['city'] = '成都'
        item['levelA_dealerLowBuyPrice'] = levelA_dealerLowBuyPrice
        item['levelA_individualHighSoldPrice'] = levelA_individualHighSoldPrice
        item['levelA_individualLowSoldPrice'] = levelA_individualLowSoldPrice

        item['levelB_dealerLowBuyPrice'] = levelB_dealerLowBuyPrice
        item['levelB_individualHighSoldPrice'] = levelB_individualHighSoldPrice
        item['levelB_individualLowSoldPrice'] = levelB_individualLowSoldPrice

        item['levelC_dealerLowBuyPrice'] = levelC_dealerLowBuyPrice
        item['levelC_individualHighSoldPrice'] = levelC_individualHighSoldPrice
        item['levelC_individualLowSoldPrice'] = levelC_individualLowSoldPrice

        item['url'] = response.url
        item['status'] = str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(
            areaCode) + '-' + response.url
        print(item)
        yield item
