# -*- coding: utf-8 -*-

import scrapy
import time

import json

import pymysql
import datetime
from redis import Redis

website = 'jzg_price_sh_master'


class JzgPriceShMasterSpider(scrapy.Spider):
    name = website

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(JzgPriceShMasterSpider, self).__init__(**kwargs)
        self.counts = 0
        self.counts = 0
        self.city_count = 0
        # connection = pymongo.MongoClient("192.168.1.94", 27017)
        # db = connection["residual_value"]
        # self.collection = db["jzg_modellist2"]
        self.mysqlconnection = pymysql.connect("192.168.1.94", "root", "Datauser@2017", 'people_zb', 3306)
        dbc = self.mysqlconnection.cursor()
        sql = "select * from jzg_modelid_need"
        dbc.execute(sql)
        res = dbc.fetchall()
        dbc.close()
        modelid_data_list = list()
        for i in res:
            modelid_data = dict()
            modelid_data["modelid"] = i[1]
            modelid_data["make_year"] = i[2]
            modelid_data["next_year"] = i[3]
            modelid_data_list.append(modelid_data)
        self.data = modelid_data_list

        redis_url = 'redis://192.168.1.241:6379/0'
        self.r = Redis.from_url(redis_url, decode_responses=True)

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'residual_value',
        'MYSQL_TABLE': 'jzg_price_sh_master',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'residual_value',
        'MONGODB_COLLECTION': 'jzg_price_sh_master',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        yield scrapy.FormRequest(method="post", url="http://common.jingzhengu.com/area/getProvList", dont_filter=True)

    def parse(self, response):
        provs = json.loads(response.text)
        for prov in provs["list"]:
            yield scrapy.FormRequest(url='http://common.jingzhengu.com/area/getCityListByProvId',
                                     formdata={"provId": str(prov["areaId"])}, callback=self.parse_city)

    def parse_city(self, response):
        # data = self.collection.find()
        data = self.data


        for model in data:
            min_year = int(model["make_year"]) - 1
            if int(model["next_year"]) == int(time.strftime('%Y', time.localtime())):
                max_year = int(model["next_year"])
            elif int(model["next_year"]) == int(time.strftime('%Y', time.localtime())) - 1:
                max_year = int(model["next_year"]) + 1
            else:
                max_year = int(model["next_year"]) + 2
            month = datetime.datetime.now().month
            for i in range(min_year, max_year+1):
                mile = 2 * (int(time.strftime('%Y', time.localtime())) - i)
                # print(mile)
                final_city_list = {"2401": u"上海"}
                for c in final_city_list:
                    if str(i) == str(time.strftime('%Y', time.localtime())):
                        month_list = [month-1, month]
                        print(i)
                        print("*"*100)
                        for month in month_list:
                            mile = 0.1 if mile == 0 else mile
                            mileage = str(mile * 10000).split('.')[0]
                            formdata = {
                                "sourcetype": "3",
                                "regdate": "%s-%s-1" % (str(i), month),
                                "cityname": final_city_list[c],
                                "CityId": str(c),
                                "styleid": str(model["modelid"]),
                                "uid": "0",
                                "op": "GetValuationInfo",
                                "mileage": mileage,
                                # "sign": "27B900C60B10581444D6F55126074414"
                            }
                            url_sell = "http://appraise.jingzhengu.com/sale-s%s-r%s-m%s-c%s-y-j-h" % (
                                formdata['styleid'], formdata['regdate'], formdata['mileage'], formdata['CityId'])
                            url_buy = "http://appraise.jingzhengu.com/buy-s%s-r%s-m%s-c%s-y-j-h" % (
                                formdata['styleid'], formdata['regdate'], formdata['mileage'], formdata['CityId'])
                            self.r.lpush('jzg_price_sh:start_urls', url_sell)
                            self.r.lpush('jzg_price_sh:start_urls', url_buy)
                            print(url_sell)
                            print(url_buy)

                    else:
                        print(i)
                        print("*"*100)
                        formdata = {
                            "sourcetype": "3",
                            "regdate": "%s-%s-1" % (str(i), month),
                            "cityname": final_city_list[c],
                            "CityId": str(c),
                            "styleid": str(model["modelid"]),
                            "uid": "0",
                            "op": "GetValuationInfo",
                            "mileage": str(mile * 10000),
                            # "sign": "27B900C60B10581444D6F55126074414"
                        }

                        url_sell = "http://appraise.jingzhengu.com/sale-s%s-r%s-m%s-c%s-y-j-h" % (
                        formdata['styleid'], formdata['regdate'], formdata['mileage'], formdata['CityId'])
                        url_buy = f"http://appraise.jingzhengu.com/buy-s{formdata['styleid']}-r{formdata['regdate']}-m{formdata['mileage']}-c{formdata['CityId']}-y-j-h"
                        self.r.lpush('jzg_price_sh:start_urls', url_sell)
                        self.r.lpush('jzg_price_sh:start_urls', url_buy)
                        print(url_sell)
                        print(url_buy)




