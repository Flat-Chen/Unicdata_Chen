# -*- coding: utf-8 -*-
import json
import time

import scrapy


class GuaziCarSpider(scrapy.Spider):
    name = 'guazi_car'
    allowed_domains = ['guazi.com']
    start_urls = ['https://marketing.guazi.com/marketing/brand/haveTags/all?cityId=12&size=14']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(GuaziCarSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'chexiu',
        'MYSQL_TABLE': 'chexiu',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'guazi',
        'MONGODB_COLLECTION': 'guazi_car',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def parse(self, response):
        data = response.text
        json_data = json.loads(data)
        for i in json_data['data']['brands']:
            for brand in json_data['data']['brands'][i]:
                # print(brand)
                brand_id = brand['id']
                brandname = brand['name']
                for family in brand['tags']:
                    family_id = family['id']
                    familyname = family['name']
                    # print(brandname, brand_id, familyname, family_id)
                    url = f'https://api.guazi.com/clientUc/brand/type?seriesId={family_id}'
                    yield scrapy.Request(url=url, callback=self.vehicle_parse,
                                         meta={"info": (brand_id, brandname, family_id, familyname)})


    def vehicle_parse(self, response):
        brand_id, brandname, family_id, familyname = response.meta.get('info')
        item = {}
        data = response.text
        json_data = json.loads(data)
        for data in json_data['data']:
            years = data
            for value in json_data['data'][data]:
                vehicle_id = value['id']
                vehicle = value['name']
                transmission = value['bian_su_qi']
                emission_standard = value['pai_fang_biao_zhun']
                seats = value['seats']
                item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['brandname'] = brandname
                item['brand_id'] = brand_id
                item['famliyname'] = familyname
                item['family_id'] = family_id
                item['vehicle'] = vehicle
                item['vehicle_id'] = vehicle_id
                item['years'] = years
                item['transmission'] = transmission
                item['emission_standard'] = emission_standard
                item['seats'] = seats
                item['url'] = response.url + str(vehicle_id)
                item['status'] = item['url'] + '-' + str(vehicle_id) + '-' + str(vehicle)
                print(item)
