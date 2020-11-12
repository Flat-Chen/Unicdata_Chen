import time
import scrapy
import json


class AutohomeDealerSpider(scrapy.Spider):
    name = 'autohome_dealer'

    allowed_domains = ['autohome.com.cn']
    start_urls = [
        'https://dealer.autohome.com.cn/DealerList/GetAreasAjax?provinceId=0&cityId=340100&brandid=0&manufactoryid=0&seriesid=0&isSales=0']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeDealerSpider, self).__init__(**kwargs)
        self.counts = 0
        self.website = 'autohome_dealer'

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': "192.168.1.94",
        'MYSQL_USER': "dataUser94",
        'MYSQL_PWD': "94dataUser@2020",
        'MYSQL_PORT': 3306,
        'MYSQL_DB': "autohome",
        'MYSQL_TABLE': "autohome_dealer",
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'network',
        'MONGODB_COLLECTION': 'autohome_dealer',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        # 'DOWNLOAD_TIMEOUT': 5,
        # 'RETRY_ENABLED': False,
        # 'RETRY_TIMES': 1,
        # 'COOKIES_ENABLED': True,
        # 'REDIS_URL': 'redis://192.168.1.241:6379/14',
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'autohome.middlewares.AutohomeProxyMiddleware': 400,
        #     'autohome.middlewares.AutohomeUserAgentMiddleware': 100,
        # },
        # 'ITEM_PIPELINES': {
        'autohome.pipelines.LuntanPipeline': 300,
        #     'autohome.pipelines.RenameTable': 299
        # },
    }

    def parse(self, response):
        json_data = json.loads(response.text)
        province_list = json_data['AreaInfoGroups']
        print(province_list)
