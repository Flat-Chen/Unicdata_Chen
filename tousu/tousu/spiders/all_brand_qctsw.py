# -*- coding: utf-8 -*-
import scrapy
import time
import json
from tousu.items import TousuItem


class AllBrandQctswSpider(scrapy.Spider):
    name = 'all_brand_qctsw'
    allowed_domains = ['qctsw.com']
    # start_urls = ['http://qctsw.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(AllBrandQctswSpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

    is_debug = True
    custom_debug_settings = {
        # 'MYSQL_SERVER': '192.168.1.94',
        # 'MYSQL_DB': 'tousu',
        # 'MYSQL_TABLE': 'car_tousu_all',
        # 'MONGODB_SERVER': '192.168.1.94',
        # 'MONGODB_DB': 'tousu',
        # 'MONGODB_COLLECTION': 'car_tousu',
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
        url = "http://www.qctsw.com/tousu/tsSearch/0_0_0_0_0_0,0,0,0,0,0_1.html"
        yield scrapy.Request(
            url=url,
            dont_filter=True
        )

    def parse(self, response):
        li_list = response.xpath("//tr[@class='purple']/td[@class='tsTitle']/a")
        for a in li_list:
            item = TousuItem()
            detail_url = a.xpath("./@href").get()
            item["detail_url"] = 'http://www.qctsw.com/' + detail_url
            yield scrapy.Request(
                url=item["detail_url"],
                callback=self.parse_detail_url,
                meta={"item": item},
                headers=self.headers
            )
        next_url = response.xpath("//*[contains(text(),'下一页')]/@href").get()
        if next_url:
            next_url = response.urljoin(response.xpath("//*[contains(text(),'下一页')]/@href").get())
            yield scrapy.Request(
                    url=next_url,
                    callback=self.parse,
                    headers=self.headers,
                    dont_filter=True
                )

    def parse_detail_url(self, response):
        item = response.meta["item"]
        item["brand"] = response.xpath("//*[contains(text(),'投诉品牌')]/following-sibling::td[1]/a[1]/text()").get()
        tousu_date = response.xpath("//*[contains(text(),'投诉时间')]/following-sibling::td[1]/text()").get()
        if tousu_date:
            item["tousu_date"] = tousu_date.replace("\r", "").replace("\n", "").replace("\t", "")
        else:
            item["tousu_date"] = None
        item["introduct"] = ",".join([x for x in response.xpath("//*[contains(text(),'投诉问题')]/following-sibling::td[1]//text()").getall() if "\n" not in x])
        item["series"] = response.xpath("//*[contains(text(),'投诉品牌')]/following-sibling::td[1]/a[2]/text()").get()
        item["model"] = response.xpath("//*[contains(text(),'所属类型')]/following-sibling::td[1]//text()").getall()[1]
        item["dataSource"] = "汽车投诉网"
        item["grabtime"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item["status"] = item["detail_url"] + '-' + str(item["series"]) + '-' + str(item["brand"])

        bugs = response.xpath("//*[contains(text(),'投诉问题')]/following-sibling::td[1]/p")
        if bugs:
            bug_list = []
            for bug in bugs:
                tag = bug.xpath("./a/text()").get()
                content = bug.xpath("./a/b/text()").get()
                if content and tag:
                    data = f"{tag}:{content}"
                else:
                    data = f"{tag}"
                bug_list.append(data)
            item["bug"] = ",".join(bug_list)
        else:
            item["bug"] = None

        yield item
        # print(item)

