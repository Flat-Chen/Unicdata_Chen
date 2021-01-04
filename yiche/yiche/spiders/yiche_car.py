# -*- coding: utf-8 -*-
import hashlib
import json
import re
import time
import urllib
from urllib.parse import unquote, quote

import scrapy


class YicheCarSpider(scrapy.Spider):
    name = 'yiche_car'
    allowed_domains = ['bitauto.com']

    # start_urls = ['http://car.m.yiche.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(YicheCarSpider, self).__init__(**kwargs)
        self.web_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
        self.wap_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
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

    def start_requests(self):
        yield scrapy.Request(url='http://car.m.yiche.com/', headers=self.wap_headers)

    def parse(self, response):
        dls = response.xpath('//dl[@class="brand-item"]//dd')
        for dl in dls:
            brand = dl.xpath('.//p[@class="brand-name"]/text()').extract_first()
            brand_id = dl.xpath('./a/@data-id').extract_first()
            brand_url = dl.xpath('./a/@href').extract_first()
            yield scrapy.Request(url='http://car.yiche.com' + brand_url, headers=self.web_headers,
                                 callback=self.family_id,
                                 meta={"info": (brand_id, brand, brand_url)}, dont_filter=True)
            break

    def family_id(self, response):
        brand_id, brand, brand_url = response.meta.get('info')
        family_id_item = {}
        family_text = re.findall(r'var carList =(.*?);', response.text)[0]
        family_json = json.loads(family_text)
        for i in family_json['onAndWaitList'] + family_json['unAndStopList']:
            for j in i['serialList']:
                family_id_item[j['allSpell']] = j['id']
        yield scrapy.Request(url='http://car.m.yiche.com' + brand_url, headers=self.wap_headers,
                             callback=self.brand_parse,
                             meta={"info": (brand_id, brand, family_id_item)}, dont_filter=True)

    def brand_parse(self, response):
        brand_id, brand, family_id_item = response.meta.get('info')
        on_sale = response.xpath('//div[@class="tab-wrap-cell-wrap"]/div[@class="tab-wrap-cell"][1]/'
                                 'div[@class="brand-list"]//div[@class="brand-item"]')
        dis_sale = response.xpath('//div[@class="tab-wrap"]/div[@class="brand-list"]//div[@class="brand-item"]')
        for brand_item in on_sale + dis_sale:
            factory = brand_item.xpath('./div[@class="brand-name"]/text()').extract_first()
            for i in brand_item.xpath('./div[@class="brand-car"]//a'):
                family_url = i.xpath('./@href').extract_first()
                family_name = i.xpath('.//div[@class="car-name"]/text()').extract_first(). \
                    replace(' ', '').replace('\n', '')
                family_id = family_id_item[family_url.strip('/')]
                yield scrapy.Request(url='http://car.yiche.com' + family_url, headers=self.web_headers,
                                     callback=self.family_parse,
                                     meta={"info": (brand, brand_id, factory, family_name, family_id)},
                                     dont_filter=True)
                break
            break

    def family_parse(self, response):
        brand, brand_id, factory, family_name, family_id = response.meta.get('info')
        text = re.findall(r'carListConditionData: "(.*?)",', response.text)[0]
        text = unquote(text)
        vehicle_ids = re.findall(r'"id":\s*(\d+),', text, re.S)
        for vehicle_id in vehicle_ids:
            vehicle_id = '144693'
            # print(vehicle_id)
            # param = str({"cityId": 2401, "carId": int(vehicle_id)})
            # print(param)
            vehicle_url = 'http://car.yiche.com/web_api/car_model_api/api/v1/car/config_new_param?cid=508&param={"cityId":2401,"carId":"' + vehicle_id + '"}'

            timestamp = int(time.time() * 1000)
            sign = hashlib.md5((
                        'cid=508&param={"cityId":2401,"carId":"' + vehicle_id + '"}19DDD1FBDFF065D3A4DA777D2D7A81EC' + str(
                    timestamp)).encode(
                'utf-8')).hexdigest()
            headers = {
                'Host': 'car.yiche.com',
                'x-city-id': '201',
                'x-platform': 'pc',
                'x-sign': sign,
                'x-timestamp': timestamp,
            }
            print(unquote(vehicle_url))
            print(sign)
            print(timestamp)
            yield scrapy.Request(url=vehicle_url, callback=self.vehicle_parse, headers=headers,
                                 meta={'info': (brand_id, brand, family_id, family_name, vehicle_id, factory)},
                                 dont_filter=True)
            break

    def vehicle_parse(self, response):
        item = {}
        brand_id, brand, family_id, family_name, vehicle_id, factory = response.meta.get('info')
        print(response.text)
        # text = re.findall(r'var carCompareJson = \[(.*?)var optionalPackageJson', response.text, re.S)[0]
        # vehicle_info = text.replace(',[[', ',[[[[').split(',[[')[0][1:-1].replace('],[', ']],[[').split('],[')
        # print(vehicle_info)
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
