# -*- coding: utf-8 -*-
import time
from datetime import datetime
import pymongo
import scrapy
from pandas import DataFrame

connection = pymongo.MongoClient('192.168.2.149', 27017)
db = connection["huaxia"]
collection = db["huaxia_car"]
model_data = collection.find({},
                             {"brand_id": 1, "brandname": 1, "family_id": 1, "famliyname": 1, "vehicle": 1,
                              "vehicle_id": 1, "years": 1, "_id": 0})

car_msg_list = list(model_data)
car_msg_df = DataFrame(car_msg_list)
car_msg_df_new = car_msg_df.drop_duplicates('vehicle_id')


class HuaxiaGuzhiSpider(scrapy.Spider):
    name = 'huaxia_guzhi'
    allowed_domains = ['hx2car.com']

    # start_urls = [
    #     f'http://www.hx2car.com/tools/assessDetail.htm?serialOne={brand_id}&year={year}&month={month}&mile={mile}&areaCode={areaCode}&serid={famliy_id}&keyword={brandname},{famliyname},{vehicle}&carType={vehicle_id}']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(HuaxiaGuzhiSpider, self).__init__(**kwargs)
        self.counts = 0
        self.car_msg_df_new = car_msg_df_new

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'chexiu',
        'MYSQL_TABLE': 'chexiu',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'huaxia',
        'MONGODB_COLLECTION': 'huaxia_guzhi',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        for index, rows in self.car_msg_df_new.iterrows():
            brand_id = rows['brand_id']
            brandname = rows['brandname']
            family_id = rows['family_id']
            familyname = rows['famliyname']
            vehicle = rows['vehicle']
            vehicle_id = rows['vehicle_id']
            years = int(rows['years'])
            if years == 0:
                pass
            else:
                # print(index, brand_id, brandname, family_id, familyname, vehicle, vehicle_id, years)
                localyears = int(datetime.now().year)
                localmonth = int(datetime.now().month)
                areaCodes = ['110100', '310100', '440100', '510100']
                for year in range(years - 1, localyears + 1):
                    if year == localyears:
                        month = localmonth - 1
                        mile = '0.1'
                    else:
                        month = localmonth
                        mile = (localyears - year) * 2
                    for areaCode in areaCodes:
                        url = f'http://www.hx2car.com/tools/assessDetail.htm?serialOne={brand_id}&year={year}&month={month}&mile={mile}&areaCode={areaCode}&serid={family_id}&keyword={brandname},{familyname},{vehicle}&carType={vehicle_id}'
                        yield scrapy.Request(url=url, meta={"info": (vehicle_id, year, month, mile, areaCode)})

    def parse(self, response):
        vehicle_id, year, month, mile, areaCode = response.meta.get('info')
        try:
            item = {}
            item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['vehicle_id'] = vehicle_id
            item['year'] = year
            item['month'] = month
            item['mile'] = mile
            if areaCode is '110100':
                item['city'] = '北京'
            elif areaCode is '310100':
                item['city'] = '上海'
            elif areaCode is '440100':
                item['city'] = '广州'
            elif areaCode is '510100':
                item['city'] = '成都'
            price = response.xpath('//span[@class="ass_num_key"]//text()').extract()
            item['purchasing_price'] = price[0]
            item['Individual_transaction_price'] = price[1]
            item['retail_price'] = price[2]
            newcar_price = response.xpath('//span[@class="ass_num_key not"]//text()').extract_first()
            item['newcar_price'] = newcar_price
            item['url'] = response.url
            item['status'] = response.url + '-' + price[0] + '-' + price[1] + '-' + price[2] + '-' + newcar_price
            yield item
        except:
            pass
