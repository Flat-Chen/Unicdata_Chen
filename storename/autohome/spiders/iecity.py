# -*- coding: utf-8 -*-
import scrapy
from autohome.items import A1688Item
import time


class IecitySpider(scrapy.Spider):
    name = 'iecity'
    allowed_domains = ['iecity.com']
    start_urls = ['http://iecity.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(IecitySpider, self).__init__(**kwargs)

        self.carnum = 1000000

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'shop_name',
        'MONGODB_COLLECTION': 'tuhu',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        for i in range(1, 4):
            url = 'http://www.iecity.com/shanghai/brand/181121_{}.html'.format(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        lis = response.xpath('//li[@class="clearfix"]')
        for li in lis:
            shop_url = li.xpath('.//div[@class="clearfix"]/h3/a/@href').extract_first()
            yield scrapy.Request(url=shop_url, callback=self.shop_parse)

    def shop_parse(self, response):
        # print(response.text)
        company = response.xpath('//div[@id="Title"]/h1/text()').extract_first()
        region = response.xpath('//span[@itemprop="addressLocality"]/text()').extract_first()
        address = response.xpath('//span[@itemprop="streetAddress"]/text()').extract_first()
        phone = response.xpath('//span[@itemprop="telephone"]/text()').extract_first()
        update_time = response.xpath('//time[@datetime]/span/text()').extract_first()
        city = '上海'
        status = response.url + company
        grabtime = time.strftime('%Y-%m-%d %X', time.localtime())
        item = A1688Item(grabtime=grabtime, company=company,
                         city=city, region=region, address=address, phone=phone, status=status)
        yield item
        # print(company, region, address, phone, update_time)
