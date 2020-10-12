# -*- coding: utf-8 -*-
import scrapy
import time
import json
from copy import deepcopy
from carbuisness_new.items import XiaoZhuItem


class XiaozhuModellistSpider(scrapy.Spider):
    name = 'xiaozhu_modellist'
    allowed_domains = ['xiaozhu2.com']
    # start_urls = ['http://xiaozhu2.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(XiaozhuModellistSpider, self).__init__(**kwargs)
        self.counts = 0


    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'residual_value',
        'MYSQL_TABLE': 'xiaozhu_modellist',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'residual_value',
        'MONGODB_COLLECTION': 'xiaozhu_modellist',
        'CrawlCar_Num': 800000,
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }
    def start_requests(self):
        url = "https://cartype-universe.maiche.com/api/h5/brand/get-brand-group-list.htm?_r=113427578184792432094"
        yield scrapy.Request(
            url=url,
            dont_filter=True
        )

    def parse(self, response):
        item = XiaoZhuItem()
        brand_data = json.loads(response.text)
        itemsList = brand_data["data"]["itemList"]
        for items in itemsList:
            for brand in items["brandList"]:
                item["brand"] = brand["name"]
                item["brand_id"] = brand["id"]
                series_url = f"https://cartype-universe.maiche.com/api/h5/series/get-series-group-list-by-brand.htm?_platform=web&_r=113427578184792432094&brandId={brand['id']}"
                yield scrapy.Request(
                    url=series_url,
                    callback=self.parse_series,
                    meta=deepcopy({"item": item}),
                    dont_filter=True
                )
    def parse_series(self, response):
        item = response.meta["item"]
        series_data = json.loads(response.text)
        # print(item)
        series_hideList = series_data["data"]["hideList"]
        series_showList = series_data["data"]["showList"]
        series_list = series_hideList+series_showList
        for series in series_list:
            # 厂商id和名字
            item["factoryId"] = series["groupId"]
            item["factoryName"] = series["groupName"]
            for serie in series["seriesList"]:
                item["series_id"] = serie["id"]
                item["maxFactoryPrice"] = serie["maxFactoryPrice"]
                item["minFactoryPrice"] = serie["minFactoryPrice"]
                item["referencePrice"] = serie["referencePrice"]
                item["series"] = serie["nameAbbr"]
                model_url = f"https://cartype-universe.maiche.com/api/h5/model/get-model-group-list-by-series.htm?_platform=web&_r=113427578184792432094&seriesId={serie['id']}"
                yield scrapy.Request(
                    url=model_url,
                    callback=self.parse_model,
                    meta=deepcopy({"item": item}),
                    dont_filter=True
                )

    def parse_model(self, response):
        item = response.meta["item"]
        model_data = json.loads(response.text)
        model_hideList = model_data["data"]["hideList"]
        model_showList = model_data["data"]["showList"]
        model_unlistedList = model_data["data"]["unlistedList"]
        model_list = model_hideList+model_showList+model_unlistedList
        for model in model_list:
            item["model_category"] = model["groupName"]
            for m in model["modelList"]:
                item["model_id"] = m["id"]
                item["price"] = m["price"]
                item["output"] = m["displacementWithUnit"]
                item["model"] = m["name"]
                item["year"] = m["year"]
                item["saleStatus"] = m["saleStatus"]
                item["status"] = str(item["year"])+'-'+str(item["model"])+'-'+str(item["model_id"])+'-'+str(item["saleStatus"])
                item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
                # print(item)
                yield item











