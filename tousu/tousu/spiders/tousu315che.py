# -*- coding: utf-8 -*-
import scrapy
from tousu.items import TousuItem
import time
from datetime import datetime


class Tousu315cheSpider(scrapy.Spider):
    name = 'tousu315che'
    allowed_domains = ['tousu.315che.com']

    # start_urls = ['http://tousu.315che.com/']

    def __init__(self):
        super(Tousu315cheSpider, self).__init__()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        self.brand_dic = None
        self.page_num = 1
        self.brand_url = None
        self.month_list = {"Jan": "1", "Feb": "2", "Mar": "3", "Apr": "4", "May": "5", "Jun": "6", "Jul": "7",
                           "Aug": "8", "Sep": "9", "Oct": "10", "Nov": "11", "Dec": "12"}

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        # 'MYSQL_TABLE': 'tousu_all',
        # 'MYSQL_DB': 'saicnqms',
        # 'MYSQL_SERVER': '192.168.1.94',
        # 'MYSQL_USER': 'dataUser94',
        # 'MYSQL_PWD': '94dataUser@2020',
        # 'MYSQL_TABLE': 'tousu315che',
        # 'MYSQL_DB': 'saicnqms',
        "MONGODB_SERVER": "192.168.2.149",
        "MONGODB_PORT": 27017,
        "MONGODB_DB": "tousu",
        "MONGODB_COLLECTION": "shangqi_tousu",
        'AUTOTHROTTLE_START_DELAY': 8,
        'DOWNLOAD_DELAY': 0.5,
    }

    def start_requests(self):
        # self.brand_dic = self.settings.get("BRAND_DIC")
        self.brand_url = self.settings.get("BRAND_URL")
        for k, v in self.brand_url.items():
            # if k == '宝骏':
            yield scrapy.Request(
                url=v,
                headers=self.headers,
                meta={"v": v, "k": k},
                dont_filter=True
            )

    def parse(self, response):
        self.brand_dic = self.settings.get("BRAND_DIC")
        k = response.meta["k"]
        li_list = response.xpath("//div[@class='tousu-filter-list']//li")
        for li in li_list:
            item = TousuItem()
            detail_url = li.xpath("./a/@href").get()
            # item["brand"] = k
            # print(detail_url)
            # print("*"*100)
            item["csName"] = self.brand_dic[k]
            item["detail_url"] = detail_url
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail_url,
                meta={"item": item},
                headers=self.headers
            )

        next_url = response.xpath("//a[@class='page next']/@href").get()
        if next_url:
            self.page_num += 1
            if self.page_num < 3:
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse,
                    headers=self.headers,
                    meta={"k": k}
                )
            else:
                pass

    def parse_detail_url(self, response):
        item = response.meta["item"]
        item["brand"] = response.xpath("//div[@class='container breadnav']/a[3]/text()").get()
        item["series"] = response.xpath("//div[@class='container breadnav']/a[4]/text()").get()
        tousu_date = \
        response.xpath("//div[@class='complaints-appeal-info']//p[contains(text(),'投诉时间')]/text()").get().split("：")[1]

        for k, v in self.month_list.items():
            tousu_date = tousu_date.replace(k, v).replace(',', '') if k in tousu_date else tousu_date
        if 'M' in tousu_date:
            s = tousu_date.split(' ')
            date_tmp = f"{s[2]}-{s[0]}-{s[1]} {s[3]}"
            item["tousu_date"] = str(datetime.strptime(date_tmp, "%Y-%m-%d %H:%M:%S"))
        else:
            item["tousu_date"] = tousu_date
        item["introduct"] = \
        response.xpath("//div[@class='complaints-appeal-info']//p[contains(text(),'诉求问题')]/text()").get().split("：")[1]
        item["dataSource"] = "汽车消费网"
        item["grabtime"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item["status"] = item["detail_url"] + '-' + str(item["series"]) + '-' + str(item["brand"])
        # item[""] = response.xpath("").get()
        yield item
        # print(item)
