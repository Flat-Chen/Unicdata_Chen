# -*- coding: utf-8 -*-
import pymysql
import scrapy
import re

coon = pymysql.connect(
    host='192.168.1.94',
    user='dataUser94',
    password='94dataUser@2020',
    database='usedcar_update',
    charset='utf8'
)
cursor = coon.cursor()
sql = '''
SELECT id,carid,url
FROM hx2car_online
WHERE newcarid IS NULL
'''
cursor.execute(sql)
countAll = cursor.fetchall()


class UpdateHx2carCartypeSpider(scrapy.Spider):
    name = 'update_hx2car_carType'
    allowed_domains = ['hx2car.com']
    start_urls = ['http://hx2car.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(UpdateHx2carCartypeSpider, self).__init__(**kwargs)
        self.counts = 0
        self.counts_None = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'sedcar_update',
        'MYSQL_TABLE': 'hx2car_online',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'huaxia',
        'MONGODB_COLLECTION': 'huaxia_guzhi',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOADER_MIDDLEWARES': {
            'huaxia.middlewares.HuaxiaDownloaderMiddleware': 543,
            'huaxia.middlewares.HuaxiaProxyMiddleware': 200,
            'huaxia.middlewares.h2xUserAgentMiddleware': 199,
        }

    }

    def start_requests(self):
        for id, carid, url in countAll:
            url = url
            yield scrapy.Request(url=url, meta={"info": (id, carid, url)})

    def parse(self, response):
        id, carid, url = response.meta.get('info')
        carType = re.findall(r'carType :\'(\d+)\'', response.text)
        if carType != []:
            newcarid = carType[0]
            # print(newcarid)
            sql_upd = 'update hx2car_online set newcarid =%s where carid =%s'
            cursor.execute(sql_upd, (newcarid, carid))
            coon.commit()
            self.counts = self.counts + 1
            print(f'已经更新了{self.counts}个carid')
            print(id, carid, newcarid, url)
        else:
            newcarid = 'None'
            sql_upd = 'update hx2car_online set newcarid =%s where carid =%s'
            cursor.execute(sql_upd, (newcarid, carid))
            coon.commit()
            self.counts_None = self.counts_None + 1
            print(f'{self.counts_None}条数据没有carid')
