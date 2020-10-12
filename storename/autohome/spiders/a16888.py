# -*- coding: utf-8 -*-
import time

import scrapy
from autohome.items import A1688Item


class A16888Spider(scrapy.Spider):
    name = 'a16888'
    allowed_domains = ['16888.com']
    start_urls = ['https://dealer.16888.com/?tag=search&nature=1']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(A16888Spider, self).__init__(**kwargs)

        self.carnum = 1000000

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'a1688',
        'MONGODB_COLLECTION': 'a1688',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        for i in range(1, 1581):
            url = 'https://dealer.16888.com/?tag=search&nature=1&page={}'.format(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        dls = response.xpath('//dl[@class="clearfix hover "]')
        for dl in dls:
            grabtime = time.strftime('%Y-%m-%d %X', time.localtime())
            company = dl.xpath('.//div[@class="title"]/a/text()').extract_first()
            level = dl.xpath('.//div[@class="title"]/b/text()').extract_first().strip()
            on_sale = dl.xpath('.//div[@class="title"]/span/em/text()').extract_first()
            major_businesses = dl.xpath('.//div[@class="camp"]/p//a//text()').getall()
            city = dl.xpath('.//div[@class="dealer-city"]/p[1]/text()').extract_first()
            region = dl.xpath('.//div[@class="dealer-city"]/p[2]/text()').extract_first()
            address = dl.xpath('.//div[@class="camp clearfix"][2]/p/text()').extract_first()
            phone = dl.xpath('//div[@class="camp clearfix"][1]/em/text()').extract_first()
            status = response.url + company
            # print(company, level, on_sale, major_businesses, city, region, address, phone)
            item = A1688Item(grabtime=grabtime, company=company, level=level, on_sale=on_sale,
                             major_businesses=major_businesses,
                             city=city, region=region, address=address, phone=phone, status=status)
            yield item
