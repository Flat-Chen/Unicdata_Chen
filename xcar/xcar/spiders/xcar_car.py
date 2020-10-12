import json
import time

import scrapy


class XcarGzCarSpider(scrapy.Spider):
    name = 'xcar_car'
    allowed_domains = ['xcar.com.cn']
    start_urls = ['https://a.xcar.com.cn/carsel/pbrand?type=1&used=1']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(XcarGzCarSpider, self).__init__(**kwargs)
        self.carnum = 1000000
        self.counts = 0
        self.headers = {}

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'xcar',
        'MONGODB_COLLECTION': 'xcar_car',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def parse(self, response):
        json_data = json.loads(response.text)
        # print(json_data)
        for i in json_data['data']:
            for j in json_data['data'][i]:
                brand = json_data['data'][i][j]['pbname']
                brand_id = j
                # print(brand, brand_id)
                family_url = f'https://a.xcar.com.cn/carsel/pserise?pbid={brand_id}&type=1&used=1'
                yield scrapy.Request(url=family_url, callback=self.family_parse, meta={'info': (brand, brand_id)})

    def family_parse(self, response):
        brand, brand_id = response.meta.get('info')
        json_data = json.loads(response.text)
        # print(json_data)
        for b in json_data['data']:
            bid = b['bid']
            bname = b['bname']
            pslist = b['pslist']
            for family in pslist:
                familyname = family['psname']
                family_id = family['pserid']
                # print(brand, brand_id, bname, bid, familyname, family_id)
                makeyear_url = f'https://a.xcar.com.cn/used/getListYearModel?pserid={family_id}&used=1'
                yield scrapy.Request(url=makeyear_url, callback=self.makeyear_parse,
                                     meta={'info': (brand, brand_id, bname, bid, familyname, family_id)})

    def makeyear_parse(self, response):
        brand, brand_id, bname, bid, familyname, family_id = response.meta.get('info')
        # print(response.text)
        json_data = json.loads(response.text)
        makeyears = json_data['syear']
        for makeyear in makeyears:
            vehicle_url = f'https://a.xcar.com.cn/used/getListYearModel?pserid={family_id}&year={makeyear}&used=1'
            yield scrapy.Request(url=vehicle_url, callback=self.vehicle_parse,
                                 meta={'info': (brand, brand_id, bname, bid, familyname, family_id, makeyear)})

    def vehicle_parse(self, response):
        brand, brand_id, bname, bid, familyname, family_id, makeyear = response.meta.get('info')
        json_data = json.loads(response.text)
        # print(json_data)
        vehicle_list = json_data['list']
        item = {}
        for i in vehicle_list:
            vehicle_id = i['mid']
            vehicle = i['mname']
            # print(brand, brand_id, bname, bid, familyname, family_id, makeyear, vehicle, vehicle_id)
            item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['brand'] = brand
            item['brand_id'] = brand_id
            item['factory'] = bname
            item['factory_id'] = bid
            item['familyname'] = familyname
            item['family_id'] = family_id
            item['makeyear'] = makeyear
            item['vehicle'] = str(makeyear) + '-' + vehicle
            item['vehicle_id'] = vehicle_id
            item['status'] = str(brand_id) + '-' + str(bid) + '-' + str(family_id) + '-' + str(vehicle_id)
            yield item
