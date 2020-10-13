# 取遗漏URL
import json
import logging
import random

import requests
import scrapy


class AutohomeLuntanSpider(scrapy.Spider):
    name = 'autohome_luntan'
    allowed_domains = ['autohome.com.cn']
    start_urls = ["https://club.autohome.com.cn/frontapi/bbs/getSeriesByLetter"]

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeLuntanSpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {'Referer': 'https://club.autohome.com.cn/',
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}

        self.factory = {'名爵': '上汽乘用车',
                        '荣威': '上汽乘用车',
                        '上海': '上汽乘用车',
                        '大众': '上汽大众',
                        '斯柯达': '上汽大众',
                        '上汽MAXUS': '上汽大通',
                        '别克': '上汽通用',
                        '凯迪拉克': '上汽通用',
                        '雪佛兰': '上汽通用',
                        '宝骏': '上汽通用五菱',
                        "新宝骏": '上汽通用五菱',
                        '五菱汽车': '上汽通用五菱',
                        '依维柯': '南京依维柯'}
        self.brand_lsit = ["斯柯达", '名爵', '荣威', '上海', '大众', '上汽MAXUS', '别克', '凯迪拉克', '雪佛兰', '宝骏', '新宝骏', '五菱汽车', '依维柯']

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': "192.168.1.94",
        'MYSQL_USER': "dataUser94",
        'MYSQL_PWD': "94dataUser@2020",
        'MYSQL_PORT': 3306,
        'MYSQL_DB': "saicnqms",
        'MYSQL_TABLE': "autohome_luntan_9url",
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'luntan',
        'MONGODB_COLLECTION': 'autohome_luntan_1',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        # 'DOWNLOAD_TIMEOUT': 5,
        # 'RETRY_ENABLED': False,
        # 'RETRY_TIMES': 1,
        # 'COOKIES_ENABLED': True,
        # 'REDIS_URL': 'redis://192.168.1.241:6379/14',
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'luntan.middlewares.LuntanProxyMiddleware': 400,
        #     'luntan.middlewares.LuntanUserAgentMiddleware': 100,
        # },
        # 'ITEM_PIPELINES': {
        'luntan.pipelines.LuntanPipeline': 300,
        #     'luntan.pipelines.RenameTable': 299
        # },
    }

    def parse(self, response):
        try:
            car_url_dict = json.loads(response.text)["resul1t"]
        except:
            car_url_dict = requests.get(url="https://club.autohome.com.cn/frontapi/bbs/getSeriesByLetter",
                                        headers=self.headers).json()["result"]
        random.shuffle(car_url_dict)
        for car_url_list in car_url_dict:
            car_urls = car_url_list["bbsBrand"]
            random.shuffle(car_urls)
            for car_url in car_urls:
                brand = car_url["bbsBrandName"]
                bbslit = car_url["bbsList"]
                random.shuffle(bbslit)
                if brand in self.brand_lsit:
                    for car in bbslit:
                        # print(car ,"-"*50)
                        car_id = car["bbsId"]
                        user_car = car["bbsName"]
                        meta = {"id": car_id, "user_car": user_car, "page": 1, "brand": brand,
                                'factory': self.factory[brand]}
                        # print(meta)
                        url = "https://club.autohome.com.cn/frontapi/topics/getByBbsId?pageindex=1&pagesize=100&bbs=c&bbsid={}&fields=topicid%2Ctitle%2Cpost_memberid%2Cpost_membername%2Cpostdate%2Cispoll%2Cispic%2Cisrefine%2Creplycount%2Cviewcount%2Cvideoid%2Cisvideo%2Cvideoinfo%2Cqainfo%2Ctags%2Ctopictype%2Cimgs%2Cjximgs%2Curl%2Cpiccount%2Cisjingxuan%2Cissolve%2Cliveid%2Clivecover%2Ctopicimgs&orderby=topicid-".format(
                            car_id)
                        yield scrapy.Request(url=url, callback=self.page_turning,
                                             meta=meta)

    def page_turning(self, response):
        # print(response.text)
        item = {}
        pinglun_url_dict = json.loads(response.text)
        if pinglun_url_dict["returncode"] != 0:
            return
        else:
            for pinglun_url in pinglun_url_dict["result"]["list"]:
                item['tiezi_url'] = url = pinglun_url["url"]
                yield item
                # 就是要把这个tiezi_url存起来 进行比对
        if int(pinglun_url_dict["result"]["list"][-1]['postdate'].split('-')[1]) > 8:
            url = "https://club.autohome.com.cn/frontapi/topics/getByBbsId?pageindex={}&pagesize=100&bbs=c&bbsid={}&fields=topicid%2Ctitle%2Cpost_memberid%2Cpost_membername%2Cpostdate%2Cispoll%2Cispic%2Cisrefine%2Creplycount%2Cviewcount%2Cvideoid%2Cisvideo%2Cvideoinfo%2Cqainfo%2Ctags%2Ctopictype%2Cimgs%2Cjximgs%2Curl%2Cpiccount%2Cisjingxuan%2Cissolve%2Cliveid%2Clivecover%2Ctopicimgs&orderby=topicid-"
            response.meta["page"] = response.meta["page"] + 1
            url = url.format(response.meta["page"], response.meta["id"], )
            yield scrapy.Request(url=url,
                                 callback=self.page_turning,
                                 meta=response.meta, headers=self.headers)
            print(response.meta["page"])
