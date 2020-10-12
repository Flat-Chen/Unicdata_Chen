# -*- coding: utf-8 -*-
import scrapy
import time

import json

import pymysql
import datetime
from redis import Redis


class JzgPriceMasterSpider(scrapy.Spider):
    name = 'jzg_price_master'

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(JzgPriceMasterSpider, self).__init__(**kwargs)
        self.counts = 0

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
        'MYSQL_DB': 'jzg',
        'MYSQL_TABLE': 'jzg_city',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'jzg',
        'MONGODB_COLLECTION': 'jzg_city',
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
        city_data = dict()
        cities = json.loads(response.text)
        for city in cities["list"]:
            city_data["areaId"] = city["areaId"]
            city_data["areaName"] = city["areaName"]
            city_data["parentAreaId"] = city["parentAreaId"]
            city_data["groupName"] = city["groupName"]
            # print(city_data)
            yield city_data
        # print(final_city_list)
        # data = self.data
        # for model in data:
        #     min_year = int(model["make_year"]) - 1
        #     if int(model["next_year"]) == int(time.strftime('%Y', time.localtime())):
        #         max_year = int(model["next_year"])
        #     elif int(model["next_year"]) == int(time.strftime('%Y', time.localtime())) - 1:
        #         max_year = int(model["next_year"]) + 1
        #     else:
        #         max_year = int(model["next_year"]) + 2
        #     month = datetime.datetime.now().month
        #
        #     for i in range(min_year, max_year+1):
        #         mile = 2 * (int(time.strftime('%Y', time.localtime())) - i)
        #         for c in final_city_list:
        #             if str(i) == str(time.strftime('%Y', time.localtime())):
        #                 month_list = [month-1, month]
        #                 for month in month_list:
        #                     formdata = {
        #                         "sourcetype": "3",
        #                         "regdate": "%s-%s-1" % (str(i), month),
        #                         "cityname": final_city_list[c],
        #                         "CityId": str(c),
        #                         "styleid": str(model["modelid"]),
        #                         "uid": "0",
        #                         "op": "GetValuationInfo",
        #                         "mileage": str(mile * 10000),
        #                         # "sign": "27B900C60B10581444D6F55126074414"
        #                     }
        #                     url_sell = f"http://appraise.jingzhengu.com/sale-s{formdata['styleid']}-r{formdata['regdate']}-m{formdata['mileage']}-c{formdata['CityId']}-y-j-h"
        #                     url_buy = f"http://appraise.jingzhengu.com/buy-s{formdata['styleid']}-r{formdata['regdate']}-m{formdata['mileage']}-c{formdata['CityId']}-y-j-h"
        #                     self.r.lpush('jzg_price:start_urls', url_sell)
        #                     self.r.lpush('jzg_price:start_urls', url_buy)
        #                     print(url_sell)
        #                     print(url_buy)
        #
        #             else:
        #                 formdata = {
        #                     "sourcetype": "3",
        #                     "regdate": "%s-%s-1" % (str(i), month),
        #                     "cityname": final_city_list[c],
        #                     "CityId": str(c),
        #                     "styleid": str(model["modelid"]),
        #                     "uid": "0",
        #                     "op": "GetValuationInfo",
        #                     "mileage": str(mile * 10000),
        #                     # "sign": "27B900C60B10581444D6F55126074414"
        #                 }
        #                 url_sell = f"http://appraise.jingzhengu.com/sale-s{formdata['styleid']}-r{formdata['regdate']}-m{formdata['mileage']}-c{formdata['CityId']}-y-j-h"
        #                 url_buy = f"http://appraise.jingzhengu.com/buy-s{formdata['styleid']}-r{formdata['regdate']}-m{formdata['mileage']}-c{formdata['CityId']}-y-j-h"
        #                 self.r.lpush('jzg_price:start_urls', url_sell)
        #                 self.r.lpush('jzg_price:start_urls', url_buy)
        #                 print(url_sell)
        #                 print(url_buy)
