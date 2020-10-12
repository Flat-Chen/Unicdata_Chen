# -*- coding: utf-8 -*-
import scrapy
import time
import json
import redis
import pymongo
import pandas as pd
import datetime
import re
from scrapy_redis.spiders import RedisSpider

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

pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=0)
con = redis.Redis(connection_pool=pool)


# def readMysqlaly(sql):
#     dbconn = pymysql.connect(
#         host="192.168.1.94",
#         database='people_zb',
#         user="dataUser94",
#         password="94dataUser@2020",
#         port=3306,
#         charset='utf8')
#     sqlcmd = sql
#     df = pd.read_sql(sqlcmd, dbconn)
#     return df
#
#
# sql = "select cityid, provid from che168_need_city"
# df_data = readMysqlaly(sql)
# city_list = df_data["cityid"].values
# prov_list = df_data["provid"].values
#
# city_dic = dict(zip(city_list, prov_list))
# print(city_dic)


class AutohomeGzSpider(RedisSpider):
    name = 'autohome_gz_4city'
    allowed_domains = ['che168.com']
    redis_key = "autohome_gz_4city:start_urls"

    # start_urls = ['http://che168.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeGzSpider, self).__init__(**kwargs)
        self.counts = 0
        # self.data = pd.DataFrame(
        #     list(collection.find({}, {'brandid': 1, 'familyid': 1, 'autohomeid': 1, 'makeyear': 1})))
        # del self.data["_id"]
        # self.data['makeyear'] = self.data['makeyear'].astype('int')
        self.c = con.client()
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

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }
        self.buy_type_list = {'2.07v': '买保障车', '2.08v': '买商家车', '2.09v': '买个人车'}
        self.sale_type_list = {'2.04v': '卖给商家', '2.03v': '4S置换', '2.09v': '卖给个人'}

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.2.149',
        'MYSQL_DB': 'autohome',
        'MYSQL_TABLE': 'autohome_gz',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'autohome',
        'MONGODB_COLLECTION': 'autohome_gz_4city',
        'CrawlCar_Num': 800000,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'DOWNLOAD_TIMEOUT': 10,
        'LOG_LEVEL': 'DEBUG',
        'COOKIES_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            # 'carbuisness.rotate_useragent.RotateUserAgentMiddleware': 543,  #543
            # 'carbuisness_new.middlewares.SeleniumMiddleware': 400,
            # 'carbuisness.middlewares.MyproxiesSpiderMiddleware':None,
            # 'carbuisness_new.middlewares.MyproxiesSpiderMiddleware': 301,
            'autohome.middlewares.ProxyMiddleware': 300,
            # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
        }

    }

    # def start_requests(self):
    #     url = "https://www.che168.com/pinggu/?pvareaid=102140&leadssources=3&sourcetwo=1&sourcethree=342"
    #     # url = "https://www.che168.com/Evaluate/v3/EvaCar.aspx?pgtype=1&pgbid=75&pgsid=831&pgspid=11171&pgyear=2015&pgmonth=12&pgpid=460000&pgcid=460100&pgmlg=8"
    #     yield scrapy.Request(
    #         url=url,
    #         dont_filter=True,
    #     )

    # def start_requests(self):
    #     # city_list = response.xpath("//dl[@class='cap-city']/dd/a[1]/text()").getall()[::-1]
    #     # print(city_list)
    #     # for k, v in self.city_dic.items():
    #     #     self.city_name[v] = city_list.pop()
    #     for index, rows in self.data[:10].iterrows():
    #         if rows["makeyear"] < self.now_year:
    #             year_list = [i for i in range(rows["makeyear"], self.now_year + 1)]
    #             year_dic = {year: (self.now_year - year) * 20000 for year in year_list}
    #             for k, v in year_dic.items():
    #                 if v == 0:
    #                     v = 1000
    #                 for p, c in self.city_dic.items():
    #                     # url = f"https://www.che168.com/Evaluate/v3/EvaCar.aspx?pgtype=1&pgbid={rows['brandid']}&pgsid={rows['familyid']}&pgspid={rows['autohomeid']}&pgyear={k}&pgmonth={self.now_month}&pgpid={p}&pgcid={c}&pgmlg={v}&type=0&buyMark=uahp10003&isfromoutside=0"
    #                     # end = f'&cdatestr={k}{self.now_month}&pvareaid=100567'
    #                     url_info = f"_appid=pc.pingu&_sign=&encoding=gb2312&pid={p}&cid={c}&mileage={v}&firstregtime={k}-{self.now_month}&specid={rows['autohomeid']}&iscondition=1&mark=&callback=PingGuCallBack3"
    #                     v7_url = f"https://pinguapi.che168.com/v1/auto/usedcarassess.ashx?_appid=pc.pingu&_sign=&encoding=gb2312&pid={p}&cid={c}&mileage={v}&firstregtime={k}-{self.now_month}&specid={rows['autohomeid']}&iscondition=1&mark=&callback=PingGuCallBack3&_appversion=2.07v"
    #                     yield scrapy.Request(
    #                         url=v7_url,
    #                         callback=self.parse_v7_price,
    #                         headers=self.headers,
    #                         meta={'url_info': url_info, "autohomeid": rows['autohomeid']}
    #                     )

    # def parse_v7_price(self, resposne):
    def parse(self, resposne):
        # if 'PingGuCallBack3'
        autohomeid = re.findall('specid=(.*?)&iscondition', resposne.url)[0]
        url_info = re.findall('\?(.*?)&_appversion', resposne.url)[0]
        data = json.loads(resposne.text.replace('PingGuCallBack3(', '').replace(')', ''))
        good_list = []
        middle_list = []
        bad_list = []
        url_list = []
        if data["returncode"] == 0:
            data_dic = dict()
            data_dic["买保障车"] = data['result']["conditiona"].split('-')[1]
            good_list.append(data_dic)
            data_dic = dict()
            data_dic["买保障车"] = data['result']["conditionb"].split('-')[1]
            middle_list.append(data_dic)
            data_dic = dict()
            data_dic["买保障车"] = data['result']["conditionc"].split('-')[1]
            bad_list.append(data_dic)
        price_data_info = dict()
        price_data_info["good"] = good_list
        price_data_info["middle"] = middle_list
        price_data_info["bad"] = bad_list
        url_list.append(resposne.url)
        v8_url = f"https://pinguapi.che168.com/v1/auto/usedcarassess.ashx?{url_info}&_appversion=2.08v"
        yield scrapy.Request(
            url=v8_url,
            callback=self.parse_v8_price,
            headers=self.headers,
            meta={'url_info': url_info, "autohomeid": autohomeid, 'price_data_info': price_data_info,
                  'url_list': url_list}
        )

        start_url = self.c.lpop('autohome_gz:start_urls')
        print("*" * 100)
        if start_url:
            start_url = bytes.decode(start_url)
            yield scrapy.Request(
                url=start_url,
                callback=self.parse,
                headers=self.headers,
            )

    def parse_v8_price(self, resposne):
        price_data_info = resposne.meta["price_data_info"]
        url_info = resposne.meta["url_info"]
        autohomeid = resposne.meta["autohomeid"]
        url_list = resposne.meta["url_list"]
        data = json.loads(resposne.text.replace('PingGuCallBack3(', '').replace(')', ''))
        if data["returncode"] == 0:
            price_data_info['good'][0]["买商家车"] = data['result']["conditiona"].split('-')[1]
            price_data_info['middle'][0]["买商家车"] = data['result']["conditionb"].split('-')[1]
            price_data_info['bad'][0]["买商家车"] = data['result']["conditionc"].split('-')[1]
        url_list.append(resposne.url)
        v9_url = f"https://pinguapi.che168.com/v1/auto/usedcarassess.ashx?{url_info}&_appversion=2.09v"
        yield scrapy.Request(
            url=v9_url,
            callback=self.parse_v9_price,
            headers=self.headers,
            meta={'url_info': url_info, "autohomeid": autohomeid, 'price_data_info': price_data_info,
                  'url_list': url_list}
        )

    def parse_v9_price(self, resposne):
        price_data_info = resposne.meta["price_data_info"]
        url_info = resposne.meta["url_info"]
        autohomeid = resposne.meta["autohomeid"]
        url_list = resposne.meta["url_list"]
        data = json.loads(resposne.text.replace('PingGuCallBack3(', '').replace(')', ''))
        if data["returncode"] == 0:
            price_data_info['good'][0]["买个人车"] = data['result']["conditiona"].split('-')[1]
            price_data_info['good'][0]["卖给个人"] = data['result']["conditiona"].split('-')[1]
            price_data_info['middle'][0]["买个人车"] = data['result']["conditionb"].split('-')[1]
            price_data_info['middle'][0]["卖给个人"] = data['result']["conditionb"].split('-')[1]
            price_data_info['bad'][0]["买个人车"] = data['result']["conditionc"].split('-')[1]
            price_data_info['bad'][0]["卖给个人"] = data['result']["conditionc"].split('-')[1]
        # print(price_data_info)
        url_list.append(resposne.url)
        v3_url = f"https://pinguapi.che168.com/v1/auto/usedcarassess.ashx?{url_info}&_appversion=2.03v"
        yield scrapy.Request(
            url=v3_url,
            callback=self.parse_v3_price,
            headers=self.headers,
            meta={'url_info': url_info, "autohomeid": autohomeid, 'price_data_info': price_data_info,
                  'url_list': url_list}
        )

    def parse_v3_price(self, resposne):
        price_data_info = resposne.meta["price_data_info"]
        url_info = resposne.meta["url_info"]
        autohomeid = resposne.meta["autohomeid"]
        url_list = resposne.meta["url_list"]
        data = json.loads(resposne.text.replace('PingGuCallBack3(', '').replace(')', ''))
        if data["returncode"] == 0:
            price_data_info['good'][0]["4S置换"] = data['result']["conditiona"].split('-')[1]
            price_data_info['middle'][0]["4S置换"] = data['result']["conditionb"].split('-')[1]
            price_data_info['bad'][0]["4S置换"] = data['result']["conditionc"].split('-')[1]
        # print(price_data_info)
        url_list.append(resposne.url)
        v4_url = f"https://pinguapi.che168.com/v1/auto/usedcarassess.ashx?{url_info}&_appversion=2.04v"
        yield scrapy.Request(
            url=v4_url,
            callback=self.parse_v4_price,
            headers=self.headers,
            meta={'url_info': url_info, "autohomeid": autohomeid, 'price_data_info': price_data_info,
                  'url_list': url_list}
        )

    def parse_v4_price(self, resposne):
        item = AutohomeGzItem()
        price_data_info = resposne.meta["price_data_info"]

        autohomeid = resposne.meta["autohomeid"]
        url_list = resposne.meta["url_list"]
        url_info = resposne.meta["url_info"]
        url_list.append(resposne.url)
        data = json.loads(resposne.text.replace('PingGuCallBack3(', '').replace(')', ''))
        if data["returncode"] == 0:
            price_data_info['good'][0]["卖给商家"] = data['result']["conditiona"].split('-')[1]
            price_data_info['middle'][0]["卖给商家"] = data['result']["conditionb"].split('-')[1]
            price_data_info['bad'][0]["卖给商家"] = data['result']["conditionc"].split('-')[1]
        good = price_data_info['good']
        middle = price_data_info['middle']
        bad = price_data_info['bad']
        good_guarantee_buy = good[0]['买保障车']
        good_merchant_buy = good[0]['买商家车']
        good_personage_buy = good[0]['买个人车']
        good_personage_sell = good[0]['卖给个人']
        good_4Sreplacement = good[0]['4S置换']
        good_merchant_sell = good[0]['卖给商家']

        middle_guarantee_buy = middle[0]['买保障车']
        middle_merchant_buy = middle[0]['买商家车']
        middle_personage_buy = middle[0]['买个人车']
        middle_personage_sell = middle[0]['卖给个人']
        middle_4Sreplacement = middle[0]['4S置换']
        middle_merchant_sell = middle[0]['卖给商家']

        bad_guarantee_buy = bad[0]['买保障车']
        bad_merchant_buy = bad[0]['买商家车']
        bad_personage_buy = bad[0]['买个人车']
        bad_personage_sell = bad[0]['卖给个人']
        bad_4Sreplacement = bad[0]['4S置换']
        bad_merchant_sell = bad[0]['卖给商家']
        item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['autohomeid'] = autohomeid
        item['good_guarantee_buy'] = good_guarantee_buy
        item['good_merchant_buy'] = good_merchant_buy
        item['good_personage_buy'] = good_personage_buy
        item['good_personage_sell'] = good_personage_sell
        item['good_4Sreplacement'] = good_4Sreplacement
        item['good_merchant_sell'] = good_merchant_sell

        item['middle_guarantee_buy'] = middle_guarantee_buy
        item['middle_merchant_buy'] = middle_merchant_buy
        item['middle_personage_buy'] = middle_personage_buy
        item['middle_personage_sell'] = middle_personage_sell
        item['middle_4Sreplacement'] = middle_4Sreplacement
        item['middle_merchant_sell'] = middle_merchant_sell

        item['bad_guarantee_buy'] = bad_guarantee_buy
        item['bad_merchant_buy'] = bad_merchant_buy
        item['bad_personage_buy'] = bad_personage_buy
        item['bad_personage_sell'] = bad_personage_sell
        item['bad_4Sreplacement'] = bad_4Sreplacement
        item['bad_merchant_sell'] = bad_merchant_sell
        cid = re.findall("&cid=(.*?)&", url_info)[0]
        item["city"] = cid
        item["price_data_info"] = json.dumps(price_data_info, ensure_ascii=False)
        item["url_list"] = json.dumps(url_list, ensure_ascii=False)
        item["status"] = url_info

        firstregtime = re.findall("&firstregtime=(.*?)&", url_info)[0]
        mileage = re.findall("&mileage=(.*?)&", url_info)[0]
        item["registerdate"] = firstregtime
        item["mile"] = mileage
        # print(item['status'])
        yield item

    #     cs = resposne.url.split('pgtype=1&')[1]
    #     autohomeid = resposne.meta["autohomeid"]
    #     data = json.loads(resposne.text.replace("'", '"'))
    #     html_id = data["message"][0]
    #     buy_detail_url = f"https://www.che168.com/pinggu/buyeva_{html_id}/0.html?{cs}{end}"
    #     sale_detail_url = f"https://www.che168.com/pinggu/eva_{html_id}/0.html?{cs}{end}"
    #     # print(buy_detail_url)
    #     # print(sale_detail_url)
    #     yield scrapy.Request(
    #         url=buy_detail_url,
    #         callback=self.parse_buy_detail_page,
    #         meta={"autohomeid": autohomeid}
    #
    #     )
    #
    # def parse_buy_detail_page(self, response):
    #     item = AutohomeGzItem()
    #     item["autohomeid"] = response.meta["autohomeid"]
    #     item["cartitle"] = response.xpath("//div[@id='cartitle']/text()").get()
    #     if 'buy' in response.url:
    #         item["gz_type"] = 'buy'
    #     else:
    #         item["gz_type"] = 'sale'
    #
    #     response.xpath("//p[@class='reference']").getall()
    #
    #     url = f'https://pinguapi.che168.com/v1/auto/usedcarassess.ashx?_appid=pc.pingu&_sign=&encoding=gb2312&pid=310000&cid=310100&mileage=40000&firstregtime=2019-06&specid=36600&iscondition=1&_appversion=2.07v'
    #
    #     print(item)
