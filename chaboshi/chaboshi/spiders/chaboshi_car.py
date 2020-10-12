import json
import time
from urllib.parse import urlencode
import scrapy


class ChaboshiCarSpider(scrapy.Spider):
    name = 'chaboshi_car'
    allowed_domains = ['chaboshi.cn']

    # start_urls = ['https://app.chaboshi.cn/app/brandModel/getBrands']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(ChaboshiCarSpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.2.149',
        'MYSQL_DB': 'chaboshi',
        'MYSQL_TABLE': 'chaboshi',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'chaboshi',
        'MONGODB_COLLECTION': 'chaboshi_car',
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        brand_url = 'https://app.chaboshi.cn/app/brandModel/getBrands'
        yield scrapy.Request(url=brand_url, method='POST')

    def parse(self, response):
        brand_json = json.loads(response.text)
        brandlist = brand_json['data']['data']
        for brands in brandlist:
            brand = brands['brandName']
            brand_id = brands['id']
            brand_pinyin = brands['brandNamePinyin']
            family_url = 'https://app.chaboshi.cn/app/brandModel/getSeries'
            yield scrapy.Request(url=family_url, method='POST', body=urlencode({'supportbrandid': brand_id}),
                                 callback=self.family_parse, meta={'info': (brand, brand_id, brand_pinyin)})

    def family_parse(self, response):
        brand, brand_id, brand_pinyin = response.meta.get('info')
        family_json = json.loads(response.text)
        factorylist = family_json['data']['data']
        for factory in factorylist:
            familyname = factorylist[factory][0]['series']
            family_id = factorylist[factory][0]['id']
            vehicle_url = 'https://app.chaboshi.cn/app/brandModel/getModelsValuationAble'
            yield scrapy.Request(url=vehicle_url, method='POST', body=urlencode({'supportseriesid': family_id}),
                                 callback=self.vehicle_parse,
                                 meta={'info': (brand, brand_id, brand_pinyin, factory, familyname, family_id)})

    def vehicle_parse(self, response):
        item = {}
        brand, brand_id, brand_pinyin, factory, familyname, family_id = response.meta.get('info')
        if '该车系下暂无车型' in response.text:
            pass
        else:
            vehicle_json = json.loads(response.text)
            yearlist = vehicle_json['data']['data']
            for year in yearlist:
                for vehicles in yearlist[year]:
                    vehicle = vehicles['model']
                    vehicle_id = vehicles['id']
                    try:
                        brand_58_id = vehicles['brand58Id']
                        family_58_id = vehicles['series58Id']
                        vehicle_58_id = vehicles['model58Id']
                    except:
                        brand_58_id = None
                        family_58_id = None
                        vehicle_58_id = None

                    sellprice = vehicles['sellPrice']
                    try:
                        level = vehicles['levelName']
                    except:
                        level = None
                    maxRegYear = vehicles['maxRegYear']
                    minRegYear = vehicles['minRegYear']
                    # print(brand, brand_pinyin, brand_id, brand_58_id, factory, familyname, family_id, family_58_id, year,
                    #       vehicle, vehicle_id, vehicle_58_id, sellprice, level, maxRegYear, minRegYear)
                    item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    item['brand'] = brand
                    item['brand_pinyin'] = brand_pinyin
                    item['brand_id'] = brand_id
                    item['brand_58_id'] = brand_58_id
                    item['factory'] = factory
                    item['familyname'] = familyname
                    item['family_id'] = family_id
                    item['family_58_id'] = family_58_id
                    item['year'] = year
                    item['vehicle'] = vehicle
                    item['vehicle_id'] = vehicle_id
                    item['vehicle_58_id'] = vehicle_58_id
                    item['sellprice'] = sellprice
                    item['level'] = level
                    item['maxRegYear'] = maxRegYear
                    item['minRegYear'] = minRegYear
                    item['url'] = 'post - ' + response.url
                    item['status'] = str(vehicle_id) + str(vehicle_58_id) + str(year) + str(vehicle)
                    yield item
