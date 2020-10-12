import scrapy
import re
import time
from urllib.parse import unquote


class YicheGuanzhuSpider(scrapy.Spider):
    name = 'yiche_guanzhu'
    allowed_domains = ['bitauto.com']
    start_urls = ['http://car.bitauto.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(YicheGuanzhuSpider, self).__init__(**kwargs)
        self.carnum = 1000000
        self.counts = 0
        self.headers = {}

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'yiche',
        'MONGODB_COLLECTION': 'yiche_guanzhu',
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
            yield scrapy.Request(url=brand_url, callback=self.brand_parse,
                                 meta={"info": (brand_id, brand)})

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
        item = {}
        brand_id, brand, family_id, familyname = response.meta.get('info')
        text = re.findall(r'carListConditionData: "(.*?)",', response.text)[0].replace('id', 'idid')
        text = unquote(text)
        car_list = re.findall(r'"id(.*?),"tranAndGearNum":', text)
        for car in car_list:
            year = re.search(r',"year":(.*?),"saleStatus', car).group(1)
            vehicle_id = re.search(r'id":(.*?),"name', car).group(1)
            vehicle = re.search(r',"name":"(.*?)","year"', car).group(1)
            vehiclename = str(year) + '-' + vehicle
            guanzhu = re.search(r'"pvPercent":"(.*?)","hasImageFlag"', car).group(1)

            item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['brand_id'] = brand_id
            item['brand'] = brand
            item['family_id'] = family_id
            item['familyname'] = familyname
            item['vehicle_id'] = vehicle_id
            item['vehiclename'] = vehiclename
            item['guanzhu'] = guanzhu
            item['url'] = response.url
            item['info'] = car
            item['status'] = vehiclename + '-' + str(vehicle_id) + '-' + str(guanzhu)
            yield item
