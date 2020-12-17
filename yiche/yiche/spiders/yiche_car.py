# -*- coding: utf-8 -*-
import json
import re
import time
from urllib.parse import unquote

import scrapy


class YicheCarSpider(scrapy.Spider):
    name = 'yiche_car'
    allowed_domains = ['bitauto.com']
    start_urls = ['http://car.bitauto.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(YicheCarSpider, self).__init__(**kwargs)
        self.carnum = 1000000
        self.counts = 0
        self.headers = {}

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'yiche',
        'MONGODB_COLLECTION': 'yiche_car',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def parse(self, response):
        brand_list = response.xpath('//div[@class="brand-list"]//div[@class="item-brand"]')
        for i in brand_list:
            brand = i.xpath('.//div[@class="brand-name"]/@data-name').extract_first()
            brand_id = i.xpath('.//div[@class="brand-name"]/@data-id').extract_first()
            brand_url = f'http://car.bitauto.com/xuanchegongju/?mid={brand_id}'
            # print(brand, brand_id)
            yield scrapy.Request(url=brand_url, callback=self.brand_parse,
                                 meta={"info": (brand_id, brand)})
            break

    def brand_parse(self, response):
        brand_id, brand = response.meta.get('info')
        family_list = response.xpath('//div[@class="search-result-list-item"]')
        for i in family_list:
            familyname = i.xpath('.//p[@class="cx-name text-hover"]/text()').extract_first()
            family_id = i.xpath('./@data-id').extract_first()

            family_url = response.urljoin(i.xpath('.//a[@target="_blank"]/@href').extract_first())

            yield scrapy.Request(url=family_url, callback=self.family_parse,
                                 meta={"info": (brand_id, brand, family_id, familyname)})

        next_url = response.xpath('//a[@class="link-btn next pg-item"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.brand_parse,
                                 meta={"info": (brand_id, brand)})

    def family_parse(self, response):
        brand_id, brand, family_id, familyname = response.meta.get('info')
        text = re.findall(r'carListConditionData: "(.*?)",', response.text)[0]
        text = unquote(text)
        print(text)
        vehicle_ids = re.findall(r'"id":\s*(\d+),', text, re.S)
        # for vehicle_id in vehicle_ids:
        #     print(vehicle_id)
    #         # vehicle_url = 'http://car.bitauto.com/quanxinaodia4l/m124251/peizhi/'
    #         vehicle_url = response.urljoin(f'm{vehicle_id}/peizhi/')
    #         yield scrapy.Request(url=vehicle_url, callback=self.vehicle_parse,
    #                              meta={'info': (brand_id, brand, family_id, familyname, vehicle_id)})
    # #
    # def vehicle_parse(self, response):
    #     item = {}
    #     brand_id, brand, family_id, familyname, vehicle_id = response.meta.get('info')
    #     text = re.findall(r'var carCompareJson = \[(.*?)var optionalPackageJson', response.text, re.S)[0]
    #     vehicle_info = text.replace(',[[', ',[[[[').split(',[[')[0][1:-1].replace('],[', ']],[[').split('],[')
    #     vehicle = vehicle_info[0][1:-1].split(',')[1].replace("'", "").replace('"', '')
    #     makeyear = vehicle_info[0][1:-1].split(',')[7].replace("'", "").replace('"', '')
    #     guide_price = vehicle_info[1][1:-1].split(',')[0].replace("'", "").replace('"', '')
    #     power_type = vehicle_info[1][1:-1].split(',')[-1].replace("'", "").replace('"', '')
    #     if '电' in power_type:
    #         displacement = vehicle_info[3][1:-1].split(',')[0].replace("'", "").replace('"', '')
    #         maximum_cruising_range = vehicle_info[3][1:-1].split(',')[-9].replace("'", "").replace('"', '')
    #     else:
    #         displacement = vehicle_info[3][1:-1].split(',')[0].replace("'", "").replace('"', '')
    #         maximum_cruising_range = None
    #     engine = vehicle_info[1][1:-1].split(',')[4].replace("'", "").replace('"', '') + '-' + \
    #              vehicle_info[1][1:-1].split(',')[5].replace("'", "").replace('"', '')
    #     gearbox = vehicle_info[1][1:-1].split(',')[8].replace("'", "").replace('"', '')
    #     environmental_standards = vehicle_info[3][1:-1].split(',')[19].replace("'", "").replace('"', '')
    #     number_of_seats = vehicle_info[2][1:-1].split(',')[5].replace("'", "").replace('"', '')
    #     drive_way = vehicle_info[4][1:-1].split(',')[0].replace("'", "").replace('"', '')
    #
    #     item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     item['brand_id'] = brand_id
    #     item['brand'] = brand
    #     item['family_id'] = family_id
    #     item['familyname'] = familyname
    #     item['vehicle_id'] = vehicle_id
    #     item['vehicle'] = str(makeyear) + ' ' + vehicle
    #     item['makeyear'] = makeyear
    #     item['guide_price'] = guide_price
    #     item['power_type'] = power_type
    #     item['engine'] = engine
    #     item['gearbox'] = gearbox
    #     item['environmental_standards'] = environmental_standards
    #     item['number_of_seats'] = number_of_seats
    #     item['displacement'] = displacement
    #     item['drive_way'] = drive_way
    #     item['maximum_cruising_range'] = maximum_cruising_range
    #     item['url'] = response.url
    #     item['status'] = str(vehicle_info)
    #     # yield item
    #     print(item)
