# -*- coding: utf-8 -*-
import scrapy
import time
import json
import pymongo
import pandas as pd
import datetime
import pymysql
import re

from autohome.items import AutohomeGzItem

settings = {
    "MONGODB_SERVER": "192.168.1.94",
    "MONGODB_PORT": 27017,
    "MONGODB_DB": "newcar",
    "MONGODB_COLLECTION": "autohome_new_id",
}
uri = f'mongodb://{settings["MONGODB_SERVER"]}:{settings["MONGODB_PORT"]}/'

connection = pymongo.MongoClient(uri)
db = connection[settings['MONGODB_DB']]
collection = db[settings['MONGODB_COLLECTION']]


def readMysqlaly(sql):
    dbconn = pymysql.connect(
        host="192.168.1.94",
        database='people_zb',
        user="dataUser94",
        password="94dataUser@2020",
        port=3306,
        charset='utf8')
    sqlcmd = sql
    df = pd.read_sql(sqlcmd, dbconn)
    return df


# sql = "select cityid, provid from che168_need_city"
# 全国所有城市
# df_data = readMysqlaly(sql)
# city_list = df_data["cityid"].values
# prov_list = df_data["provid"].values
# city_dic = dict(zip(city_list, prov_list))


# 四个城市 北京 上海 广州 成都
city_dic = {'110100': '110000', '310100': '310000', '440100': '440000', '510100': '510000'}
# print(city_dic)


class AutohomeUrlSpider(scrapy.Spider):
    name = 'autohome_url'
    allowed_domains = ['che168.com']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeUrlSpider, self).__init__(**kwargs)
        self.counts = 0
        self.data = pd.DataFrame(
            list(collection.find({}, {'brandid': 1, 'familyid': 1, 'autohomeid': 1, 'makeyear': 1})))
        del self.data["_id"]
        self.data['makeyear'] = self.data['makeyear'].astype('int')
        self.now_year = datetime.datetime.now().year
        now_month = datetime.datetime.now().month
        self.now_month = f"0{str(now_month)}" if now_month < 10 else now_month
        # self.city_dic = {'340000': '340100', '110000': '110100', '500000': '500100', '350000': '350100',
        #                  '440000': '440100', '450000': '450100', '520000': '520100', '620000': '620100',
        #                  '460000': '460100', '410000': '410100', '420000': '420100', '430000': '430100',
        #                  '130000': '130100', '230000': '230100', '320000': '320100', '360000': '360100',
        #                  '220000': '220100', '640000': '640100', '630000': '630100', '610000': '610100',
        #                  '310000': '310100', '370000': '370100', '120000': '120100', '650000': '650100',
        #                  '540000': '540100', '530000': '530100', '330000': '330100'}
        # self.city_name = {'110100': '北京', '120100': '成都', '130100': '石家庄', '220100': '长春',
        #                   '230100': '哈尔滨', '310100': '西宁', '320100': '南京', '330100': '天津', '340100': '合肥',
        #                   '350100': '福州', '360100': '南昌', '370100': '西安', '410100': '郑州', '420100': '武汉',
        #                   '430100': '长沙', '440100': '广州',
        #                   '450100': '南宁', '460100': '海口', '500100': '重庆', '520100': '贵阳', '530100': '济南',
        #                   '540100': '太原', '610100': '银川', '620100': '兰州', '630100': '呼和浩特', '640100': '沈阳',
        #                   '650100': '上海'}
        # self.city_dic = {'650000': '650100'}
        # self.city_name = {'650100': '上海'}

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }
        self.buy_type_list = {'2.07v': '买保障车', '2.08v': '买商家车', '2.09v': '买个人车'}
        self.sale_type_list = {'2.04v': '卖给商家', '2.03v': '4S置换', '2.09v': '卖给个人'}

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'residual_value',
        'MYSQL_TABLE': 'autohome_gz',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'residual_value',
        'MONGODB_COLLECTION': 'autohome_gz',
        'CrawlCar_Num': 800000,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'COOKIES_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            # 'carbuisness.rotate_useragent.RotateUserAgentMiddleware': 543,  #543
            # 'carbuisness_new.middlewares.SeleniumMiddleware': 400,
            # 'carbuisness.middlewares.MyproxiesSpiderMiddleware':None,
            # 'carbuisness_new.middlewares.MyproxiesSpiderMiddleware': 301,
            # 'carbuisness_new.middlewares.ProxyMiddleware': 300,
            # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
        },
        'ITEM_PIPELINES': {
            # 'carbuisness_new.pipelines.CarbuisnessNewPipeline': 300,
            'autohome.pipelines.MasterPipeline': 300,
        }

    }

    def start_requests(self):
        url = "https://www.baidu.com/"
        yield scrapy.Request(
            url=url,
            dont_filter=True,
        )

    def parse(self, response):
        for index, rows in self.data.iterrows():
            if rows["makeyear"] < self.now_year:
                if self.now_year - rows["makeyear"] >= 4:
                    year_list = [i for i in range(rows["makeyear"], rows["makeyear"] + 4)]
                else:
                    year_list = [i for i in range(rows["makeyear"], self.now_year + 1)]
                # print(year_list)
                year_dic = {year: (self.now_year - year) * 20000 for year in year_list}
                for k, v in year_dic.items():
                    if v == 0:
                        v = 1000
                    for c, p in city_dic.items():
                        item = AutohomeGzItem()
                        v7_url = f"https://pinguapi.che168.com/v1/auto/usedcarassess.ashx?_appid=pc.pingu&_sign=&encoding=gb2312&pid={p}&cid={c}&mileage={v}&firstregtime={k}-{self.now_month}&specid={rows['autohomeid']}&iscondition=1&mark=&callback=PingGuCallBack3&_appversion=2.07v"
                        item["url"] = v7_url
                        yield item
                        # print(c, p)
                        # print(item)
