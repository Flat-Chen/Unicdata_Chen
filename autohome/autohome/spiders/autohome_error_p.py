# -*- coding: utf-8 -*-
import json
import re
import time
import pymongo
import scrapy


class AutohomeErrorPSpider(scrapy.Spider):
    name = 'autohome_error_p'
    allowed_domains = ['autohome.com.cn']

    # start_urls = ['http://autohome.com.cn/']
    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeErrorPSpider, self).__init__(**kwargs)
        # print('              运行的是autohome_error_p！！！！！！')
        self.carnum = 1000000
        self.error_list = []

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'autohome',
        'MONGODB_COLLECTION': 'autohome_error_p',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["newcar"]
        collection = db["autohome_newcar"]
        # families = collection.distinct("familyid")
        # print(families)
        families = ['3780', '4370', '3429']
        urls = []
        for family in families:
            # print(family)
            url1 = "https://k.m.autohome.com.cn/seriesQuality/indexh5?sid=%s&carType=1" % family
            url2 = "https://k.m.autohome.com.cn/seriesQuality/indexh5?sid=%s&carType=2" % family
            urls.append(scrapy.Request(url=url1, meta={"category_id": 1, "familyid": family}))
            urls.append(scrapy.Request(url=url2, meta={"category_id": 2, "familyid": family}))
        return urls

    def parse(self, response):
        family_id = response.meta.get('familyid')
        if 'class="img404"' in response.text or '暂无质量报告数据' in response.text:
            # 过滤掉无数据的404网页
            # print('            无数据 pass掉!')
            pass
        else:
            if response.meta["category_id"] == 1:
                # 新车质量研究
                print(family_id, '这是新车质量研究')
                familyname = response.xpath('//p[@class="car-name"]//text()').extract_first()
                error_index = response.xpath('//span[@class="normal-nums"]/text()').extract_first().strip()
                error_all = response.xpath('//ul[@class="legend clearfix"]/li/text()')
                print(familyname, error_index, error_all)




            else:
                # print(family_id, '这是可靠性质量研究')
                # 可靠性质量研究
                pass











        # data = re.findall(r"data\: \[(.*?)\]", response.text, re.S)[0]
        # if data:
        #     # print(data)
        #     data_obj = json.loads("[" + data + "]")
        #     item = {}
        #     item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        #     item["url"] = response.url
        #     item["status"] = response.url + "-" + time.strftime('%Y-%m', time.localtime())
        #     item["waiguan1"] = "-"
        #     item["xingshi1"] = "-"
        #     item["caozuo1"] = "-"
        #     item["dianzi1"] = "-"
        #     item["zuoyi1"] = "-"
        #     item["kongtiao1"] = "-"
        #     item["neishi1"] = "-"
        #     item["fadongji1"] = "-"
        #     item["biansuxitong1"] = "-"
        #     if response.meta["category_id"] == 1:
        #         for d in data_obj:
        #             item["waiguan1"] = d["value"] if d["id"] == "01" and item["waiguan1"] == "-" else item[
        #                 "waiguan1"]
        #             item["xingshi1"] = d["value"] if d["id"] == "02" and item["xingshi1"] == "-" else item[
        #                 "xingshi1"]
        #             item["caozuo1"] = d["value"] if d["id"] == "03" and item["caozuo1"] == "-" else item["caozuo1"]
        #             item["dianzi1"] = d["value"] if d["id"] == "04" and item["dianzi1"] == "-" else item["dianzi1"]
        #             item["zuoyi1"] = d["value"] if d["id"] == "05" and item["zuoyi1"] == "-" else item["zuoyi1"]
        #             item["kongtiao1"] = d["value"] if d["id"] == "06" and item["kongtiao1"] == "-" else item[
        #                 "kongtiao1"]
        #             item["neishi1"] = d["value"] if d["id"] == "07" and item["neishi1"] == "-" else item["neishi1"]
        #             item["fadongji1"] = d["value"] if d["id"] == "08" and item["fadongji1"] == "-" else item[
        #                 "fadongji1"]
        #             item["biansuxitong1"] = d["value"] if d["id"] == "09" and item["biansuxitong1"] == "-" else item[
        #                 "biansuxitong1"]
        #     else:
        #         for d in data_obj:
        #             item["fadongji1"] = d["value"] if d["id"] == "10" and item["fadongji1"] == "-" else item[
        #                 "fadongji1"]
        #             item["neishi1"] = d["value"] if d["id"] == "11" and item["neishi1"] == "-" else item["neishi1"]
        #             item["kongtiao1"] = d["value"] if d["id"] == "12" and item["kongtiao1"] == "-" else item[
        #                 "kongtiao1"]
        #             item["zuoyi1"] = d["value"] if d["id"] == "13" and item["zuoyi1"] == "-" else item["zuoyi1"]
        #             item["dianzi1"] = d["value"] if d["id"] == "14" and item["dianzi1"] == "-" else item["dianzi1"]
        #             item["caozuo1"] = d["value"] if d["id"] == "15" and item["caozuo1"] == "-" else item["caozuo1"]
        #             item["xingshi1"] = d["value"] if d["id"] == "16" and item["xingshi1"] == "-" else item[
        #                 "xingshi1"]
        #             item["waiguan1"] = d["value"] if d["id"] == "17" and item["waiguan1"] == "-" else item[
        #                 "waiguan1"]
        #     item["familyid"] = response.meta["familyid"]
        #     item["category_id"] = response.meta["category_id"]
        #     item["json"] = data
        #     item["sum"] = response.xpath("//*[@class='piechart']/h4/span[2]/text()[1]").extract_first().strip()
        #     print(item)
