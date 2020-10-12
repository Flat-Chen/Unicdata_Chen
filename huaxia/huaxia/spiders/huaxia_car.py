# -*- coding: utf-8 -*-
import json
import time

import scrapy


class HuaxiaCarSpider(scrapy.Spider):
    name = 'huaxia_car'
    allowed_domains = ['hx2car.com']
    start_urls = ['http://www.hx2car.com/tools/carassess.htm']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(HuaxiaCarSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'chexiu',
        'MYSQL_TABLE': 'chexiu',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'huaxia',
        'MONGODB_COLLECTION': 'huaxia_car',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def parse(self, response):
        divs = response.xpath('//ul[@class="brand"]//div')
        for div in divs:
            brand_id = ''.join(div.xpath('./@id').extract()).strip()
            brandname = ''.join(div.xpath('./text()').extract()).strip()
            # print(brand_id, brandname)
            url = 'http://www.hx2car.com/mobile/appMatchRequire/getCarSerialByParentIdJson.json'
            data = {'pids': str(brand_id)}
            yield scrapy.FormRequest(url=url, formdata=data, callback=self.family_parse,
                                     meta={"info": (brand_id, brandname)})

    def family_parse(self, response):
        brand_id, brandname = response.meta.get('info')
        data = response.text
        json_data = json.loads(data)
        # print(json_data["sonCarSerials"])
        # print('*' * 100)
        for factor in json_data["sonCarSerials"]:
            factorname = factor
            for family in json_data["sonCarSerials"][factor]:
                family_id = family['id']
                familyname = family['title']
                # print(factorname, family_name, family_id)
                url = 'http://www.hx2car.com/car/getCarTypeByParentIdJson.json'
                data = {'parentId': str(family_id)}
                yield scrapy.FormRequest(url=url, formdata=data, callback=self.vehicle_parse,
                                         meta={"info": (brand_id, brandname, family_id, familyname, factorname)})

    def vehicle_parse(self, response):
        item = {}
        brand_id, brandname, family_id, familyname, factoryname = response.meta.get('info')
        data = response.text
        json_data = json.loads(data)
        for map in json_data['maps']:
            for value in map['value']:
                vehicle = value['subject']
                vehicle_id = value['id']
                years = value['years']
                displacement = value['title']
                guideprice = value['prices']
                # print(vehicle, vehicle_id, years, displacement, guideprice)
                item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['brandname'] = brandname
                item['brand_id'] = brand_id
                item['factoryname'] = factoryname
                item['family_id'] = family_id
                item['famliyname'] = familyname
                item['vehicle'] = vehicle
                item['vehicle_id'] = vehicle_id
                item['years'] = years
                item['displacement'] = displacement
                item['guideprice'] = guideprice
                item['url'] = response.url + str(vehicle_id)
                item['status'] = item['url'] + str(guideprice)
                yield item
