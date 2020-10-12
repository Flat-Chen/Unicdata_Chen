# -*- coding: utf-8 -*-
import json
import time

import scrapy


class DasoucheCarSpider(scrapy.Spider):
    name = 'dasouche_car'
    allowed_domains = ['souche.com']
    start_urls = ['https://erp.souche.com/pc/car/carModelV2Action/queryBrand.jsonp?callback=__jp0']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(DasoucheCarSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'dasouche',
        'MYSQL_TABLE': 'dasouche_car',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'dasouche',
        'MONGODB_COLLECTION': 'dasouche_car',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def parse(self, response):
        data = response.text[6:].replace(');', '')
        json_data = json.loads(data)
        for brands in json_data['data']['brands']:
            brandname = brands['brandName']
            brand_id = brands['brandCode'][6:]
            country = brands['country']
            # print(brandname, brand_id, country)
            # brand_id = 15  # 奥迪
            url = f'http://erp.souche.com/pc/car/carModelV2Action/querySeriesByBrand.jsonp?brandCode=brand-{brand_id}&callback=__jp1'
            yield scrapy.Request(url=url, callback=self.brand_parse, meta={'info': (brand_id, brandname, country)})

    def brand_parse(self, response):
        brand_id, brandname, country = response.meta.get('info')
        data = response.text[6:].replace(');', '')
        json_data = json.loads(data)
        # print(json_data)
        for familys in json_data['data']['series']:
            familyname = familys['seriesName']
            family_id = familys['seriesCode'][7:]
            factory = familys['manufacturer']
            level = familys['level']
            # family_id = 621  # A4L
            # print(familyname, family_id, factory, level)
            url = f'https://erp.souche.com/pc/car/carModelV2Action/queryModelBySeries.jsonp?seriesCode=series-{family_id}&callback=__jp2'
            yield scrapy.Request(url=url, callback=self.family_parse,
                                 meta={'info': (brand_id, brandname, country, familyname, family_id, factory, level)})

    def family_parse(self, response):
        item = {}
        brand_id, brandname, country, familyname, family_id, factory, level = response.meta.get('info')
        data = response.text[6:].replace(');', '')
        json_data = json.loads(data)
        for vehicles in json_data['data']['models']:
            vehicle = vehicles['modelName']
            vehicle_id = vehicles['modelCode']
            year = vehicles['year']
            try:
                guidePrice = vehicles['guidePrice']
            except KeyError:
                guidePrice = '无'
            item['grantime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['brand_id'] = brand_id
            item['brandname'] = brandname
            item['country'] = country
            item['family_id'] = family_id
            item['family_name'] = familyname
            item['factory'] = factory
            item['level'] = level
            item['vehicle_id'] = vehicle_id
            item['vehicle'] = vehicle
            item['year'] = year
            item['guideprice'] = guidePrice
            item['url'] = response.url
            item['status'] = brand_id + '-' + family_id + '-' + vehicle_id + '-' + vehicle
            yield item
