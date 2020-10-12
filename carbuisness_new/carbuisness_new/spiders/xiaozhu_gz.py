# -*- coding: utf-8 -*-
import scrapy
import time
import json
import pymongo
import pandas as pd
import datetime
import re

from carbuisness_new.items import XiaoZhuItem

settings = {
    "MONGODB_SERVER": "192.168.1.94",
    "MONGODB_PORT": 27017,
    "MONGODB_DB": "residual_value",
    "MONGODB_COLLECTION": "xiaozhu_modellist",
}
uri = f'mongodb://{settings["MONGODB_SERVER"]}:{settings["MONGODB_PORT"]}/'

connection = pymongo.MongoClient(uri)
db = connection[settings['MONGODB_DB']]
collection = db[settings['MONGODB_COLLECTION']]


class XiaozhuGzSpider(scrapy.Spider):
    name = 'xiaozhu_gz'

    # allowed_domains = ['xiaozhu2.com']

    # start_urls = ['http://xiaozhu2.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(XiaozhuGzSpider, self).__init__(**kwargs)
        self.counts = 0
        self.city_list = ["beijing", "tianjin", "shijiazhuang", "taiyuan", "huhehaote", "shanghai", "qingdao", "suzhou",
                          "hangzhou", "hefei", "shenzhen", "fuzhou", "nanning", "haikou", "zhengzhou", "wuhan",
                          "changsha", "nanchang", "shenyang", "haerbin", "changchun", "chongqing", "chengdu", "kunming",
                          "guiyang", "lasa", "xian", "wulumuqi", "lanzhou", "yinchuan", "xining"]
        data = pd.DataFrame(list(collection.find()))
        data = data[data["output"].notnull()]
        self.data = data.loc[:, ["model_id", "year"]]
        self.data["year"].astype('int')
        self.now_year = datetime.datetime.now().year
        now_month = datetime.datetime.now().month
        self.now_month = f"0{str(now_month)}" if now_month < 10 else now_month
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'residual_value',
        'MYSQL_TABLE': 'xiaozhu_gz',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'xiaozhu',
        'MONGODB_COLLECTION': 'xiaozhu_gz_update',
        'CrawlCar_Num': 800000,
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'ITEM_PIPELINES': {
            'carbuisness_new.pipelines.CarbuisnessNewPipeline': 300,
            'carbuisness_new.pipelines.RenameTable': 299
        }
    }

    def start_requests(self):
        url = "https://www.baidu.com/"
        yield scrapy.Request(
            url=url,
        )

    def parse(self, response):
        for index, rows in self.data.iterrows():
            if rows["year"] < self.now_year:
                year_list = [i for i in range(rows["year"], self.now_year + 1)]
                year_dic = {year: (self.now_year - year) * 20000 for year in year_list}
                for k, v in year_dic.items():
                    if v == 0:
                        v = 1000
                    for city in self.city_list:
                        url = f"https://www.xiaozhu2.com/appraisal/w{city}-x{rows['model_id']}-y{k}{self.now_month}-z{v}.html"
                        if k == 2020:
                            print(url)
                        yield scrapy.Request(
                            url=url,
                            callback=self.parse_detail,
                            headers=self.headers,
                            dont_filter=True
                        )

    def parse_detail(self, response):
        item = dict()
        price_list = response.xpath("//div[@class='holder']/span/text()").getall()
        tag_list = response.xpath("//div[@class='content-tab']/ul/li/text()").getall()
        data_dict = dict()
        for tag in tag_list:
            price = [price_list[i:i + 3] for i in range(0, len(price_list), 3)]
            data_dict[tag] = price[tag_list.index(tag)]

        # price = json.dumps(data_dict, ensure_ascii=False)
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["model_id"] = re.findall('-x(.*?)-y', response.url)[0]
        info = response.xpath("//p[@class='price']/following-sibling::p/text()").get().replace(' ', '').replace('\xa0',
                                                                                                                '')
        info_list = info.split('|')
        item["city"] = info_list[0]
        item["registerdate"] = info_list[1]
        item["mile"] = info_list[2]
        item["desc"] = response.xpath("//h3[@class='name']/text()").get()
        item['commonly_low'] = data_dict['车况一般'][2]
        item['commonly_middle'] = data_dict['车况一般'][1]
        item['commonly_high'] = data_dict['车况一般'][0]
        item['good_low'] = data_dict['车况良好'][2]
        item['good_middle'] = data_dict['车况良好'][2]
        item['good_high'] = data_dict['车况良好'][2]
        item['excellent_low'] = data_dict['车况优秀'][2]
        item['excellent_middle'] = data_dict['车况优秀'][2]
        item['excellent_high'] = data_dict['车况优秀'][2]
        item["status"] = response.url + "-" + str(datetime.datetime.now().year) + "-" + str(
            datetime.datetime.now().month)

        yield item
        # print(item)
