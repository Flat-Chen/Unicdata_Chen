# -*- coding: utf-8 -*-
import datetime
import json
import time

import scrapy


class A58CarSpider(scrapy.Spider):
    name = '58_car'
    allowed_domains = ['58.com']
    start_urls = ['https://carprice.58.com/comm/brand.json']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(A58CarSpider, self).__init__(**kwargs)
        self.counts = 0
        self.now_year = datetime.datetime.now().year
        self.now_month = datetime.datetime.now().month

    is_debug = True
    custom_debug_settings = {
        # 'MYSQL_SERVER': '192.168.1.94',
        # 'MYSQL_DB': 'taoche',
        # 'MYSQL_TABLE': 'taoche',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': '58tc',
        'MONGODB_COLLECTION': '58_car',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def parse(self, response):
        data = response.text
        json_data = json.loads(data)
        for i in json_data:
            if i['zimu'] in '热门':
                pass
            else:
                for brands in i['brandList']:
                    brandname = brands['text']
                    brand_id = brands['value']
                    # print(brandname,brand_id)

                    # 奥迪测试
                    # brand_id = 408844
                    # brandname = '奥迪'
                    brand_url = f'https://carprice.58.com/comm/chexi.json?cityid=1&vid={brand_id}&&key={brandname}'
                    yield scrapy.Request(url=brand_url, callback=self.brand_parse, meta={'info': (brand_id, brandname)})

    def brand_parse(self, response):
        brand_id, brandname = response.meta.get('info')
        data = response.text
        json_data = json.loads(data)
        for family in json_data:
            familyname = family['text']
            family_id = family['value']
            # print(familyname,family_id)
            # 奥迪A4L测试
            # familyname = '奥迪A4L'
            # family_id = 409012
            family_url = f'https://carprice.58.com/comm/model.json?cityid=1&vid={family_id}&&key={familyname}'
            yield scrapy.Request(url=family_url, callback=self.family_parse,
                                 meta={'info': (brand_id, brandname, family_id, familyname)})

    def family_parse(self, response):
        brand_id, brandname, family_id, familyname = response.meta.get('info')
        data = response.text
        json_data = json.loads(data)
        for i in json_data:
            year = i['year']
            for vehicles in i['modelList']:
                vehicle = vehicles['shortText']
                vehicle_id = vehicles['modelid']
                order = vehicles['order']
                guide_price = vehicles['priceText'].split('：')[1]
                # print(brandname, familyname, vehicle, year, vehicle_id, guide_price, order)
                item = {}
                item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['brand_id'] = brand_id
                item['brandname'] = brandname
                item['family_id'] = family_id
                item['family_name'] = familyname
                item['vehicle_id'] = vehicle_id
                item['vehicle'] = vehicle
                item['year'] = year
                item['guide_price'] = guide_price
                item['order'] = order
                item['url'] = response.url
                item['status'] = brand_id + '-' + family_id + '-' + vehicle_id + '-' + vehicle + year
                yield item
