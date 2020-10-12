# -*- coding: utf-8 -*-
import time

import scrapy


class DiyiqicheSpider(scrapy.Spider):
    name = 'diyidiandong'
    allowed_domains = ['touchev.com']

    # start_urls = ['http://touchev.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(DiyiqicheSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        # 'MYSQL_SERVER': '192.168.1.94',
        # 'MYSQL_DB': 'chexiu',
        # 'MYSQL_TABLE': 'chexiu',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'gonggao',
        'MONGODB_COLLECTION': 'diyidiandong',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        url_list = ['http://biz.touchev.com/industry_notice?cat=taxfree_fev&group=all&keyword=&page=all',
                    'http://biz.touchev.com/industry_notice?cat=taxfree_hev&group=all&keyword=&page=all',
                    'http://biz.touchev.com/industry_notice?cat=taxfree_bev&group=all&keyword=&page=all']
        for url in url_list:
            yield scrapy.Request(url=url)

    def parse(self, response):
        # print(response.text)
        item = {}
        if 'taxfree_fev' in response.url:
            category = '燃料电池'
            trs = response.xpath('//tbody/tr[@class]')
            for tr in trs:
                data = tr.xpath('.//td/text()').getall()
                # print(data)
                batch = data[0]
                serial_number = data[1]
                company = data[2]
                type = data[3]
                vehicle_model = data[4]
                name = data[5]
                mileage = data[6]
                car_quality = data[7]
                battery_quality = data[8]
                battery_energy = data[9]
                try:
                    remarks = data[10]
                except:
                    remarks = ' '
                item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['category'] = category
                item['batch'] = batch
                item['serial_number'] = serial_number
                item['company'] = company
                item['type'] = type
                item['vehicle_model'] = vehicle_model
                item['name'] = name
                item['mileage'] = mileage
                item['car_quality'] = car_quality
                item['battery_quality'] = battery_quality
                item['battery_energy'] = battery_energy
                item['remarks'] = remarks
                item['url'] = response.url
                item['status'] = category + batch + serial_number + vehicle_model + name
                yield item
        elif 'taxfree_hev' in response.url:
            category = '插电式混合动力'
            trs = response.xpath('//tbody/tr[@class]')
            for tr in trs:
                data = tr.xpath('.//td/text()').getall()
                batch = data[0]
                serial_number = data[1]
                company = data[2]
                type = data[3]
                vehicle_model = data[4]
                name = data[5]
                mileage = data[6]
                fuel_consumption = data[7]
                engine_displacement = data[8]
                car_quality = data[9]
                battery_quality = data[10]
                try:
                    battery_energy = data[11]
                except:
                    battery_energy = ''
                try:
                    remarks = data[12]
                except:
                    remarks = ' '
                item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['category'] = category
                item['batch'] = batch
                item['serial_number'] = serial_number
                item['company'] = company
                item['type'] = type
                item['vehicle_model'] = vehicle_model
                item['name'] = name
                item['mileage'] = mileage
                item['fuel_consumption'] = fuel_consumption
                item['engine_displacement'] = engine_displacement
                item['car_quality'] = car_quality
                item['battery_quality'] = battery_quality
                item['battery_energy'] = battery_energy
                item['remarks'] = remarks
                item['url'] = response.url
                item['status'] = category + batch + serial_number + vehicle_model + name
                yield item
        elif 'taxfree_bev' in response.url:
            category = '纯电动'
            trs = response.xpath('//tbody/tr[@class]')
            for tr in trs:
                data = tr.xpath('.//td/text()').getall()
                batch = data[0]
                serial_number = data[1]
                company = data[2]
                type = data[3]
                vehicle_model = data[4]
                name = data[5]
                mileage = data[6]
                car_quality = data[7]
                battery_quality = data[8]
                try:
                    battery_energy = data[9]
                except:
                    battery_energy = ' '
                try:
                    remarks = data[10]
                except:
                    remarks = ' '
                item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['category'] = category
                item['batch'] = batch
                item['serial_number'] = serial_number
                item['company'] = company
                item['type'] = type
                item['vehicle_model'] = vehicle_model
                item['name'] = name
                item['mileage'] = mileage
                item['car_quality'] = car_quality
                item['battery_quality'] = battery_quality
                item['battery_energy'] = battery_energy
                item['remarks'] = remarks
                item['url'] = response.url
                item['status'] = category + batch + serial_number + vehicle_model + name
                yield item
