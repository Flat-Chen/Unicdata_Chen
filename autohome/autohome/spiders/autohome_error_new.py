# -*- coding: utf-8 -*-
import scrapy
from autohome.items import AutohomeErrorItem
import time
import logging
import json
import re
import pymongo

website = 'autohome_error_new'


class CarSpider(scrapy.Spider):
    name = website
    start_urls = []

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'carbusiness',
        'MONGODB_COLLECTION': website,
        'CrawlCar_Num': 800000,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
    }

    def __init__(self, **kwargs):
        super(CarSpider, self).__init__(**kwargs)
        self.counts = 0

    def start_requests(self):
        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["newcar"]
        collection = db["autohome_newcar"]
        families = collection.distinct("familyid")

        urls = []
        for family in families:
            url = f"https://k.autohome.com.cn/{family}/quality"
            urls.append(scrapy.Request(url=url, meta={"familyid": family}))
            # urls.append(url)
        return urls

    def parse(self, response):
        item = AutohomeErrorItem()
        familyid = response.meta["familyid"]
        item["series_id"] = familyid
        item["url"] = response.url
        item["status"] = response.url + "-" + time.strftime('%Y-%m', time.localtime())
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["brand"] = response.xpath("//div[@class='subnav-title-name']/a/text()").get().replace("-", '')
        item["series"] = response.xpath("//div[@class='subnav-title-name']/a/h1/text()").get()
        # item[""] = response.xpath("").get()
        # item["newcar_quality"] = response.xpath("").get()
        item["newcar_bug_num"] = response.xpath("//div[@class='tab-nav']/a[1]/b/text()").get().split("：")[1]
        item["newcar_people_num"] = response.xpath("//div[@class='tab-nav']/a[1]/text()").getall()[1]

        # # item["oldcar_quality"] = response.xpath("").get()
        item["oldcar_bug_num"] = response.xpath("//div[@class='tab-nav']/a[2]/b/text()").get().split("：")[1]
        item["oldcar_people_num"] = response.xpath("//div[@class='tab-nav']/a[2]/text()").getall()[1]

        # item["oldcar_bug_ratio"] = response.xpath("").get()
        try:
            item["newcar_bug_num"] = re.search("\d+", item["newcar_bug_num"]).group()
        except AttributeError:
            item["newcar_bug_num"] = None
        try:
            item["newcar_people_num"] = re.search("\d+", item["newcar_people_num"]).group()
        except AttributeError:
            item["newcar_people_num"] = None
        try:
            item["oldcar_bug_num"] = re.search("\d+", item["oldcar_bug_num"]).group()
        except AttributeError:
            item["oldcar_bug_num"] = None
        try:
            item["oldcar_people_num"] = re.search("\d+", item["oldcar_people_num"]).group()
        except AttributeError:
            item["oldcar_people_num"] = None

        oldcar_li_list = response.xpath("//div[@id='quality-chart-box-02']//div[@class='quality-most mb-10']/ul/li")
        newcar_li_list = response.xpath("//div[@id='quality-chart-box-01']//div[@class='quality-most mb-10']/ul/li")
        if oldcar_li_list:
            oldcar_bug_type_list = list()
            for li in oldcar_li_list:
                bug_type_dic = dict()
                bug_type_dic["bug_name"] = li.xpath("./a/em/text()").get()
                bug_type_dic["bug_num"] = li.xpath("./a/span/text()").get().replace(" 个", "")
                oldcar_bug_type_list.append(bug_type_dic)
            item["oldcar_bug_type"] = oldcar_bug_type_list
        else:
            item["oldcar_bug_type"] = None

        if newcar_li_list:
            newcar_bug_type_list = list()
            for li in newcar_li_list:
                bug_type_dic = dict()
                bug_type_dic["bug_name"] = li.xpath("./a/em/text()").get()
                bug_type_dic["bug_num"] = li.xpath("./a/span/text()").get().replace(" 个", "")
                newcar_bug_type_list.append(bug_type_dic)
            item["newcar_bug_type"] = newcar_bug_type_list
        else:
            item["newcar_bug_type"] = None


        newcar_a_list = response.xpath("//div[@id='quality-chart-box-01']//div[@class='quality-form']/a")
        oldcar_a_list = response.xpath("//div[@id='quality-chart-box-02']//div[@class='quality-form']/a")

        if newcar_a_list:
            newcar_bug_ratio_list = list()
            for a in newcar_a_list:
                newcar_ratio_dic = dict()
                newcar_ratio_dic["qualityName"] = a.xpath(".//dt/text()").get()
                newcar_ratio_dic["qualityRatio"] = a.xpath(".//span/text()").get()
                newcar_bug_ratio_list.append(newcar_ratio_dic)
                # item["newcar_bug_ratio"] = newcar_bug_ratio_list
            if newcar_bug_ratio_list[0]["qualityRatio"] == '0%' and newcar_bug_ratio_list[1]["qualityRatio"] == '0%' and newcar_bug_ratio_list[2]["qualityRatio"] == '0%':
                item["newcar_bug_ratio"] = None
                print("*"*100)
                print(newcar_bug_ratio_list[0]["qualityRatio"])
            else:
                item["newcar_bug_ratio"] = newcar_bug_ratio_list
        else:
            item["newcar_bug_ratio"] = None

        if oldcar_a_list:
            oldcar_bug_ratio_list = list()
            for a in oldcar_a_list:
                oldcar_ratio_dic = dict()
                oldcar_ratio_dic["qualityName"] = a.xpath(".//dt/text()").get()
                oldcar_ratio_dic["qualityRatio"] = a.xpath(".//span/text()").get()
                oldcar_bug_ratio_list.append(oldcar_ratio_dic)
            if oldcar_bug_ratio_list[0]["qualityRatio"] == '0%' and oldcar_bug_ratio_list[1]["qualityRatio"] == '0%' and oldcar_bug_ratio_list[2]["qualityRatio"] == '0%':
                item["oldcar_bug_ratio"] = None
                print("-"*100)
                print(oldcar_bug_ratio_list[0]["qualityRatio"])
            else:
                item["oldcar_bug_ratio"] = oldcar_bug_ratio_list
        else:
            item["oldcar_bug_ratio"] = None

        # print(item)
        yield item
