import json
import time
from _datetime import datetime
from urllib.parse import urlencode

import pymongo
import scrapy
from pandas import DataFrame

connection = pymongo.MongoClient('192.168.2.149', 27017)
db = connection["chaboshi"]
collection = db["chaboshi_car"]
model_data = collection.find({}, {"vehicle_id": 1, "maxRegYear": 1, "minRegYear": 1, "_id": 0})

car_msg_list = list(model_data)
car_msg_df = DataFrame(car_msg_list)
car_msg_df_new = car_msg_df.drop_duplicates('vehicle_id')


class ChaboshiGzSpider(scrapy.Spider):
    name = 'chaboshi_gz'
    allowed_domains = ['chaboshi.cn']

    # start_urls = ['http://chaboshi.cn/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(ChaboshiGzSpider, self).__init__(**kwargs)
        self.counts = 0
        self.car_msg_df_new = car_msg_df_new
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
        'MONGODB_COLLECTION': 'chaboshi_gz',
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        localyears = int(datetime.now().year)
        localmonth = int(datetime.now().month)
        city_list = ['735', '970', '797', '757']  # 北京 上海 广州 成都
        for index, rows in self.car_msg_df_new.iterrows():
            vehicle_id = rows['vehicle_id']
            maxRegYear = rows['maxRegYear']
            minRegYear = rows['minRegYear']
            for regYear in range(minRegYear, maxRegYear + 1):
                if regYear >= localyears:
                    regMonth = localmonth - 1
                    mile = 0.1
                else:
                    regMonth = localmonth
                    mile = (localyears - regYear) * 2
                regDate = str(regYear) + '-' + str(regMonth)
                for city in city_list:
                    url = 'https://app.chaboshi.cn/app/assess/freeSubmit'
                    data = {
                        'carModelId': vehicle_id,
                        'drivedMiles': mile,
                        'cityId': city,
                        'source': 'android',
                        'plateTime': regDate
                    }
                    yield scrapy.Request(url=url, method='POST', body=urlencode(data),
                                         meta={'info': (vehicle_id, regDate, city, mile)})


    def parse(self, response):
        vehicle_id, regDate, city, mile = response.meta.get('info')
        if '估价成功' in response.text:
            token = json.loads(response.text)['data']['fakeOrderNo']
            gz_url = f'https://app.chaboshi.cn/wap/getFreeAssessReport?fakeOrderNo={token}'
            yield scrapy.Request(url=gz_url, callback=self.parse_gz, meta={'info': (vehicle_id, regDate, city, mile)})

    def parse_gz(self, response):
        item = {}
        localyears = str(datetime.now().year)
        localmonth = str(datetime.now().month)
        vehicle_id, regDate, city, mile = response.meta.get('info')
        gudie_price = response.xpath('//div[@class="price"]/label[1]/span/text()').extract_first().strip()
        local_price = response.xpath('//div[@class="price"]/label[2]/span/text()').extract_first().strip()
        gz_3price = response.xpath('//li[@class="profitCol"]/text()').getall()
        price_normal = gz_3price[0].strip()
        price_good = gz_3price[1].strip()
        price_excellent = gz_3price[2].strip()
        gz_4price = response.xpath('//div[@class="carSupply"]/span/text()').getall()
        price_1 = gz_4price[0]
        price_2 = gz_4price[1]
        price_3 = gz_4price[2]
        price_4 = gz_4price[3]

        # print(gudie_price, local_price, price_normal, price_good, price_excellent, price_1, price_2, price_3, price_4)
        item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['vehicle_id'] = str(vehicle_id)
        item['regDate'] = regDate
        item['mile'] = mile
        if city in '735':
            item['city'] = '北京'
        elif city in '970':
            item['city'] = '上海'
        elif city in '797':
            item['city'] = '广州'
        elif city in '757':
            item['city'] = '成都'
        item['gudie_price'] = gudie_price
        item['local_price'] = local_price
        item['price_normal'] = price_normal
        item['price_good'] = price_good
        item['price_excellent'] = price_excellent
        item['price_1'] = price_1
        item['price_2'] = price_2
        item['price_3'] = price_3
        item['price_4'] = price_4
        item['url'] = response.url
        item['status'] = localyears + '-' + localmonth + '-' + response.url
        # yield item
        print(item)
