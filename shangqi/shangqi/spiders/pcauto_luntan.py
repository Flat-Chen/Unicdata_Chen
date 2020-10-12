# -*- coding: utf-8 -*-
import copy
import json
import time
from shangqi.items import LuntanItem
import scrapy
import re

website = 'pcauto_luntan'


class PcautoLuntanSpider(scrapy.Spider):
    name = 'pcauto_luntan'
    allowed_domains = ['pcauto.com.cn']
    start_urls = ['http://www.pcauto.com.cn/forum/sitemap/pp/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(PcautoLuntanSpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {
            'Referer': 'https://bbs.pcauto.com.cn',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            # "Cookie": "visitedfid=17957D20685D22418D20697D23985D23585D17913D17608D17504D17329",
        }

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'luntan',
        'MYSQL_TABLE': 'pcauto_luntan_new',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'luntan',
        'MONGODB_COLLECTION': 'pcauto_luntan',
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 1,
        'LOG_LEVEL': 'DEBUG',
    }

    def parse(self, response):
        tr_list = response.xpath("//td[@class='tdCon']/..")
        for tr in tr_list:
            brand = tr.xpath(".//td[@class='tdTit']/i/text()").get()
            brand_url = tr.xpath(".//a[@class='hei']/@href").getall()
            if brand_url:
                for url in brand_url:
                    forumId = re.findall('forum-(.*?).html', url)[0]
                    json_url = f"https://mrobot.pcauto.com.cn/xsp/s/auto/info/nocache/bbs/forums.xsp?forumId={forumId}&pageNo=1&pageSize=20"
                    # json_url = 'https://mrobot.pcauto.com.cn/xsp/s/auto/info/nocache/bbs/forums.xsp?forumId=28425&pageNo=1&pageSize=20'
                    yield scrapy.Request(
                        url=json_url,
                        callback=self.brand_parse,
                        headers=self.headers,
                        meta={"brand": brand, "forumId": forumId},
                        dont_filter=True
                    )

    def brand_parse(self, response):
        # print(response.url)
        forumId = response.meta["forumId"]
        json_data = json.loads(response.text)
        data_num = int(json_data["total"])

        for page_num in range(1, 6):
            print(data_num, page_num)

            url = f"https://mrobot.pcauto.com.cn/xsp/s/auto/info/nocache/bbs/forums.xsp?forumId={forumId}&pageNo={page_num}&pageSize=20"
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse_list, meta=response.meta)

    def parse_list(self, response):
        if response.status is 500:
            print('超出页数了！！！！')
        elif response.status is 200:
            json_data = json.loads(response.text)
            data_list = json_data["topicList"]
            for data in data_list:
                item = LuntanItem()
                item["brand"] = response.meta["brand"]
                item["title"] = data["title"]
                item["reply_num"] = data["replyCount"]
                # item["content_num"] = data["view"]
                item["click_num"] = data["view"]
                item["information_source"] = website
                item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item["user_name"] = data["author"]["name"]
                item["region"] = data["author"]["cityName"] if data["author"]["cityName"] else None
                createAt = data["createAt"]
                item["posted_time"] = deal_time(createAt)
                topicId = data["topicId"]
                datail_url = f"https://magear.pcauto.com.cn/p/bbs.pcauto.com.cn/wxapi/1/topic.do?tid={topicId}"
                yield scrapy.Request(
                    url=datail_url,
                    headers=self.headers,
                    callback=self.parse_detail_url,
                    meta={"item": copy.deepcopy(item)},
                    dont_filter=True,
                )

        else:
            print('什么都没执行到')

    def parse_detail_url(self, response):
        item = response.meta["item"]
        json_data = json.loads(response.text)
        data = json_data["data"]
        content_list = data["content"]
        txt_list = list()
        for content in content_list:
            if content["type"] == 2:
                txt_list.append(content["txt"])
        contents = "".join(txt_list).replace('&nbsp', '').replace(' ', '').replace('\u3000', '').replace('<br/>',
                                                                                                         '').replace(
            '\t', '').replace(';', '')
        item["content"] = contents
        item = response.meta["item"]
        item["url"] = response.url
        item["user_car"] = data["forumName"].replace("论坛", "")
        item["statusplus"] = str(item["user_name"]) + str(item["title"]) + str(item["posted_time"]) + str(
            item["brand"]) + str(item["reply_num"])
        print(item)
        yield item


def deal_time(sold_time):
    timeStamp = sold_time / 1000
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime
