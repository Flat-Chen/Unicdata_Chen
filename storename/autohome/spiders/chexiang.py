# -*- coding: utf-8 -*-
import scrapy


class ChexiangSpider(scrapy.Spider):
    name = 'chexiang'
    allowed_domains = ['chexiang.com']

    # start_urls = ['http://chexiang.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(ChexiangSpider, self).__init__(**kwargs)

        self.carnum = 1000000

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'StoreName',
        'MONGODB_COLLECTION': 'chexiang',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Referer': 'https://jia.chexiang.com/t/stores.htm',
            'X-Requested-With': 'XMLHttpRequest'
        }
        url = 'https://jia.chexiang.com/store/queryStoreByXY.htm'
        data = {'D': "", 'X': '31.230416', 'Y': '121.473701', 'areaCode': "310100"}
        yield scrapy.FormRequest(url=url, formdata=data, headers=headers, callback=self.parse)

    def parse(self, response):
        print(response)
