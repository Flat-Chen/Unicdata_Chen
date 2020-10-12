import json
import random
import time
from _datetime import datetime
from urllib.parse import urlencode

import pymongo
import scrapy
from pandas import DataFrame

connection = pymongo.MongoClient('192.168.2.149', 27017)
db = connection["xcar"]
collection = db["xcar_car"]
model_data = collection.find({}, {"vehicle_id": 1, "makeyear": 1, "_id": 0})

car_msg_list = list(model_data)
car_msg_df = DataFrame(car_msg_list)
car_msg_df_new = car_msg_df.drop_duplicates('vehicle_id')


# 随机生成一个手机号
def phoneNORandomGenerator():
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153",
               "155", "156", "157", "158", "159", "186", "187", "188"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))


class XcarGzSpider(scrapy.Spider):
    name = 'xcar_gz'
    allowed_domains = ['xcar.com.cn']

    # start_urls = ['http://xcar.com.cn/']
    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(XcarGzSpider, self).__init__(**kwargs)
        self.counts = 0
        self.car_msg_df_new = car_msg_df_new
        self.city_list = [{'province': '1', 'city_id': '475', 'city_name': '%e5%8c%97%e4%ba%ac%e5%b8%82'},
                          {'province': '2', 'city_id': '507', 'city_name': '上海市'},
                          {'province': '30', 'city_id': '347', 'city_name': '广州市'},
                          {'province': '17', 'city_id': '386', 'city_name': '成都市'}]

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'xcar',
        'MONGODB_COLLECTION': 'xcar_gz',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        localyears = int(datetime.now().year)
        localmonth = int(datetime.now().month)
        url = 'https://a.xcar.com.cn/nxcar/index.php/userdcar/carassess/assessSub'
        for city_dict in self.city_list:
            province = city_dict['province']
            city_id = city_dict['city_id']
            city_name = city_dict['city_name']
            for index, rows in self.car_msg_df_new.iterrows():
                vehicle_id = rows['vehicle_id']
                makeyear = int(rows['makeyear'])
                if localyears > makeyear:
                    if localyears - makeyear >= 4:
                        year_list = [i for i in range(makeyear, makeyear + 4)]
                    else:
                        year_list = [i for i in range(makeyear, localyears + 1)]
                    for year in year_list:
                        if year == localyears:
                            month = localmonth - 1
                            # month = f"0{str(month)}" if month < 10 else month
                            mile = '0_1'
                            regDate = str(year) + '-' + str(month) + '-' + '1'
                            data = {
                                'mid': vehicle_id,
                                'province_id': province,
                                'city_id': city_id,
                                'city_name': city_name,
                                'card_time': regDate,
                                'mileage': mile,
                                'mobile': phoneNORandomGenerator()
                            }
                            data = json.dumps(data)
                            print(data)
                            yield scrapy.Request(url=url, method='POST', body=data,
                                                 meta={"info": (vehicle_id, regDate, mile, city_name)})
                        else:
                            month = localmonth
                            # month = f"0{str(month)}" if month < 10 else month
                            mile = (localyears - year) * 2
                            regDate = str(year) + '-' + str(month) + '-' + '1'
                            data = {
                                'mid': vehicle_id,
                                'province_id': province,
                                'city_id': city_id,
                                'city_name': city_name,
                                'card_time': regDate,
                                'mileage': mile,
                                'mobile': phoneNORandomGenerator()
                            }
                            data = json.dumps(data)
                            print(data)
                            yield scrapy.Request(url=url, method='POST', body=data,
                                                 meta={"info": (vehicle_id, regDate, mile, city_name)})
                else:
                    year = localyears
                    month = localmonth - 1
                    # month = f"0{str(month)}" if month < 10 else month
                    regDate = str(year) + '-' + str(month) + '-' + '1'
                    mile = '0_1'
                    data = {
                        'mid': vehicle_id,
                        'province_id': province,
                        'city_id': city_id,
                        'city_name': city_name,
                        'card_time': regDate,
                        'mileage': mile,
                        'mobile': phoneNORandomGenerator()
                    }
                    data = json.dumps(data)
                    print(data)
                    yield scrapy.Request(url=url, method='POST', body=data,
                                         meta={"info": (vehicle_id, regDate, mile, city_name)})
                break
            break

    def parse(self, response):
        json_data = json.loads(response.text)
        print(json_data)
