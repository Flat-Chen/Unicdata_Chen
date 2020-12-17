import json
import time

import pymongo
import scrapy


class Che300ModelinfoSpider(scrapy.Spider):
    name = 'che300_modelinfo'
    allowed_domains = ['che300.com']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(Che300ModelinfoSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': "192.168.1.94",
        'MYSQL_USER': "dataUser94",
        'MYSQL_PWD': "94dataUser@2020",
        'MYSQL_PORT': 3306,
        'MYSQL_DB': "che300",
        'MYSQL_TABLE': "che300_app_modelinfo",
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'che300',
        'MONGODB_COLLECTION': 'che300_app_modelinfo_update',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        # 'DOWNLOAD_TIMEOUT': 5,
        # 'RETRY_ENABLED': False,
        # 'RETRY_TIMES': 1,
        # 'COOKIES_ENABLED': True,
        # 'REDIS_URL': 'redis://192.168.1.241:6379/14',
        'DOWNLOADER_MIDDLEWARES': {
            # 'che300_xcx.middlewares.Che300XcxDownloaderMiddleware': 400,
            'che300_xcx.middlewares.Che300XcxUserAgentMiddleware': 101,
            'che300_xcx.middlewares.Che300XcxProxyMiddleware': 100,
        },
        'ITEM_PIPELINES': {
            'che300_xcx.pipelines.Che300XcxPipeline': 300,
            'che300_xcx.pipelines.RenameTable': 500,
        }
    }

    def start_requests(self):
        connection = pymongo.MongoClient('192.168.1.94', 27017)
        db = connection["che300"]
        collection = db["che300_car"]
        result = collection.find()
        result_list = list(result)
        for cars in result_list:
            vehicle_id = cars['vehicle_id']
            url = 'https://dingjia.che300.com/app/CarDetail/getModelConfigure/' + vehicle_id
            yield scrapy.Request(url)

    def parse(self, response):
        item = {}
        item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        json_data = json.loads(response.text)
        modelInfo = json_data['success']['modelInfo']
        for i in modelInfo.keys():
            try:
                item[i] = modelInfo[i]
            except:
                item[i] = modelInfo[i]
        item['url'] = response.url
        item['modelConfigure'] = str(json_data['success']['modelConfigure'])
        yield item
        # print(item)
