# -*- coding: utf-8 -*-
import scrapy
import time
import json
import pymongo

from autohome.items import AutohomeButieItem

website = 'autohome_butie'


class AutohomeButieSpider(scrapy.Spider):
    name = website

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeButieSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'koubei',
        'MYSQL_TABLE': 'autohome_butie',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'koubei',
        'MONGODB_COLLECTION': 'autohome_butie',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'ITEM_PIPELINES': {'autohome.pipelines.GanjiPipeline': 300, }
    }

    def start_requests(self):
        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["newcar"]
        collection = db["autohome_newcar"]
        print("数据查询中...")
        result = collection.distinct("autohomeid")
        for autohomeid in result:
            url = "https://carif.api.autohome.com.cn/car/getspecelectricbutie.ashx?_callback=GetSpecElectricSubsidy&speclist=%s&cityid=310100&type=1" % str(
                autohomeid)
            yield scrapy.Request(
                url=url,
                dont_filter=False,
                meta={"autohomeid": autohomeid}
            )

    def parse(self, response):
        print(response.url)
        obj = json.loads(response.text.replace("GetSpecElectricSubsidy(", "")[:-1])
        if obj["result"] is not None:
            item = AutohomeButieItem()
            item['url'] = response.url
            item['status'] = response.url + time.strftime('%Y-%m', time.localtime())
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['autohomeid'] = response.meta["autohomeid"]
            item['minprice'] = obj['result']['specitems'][0]['minprice']
            item['maxprice'] = obj['result']['specitems'][0]['maxprice']
            yield item
            print(item)
