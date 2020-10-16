# -*- coding: utf-8 -*-
# 逻辑是先运行xiaozhu_url 将所有要爬取的URL存到数据库
# 该爬虫直接从数据库取URL爬取 对比总量看遗漏
import scrapy
import time
import pymongo
import pandas as pd
import datetime
import re

from pandas import DataFrame

settings = {
    "MONGODB_SERVER": "192.168.2.149",
    "MONGODB_PORT": 27017,
    "MONGODB_DB": "xiaozhu",
    "MONGODB_COLLECTION": "xiaozhu_url_2020-10-16",
}
uri = f'mongodb://{settings["MONGODB_SERVER"]}:{settings["MONGODB_PORT"]}/'

connection = pymongo.MongoClient(uri)
db = connection[settings['MONGODB_DB']]
collection = db[settings['MONGODB_COLLECTION']]
model_data = collection.find({}, {"status": 1, "_id": 0})

car_msg_list = list(model_data)
car_msg_df = DataFrame(car_msg_list)
car_msg_df_new = car_msg_df.drop_duplicates('status')


class XiaozhuGzSpider(scrapy.Spider):
    name = 'xiaozhu_gz'
    allowed_domains = ['xiaozhu2.com']

    # start_urls = ['http://xiaozhu2.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(XiaozhuGzSpider, self).__init__(**kwargs)
        self.counts = 0
        self.car_msg_df_new = car_msg_df_new

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
        'MONGODB_COLLECTION': 'xiaozhu_gz_update',
        'CONCURRENT_REQUESTS': 32,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOAD_TIMEOUT': 15,
        # 'REDIS_URL': 'redis://192.168.1.241:6379/14',
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'che300_new.middlewares.Che300NewProxyMiddleware': 400,
        #     'che300_new.middlewares.Che300NewUserAgentMiddleware': 100,
        # },
        'ITEM_PIPELINES': {
            'xiaozhu.pipelines.XiaozhuPipeline': 299,
            'xiaozhu.pipelines.RenameTable': 298,
        },
    }

    def start_requests(self):
        for index, rows in self.car_msg_df_new.iterrows():
            url = rows['status']
            yield scrapy.Request(url=url)

    def parse(self, response):
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
        item['good_middle'] = data_dict['车况良好'][1]
        item['good_high'] = data_dict['车况良好'][0]
        item['excellent_low'] = data_dict['车况优秀'][2]
        item['excellent_middle'] = data_dict['车况优秀'][1]
        item['excellent_high'] = data_dict['车况优秀'][0]
        item["status"] = response.url + "-" + str(datetime.datetime.now().year) + "-" + str(
            datetime.datetime.now().month)

        yield item
        # print(item)
