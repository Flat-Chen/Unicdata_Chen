import re
import time

import scrapy


class Nantong16888Spider(scrapy.Spider):
    name = 'nantong_16888'
    allowed_domains = ['16888.com']
    start_urls = ['http://dealer.16888.com/?tag=search&pid=16&cid=226&nature=1']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(Nantong16888Spider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': "192.168.1.94",
        'MYSQL_USER': "dataUser94",
        'MYSQL_PWD': "94dataUser@2020",
        'MYSQL_PORT': 3306,
        'MYSQL_DB': "",
        'MYSQL_TABLE': "",
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'shop_name',
        'MONGODB_COLLECTION': 'nantong_16888',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def parse(self, response):
        dls = response.xpath('//div[@class="dealer-box"]/dl')
        for dl in dls:
            store_name = dl.xpath('.//div[@class="title"]/a/text()').extract_first()
            main_business = ','.join(dl.xpath('.//div[@class="camp"]/p//text()').extract()) \
                .replace('\n', '').replace('\r', '').replace(' ', '').split(',')
            main_business = list(filter(None, main_business))
            main_business = ','.join(main_business)
            phone = dl.xpath('.//div[@class="camp clearfix"][1]/em/text()').extract_first()
            address = dl.xpath('.//div[@class="camp clearfix"][2]/p/text()').extract_first()
            map_url = dl.xpath('.//div[@class="camp clearfix"][2]/p/a/@href').extract_first()
            yield scrapy.Request(url=map_url, meta={'info': (store_name, main_business, phone, address, map_url)},
                                 callback=self.map_coordinate)
            # break
            # print(store_name, main_business, phone, address, map_url)

        next_url = response.xpath('//div[@class="mod-pagination"]/a[@class="next"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse)

    def map_coordinate(self, response):
        item = {}
        store_name, main_business, phone, address, map_url = response.meta.get('info')
        zuobiao = re.findall(r'Latitude="(.*?)";', response.text)[0]
        try:
            zuobiao = zuobiao.split(',')
            longitude = zuobiao[0]
            latitude = zuobiao[1]
        except:
            longitude = None
            latitude = None
        grabtime = time.strftime('%Y-%m-%d %X', time.localtime())
        item['grabtime'] = grabtime
        item['store_name'] = store_name
        item['main_business'] = main_business
        item['phone'] = phone
        item['address'] = address
        item['longitude'] = longitude
        item['latitude'] = latitude
        item['map_url'] = map_url
        item['status'] = store_name + main_business + map_url
        yield item
