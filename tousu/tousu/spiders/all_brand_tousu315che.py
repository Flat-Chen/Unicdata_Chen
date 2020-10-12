# -*- coding: utf-8 -*-
import scrapy
import time
import json
from tousu.items import TousuItem
import time
from datetime import datetime


class AllBrandTousu315cheSpider(scrapy.Spider):
    name = 'all_brand_tousu315che'
    allowed_domains = ['315che.com']
    # start_urls = ['http://315che.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(AllBrandTousu315cheSpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        self.page_num = 1
        self.month_list = {"Jan": "1", "Feb": "2", "Mar": "3", "Apr": "4", "May": "5", "Jun": "6", "Jul": "7",
                           "Aug": "8", "Sep": "9", "Oct": "10", "Nov": "11", "Dec": "12"}

    is_debug = True
    custom_debug_settings = {
        # 'MYSQL_SERVER': '192.168.1.94',
        # 'MYSQL_USER': 'dataUser94',
        # 'MYSQL_PWD': '94dataUser@2020',
        # 'MYSQL_DB': 'tousu',
        # 'MYSQL_TABLE': 'car_tousu_all',
        # 'MONGODB_SERVER': '',
        # 'MONGODB_DB': '',
        # 'MONGODB_COLLECTION': 'all_brand_tousu315che',
        "MONGODB_SERVER": "192.168.2.149",
        "MONGODB_PORT": 27017,
        "MONGODB_DB": "tousu",
        "MONGODB_COLLECTION": "quanwang_tousu",
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
            'tousu.middlewares.ProxyMiddleware': 400,
            # 'tousu.middlewares.SeleniumMiddleware': 401,
        },

    }

    def start_requests(self):
        for page_num in range(1, 2000):
            url = f'http://tousu.315che.com/tousuList/2/12/{page_num}.htm'
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                dont_filter=True
            )

    def parse(self, response):
        li_list = response.xpath("//div[@class='tousu-list-box clearfix']//li")
        for li in li_list:
            detail_url = li.xpath(".//a/@href").get()
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail_url,
                headers=self.headers
            )

        # next_url = response.xpath("//a[@class='page next']/@href").get()
        # if next_url:
        #     self.page_num += 1
        #     if self.page_num < 3:
        #         yield scrapy.Request(
        #             url=next_url,
        #             callback=self.parse,
        #             headers=self.headers,
        #             meta={"k": k}
        #         )
        #     else:
        #         pass

    def parse_detail_url(self, response):
        item = TousuItem()
        item["detail_url"] = response.url
        item["brand"] = response.xpath("//div[@class='container breadnav']/a[3]/text()").get()
        item["series"] = response.xpath("//div[@class='container breadnav']/a[4]/text()").get()
        tousu_date = response.xpath("//div[@class='complaints-appeal-info']//p[contains(text(),'投诉时间')]/text()").get().split("：")[1]

        for k, v in self.month_list.items():
            tousu_date = tousu_date.replace(k, v).replace(',', '') if k in tousu_date else tousu_date
        if 'M' in tousu_date:
            s = tousu_date.split(' ')
            date_tmp = f"{s[2]}-{s[0]}-{s[1]} {s[3]}"
            item["tousu_date"] = str(datetime.strptime(date_tmp, "%Y-%m-%d %H:%M:%S"))
        else:
            item["tousu_date"] = tousu_date
        item["introduct"] = response.xpath("//div[@class='complaints-appeal-info']//p[contains(text(),'诉求问题')]/text()").get().split("：")[1]
        item["dataSource"] = "汽车消费网"
        item["grabtime"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item["status"] = item["detail_url"] + '-' + str(item["series"]) + '-' + str(item["brand"])
        # item[""] = response.xpath("").get()
        yield item
        # print(item)


