import scrapy
import time
import pymongo
import pandas as pd
import datetime
import re

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


class XiaozhuUrlSpider(scrapy.Spider):
    name = 'xiaozhu_url'

    # allowed_domains = ['xiaozhu2.com']
    # start_urls = ['http://xiaozhu2.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(XiaozhuUrlSpider, self).__init__(**kwargs)
        self.counts = 0
        self.city_list = ["beijing", "shanghai", "chengdu", "guangzhou"]
        data = pd.DataFrame(list(collection.find()))
        data = data[data["output"].notnull()]
        self.data = data.loc[:, ["model_id", "year"]]
        self.data["year"].astype('int')
        self.now_year = datetime.datetime.now().year
        now_month = datetime.datetime.now().month
        self.now_month = f"0{str(now_month)}" if now_month < 10 else now_month

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': "192.168.1.94",
        'MYSQL_USER': "dataUser94",
        'MYSQL_PWD': "94dataUser@2020",
        'MYSQL_PORT': 3306,
        'MYSQL_DB': "",
        'MYSQL_TABLE': "",
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'xiaozhu',
        'MONGODB_COLLECTION': 'xiaozhu_url_2020-10-16',
        'CONCURRENT_REQUESTS': 32,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOAD_TIMEOUT': 15,
        # 'DOWNLOAD_TIMEOUT': 5,
        # 'RETRY_ENABLED': False,
        # 'RETRY_TIMES': 1,
        # 'COOKIES_ENABLED': True,
        # 'REDIS_URL': 'redis://192.168.1.241:6379/14',
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'xiaozhu.middlewares.XiaozhuProxyMiddleware': 400,
        #     'xiaozhu.middlewares.XiaozhuUserAgentMiddleware': 100,
        # },
        # 'ITEM_PIPELINES': {
        'xiaozhu.pipelines.XiaozhuPipeline': 300,
        #     'xiaozhu.pipelines.RenameTable': 299
        # },
    }

    def start_requests(self):
        yield scrapy.Request(url='http://www.baidu.com')

    def parse(self, response):
        item = {}
        for index, rows in self.data.iterrows():
            if rows["year"] < self.now_year - 4:
                year_list = [i for i in range(rows["year"], rows["year"] + 4)]
                year_dic = {year: (self.now_year - year) * 20000 for year in year_list}
                for k, v in year_dic.items():
                    if v == 0:
                        v = 1000
                    for city in self.city_list:
                        url = f"https://www.xiaozhu2.com/appraisal/w{city}-x{rows['model_id']}-y{k}{self.now_month}-z{v}.html"
                        item['status'] = url
                        yield item
            else:
                year_list = [i for i in range(rows["year"], self.now_year + 1)]
                year_dic = {year: (self.now_year - year) * 20000 for year in year_list}
                for k, v in year_dic.items():
                    if v == 0:
                        v = 1000
                    for city in self.city_list:
                        url = f"https://www.xiaozhu2.com/appraisal/w{city}-x{rows['model_id']}-y{k}{self.now_month}-z{v}.html"
                        item['status'] = url
                        yield item
