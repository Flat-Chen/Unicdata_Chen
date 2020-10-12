# -*- coding: utf-8 -*-
import datetime
import json
import time

import scrapy


class TaocheCarSpider(scrapy.Spider):
    name = 'taoche_car'
    allowed_domains = ['taoche.com']
    start_urls = ['https://pg.taoche.com/ajax/carinfojs.ashx?']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(TaocheCarSpider, self).__init__(**kwargs)
        self.counts = 0
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
        'MONGODB_COLLECTION': 'taoche_car',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def parse(self, response):
        car_list = response.text.split(' ')[2:]
        for car in car_list:
            car_ = car.split(',')
            brandname = car_[0]
            brand_id = car_[1]
            # print(brandname, brand_id)
            brand_url = 'https://pg.taoche.com/ajax/carinfojs.ashx?carbrandid={}&'.format(brand_id)
            yield scrapy.Request(url=brand_url, callback=self.brand_parse,
                                 meta={"info": (brand_id, brandname)})

    def brand_parse(self, response):
        brand_id, brandname = response.meta.get('info')
        car_list = response.text.split('=')[1][1:-1].split("', '")[0].replace(',{', ',{{').split(',{')
        for car in car_list:
            car = car.replace("'", '')
            car = json.loads(car)
            factoryname = car['GroupName']
            familyname = car['Text']
            family_id = car['Value']
            # print(GroupName, Text, Value)
            family_url = 'https://pg.taoche.com/ajax/carinfojs.ashx?carserialid={}'.format(family_id)
            yield scrapy.Request(url=family_url, callback=self.family_parse,
                                 meta={"info": (brand_id, brandname, factoryname, familyname, family_id)})

    def family_parse(self, response):
        global carRegDate, mileage
        brand_id, brandname, factoryname, familyname, family_id = response.meta.get('info')
        vehicle_list = response.text.split('=')[1][1:-1].replace(',{', ',{{').split(',{')
        for car in vehicle_list:
            car = json.loads(car)
            GroupName = car['GroupName']
            Text = car['Text']
            vehicle_id = car['Value']
            vehicle = GroupName + '-' + Text
            makeyear = int(GroupName.split(' ')[0])
            item = {}
            item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['brandname'] = brandname
            item['brand_id'] = brand_id
            item['familyname'] = familyname
            item['family_id'] = family_id
            item['factoryname'] = factoryname
            item['vehicle'] = vehicle
            item['vehicle_id'] = vehicle_id

            item['makeyear'] = makeyear
            item['url'] = response.url
            item['status'] = vehicle_id + str(self.now_year) + str(self.now_month)
            yield item

    #         if self.now_year > makeyear:
    #             if self.now_year - makeyear >= 4:
    #                 year_list = [i for i in range(makeyear, makeyear + 4)]
    #             else:
    #                 year_list = [i for i in range(makeyear, self.now_year + 1)]
    #             for year in year_list:
    #                 if year == self.now_year:
    #                     month = self.now_month - 1
    #                     month = f"0{str(month)}" if month < 10 else month
    #                     carRegDate = f'{year}-{month}-01'
    #                     mileage = 0.1
    #                 else:
    #                     month = f"0{str(self.now_month)}" if self.now_month < 10 else self.now_month
    #                     carRegDate = f'{year}-{month}-01'
    #                     mileage = (self.now_year - year) * 2
    #         else:
    #             month = self.now_month - 1
    #             month = f"0{str(month)}" if month < 10 else month
    #             carRegDate = f'{self.now_year}-{month}-01'
    #             mileage = 0.1
    #
    #         vehicle_url = 'https://proconsumer.taoche.com/c-carsource-consumer/carsource/get-car-eval'
    #         city_list = ['110100', '310100', '440100', '510100']
    #         for city in city_list:
    #             data = {
    #                 'carRegDate': carRegDate,
    #                 'cityId': city,
    #                 'mileage': mileage,
    #                 'terminal': 30,
    #                 'vehicleModelId': vehicle_id,
    #             }
    #             data = json.dumps(data)
    #             yield scrapy.Request(url=vehicle_url, method='POST', body=data, headers=self.headers,
    #                                  callback=self.vehicle_parse,
    #                                  meta={"info": (
    #                                      brand_id, brandname, factoryname, familyname, family_id, vehicle_id, vehicle,
    #                                      makeyear, carRegDate, city, mileage)})
    #
    # def vehicle_parse(self, response):
    #     brand_id, brandname, factoryname, familyname, family_id, vehicle_id, vehicle, makeyear, carRegDate, city, mileage = response.meta.get(
    #         'info')
    #     if '"normalMinPrice":0.0' in response.text:
    #         pass
    #     else:
    #         data = response.text
    #         json_data = json.loads(data)
    #         salePrice = json_data['data']['salePrice']
    #         normalMinPrice = json_data['data']['normalMinPrice']
    #         normalMaxPrice = json_data['data']['normalMaxPrice']
    #         betterMinPrice = json_data['data']['betterMinPrice']
    #         betterMaxPrice = json_data['data']['betterMaxPrice']
    #         bestMinPrice = json_data['data']['bestMinPrice']
    #         bestMaxPrice = json_data['data']['bestMaxPrice']
    #
    #         item = {}
    #         item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #         item['brandname'] = brandname
    #         item['brand_id'] = brand_id
    #         item['familyname'] = familyname
    #         item['family_id'] = family_id
    #         item['factoryname'] = factoryname
    #         item['vehicle'] = vehicle
    #         item['vehicle_id'] = vehicle_id
    #
    #         item['makeyear'] = makeyear
    #         item['carRagDate'] = carRegDate
    #         item['mileage'] = mileage
    #         item['city'] = city
    #
    #         item['salePrice'] = salePrice
    #         item['normalMinPrice'] = normalMinPrice
    #         item['normalMaxPrice'] = normalMaxPrice
    #         item['betterMinPrice'] = betterMinPrice
    #         item['betterMaxPrice'] = betterMaxPrice
    #         item['bestMinPrice'] = bestMinPrice
    #         item['bestMaxPrice'] = betterMaxPrice
    #         item['status'] = vehicle + str(city) + str(normalMinPrice) + str(normalMaxPrice) + str(
    #             betterMaxPrice) + str(betterMinPrice) + str(bestMinPrice) + str(bestMaxPrice)
    #         yield item
