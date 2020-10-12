# -*- coding: utf-8 -*-
import scrapy
import time
import json

from tousu.items import TousuItem


class AllBrand315tousuSpider(scrapy.Spider):
    name = 'all_brand_315tousu'
    allowed_domains = ['315qc.com']

    # start_urls = ['http://315qc.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(AllBrand315tousuSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        # 'MYSQL_SERVER': '192.168.1.94',
        # 'MYSQL_USER': 'dataUser94',
        # 'MYSQL_PWD': '94dataUser@2020',
        # 'MYSQL_DB': 'tousu',
        # 'MYSQL_TABLE': 'car_tousu_all',
        # 'MONGODB_SERVER': '',
        # 'MONGODB_DB': '',
        # 'MONGODB_COLLECTION': 'all_brand_315tousu',
        "MONGODB_SERVER": "192.168.2.149",
        "MONGODB_PORT": 27017,
        "MONGODB_DB": "tousu",
        "MONGODB_COLLECTION": "quanwang_tousu",
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = "http://315qc.com/Home/Carcomplaints/index/p/1"
        yield scrapy.Request(
            url=url,
        )

    def parse(self, response):
        tr_list = response.xpath("//div[@class='tszb tipbox']//tr")
        for tr in tr_list[1:]:
            item = TousuItem()
            bugs = tr.xpath("td[5]/div/article/div")
            if bugs:
                bug_list = []
                for bug in bugs:
                    tag = bug.xpath("./i/a/text()").get()
                    content = "".join(bug.xpath("./span//text()").getall()).replace("\t", "").replace("\n", "").replace(
                        "\r", "")
                    data = tag + ':' + content
                    bug_list.append(data)
                item["bug"] = ",".join(bug_list)
            else:
                item["bug"] = None
            item["brand"] = tr.xpath("./td[2]/text()").get()
            item["series"] = tr.xpath("./td[3]/text()").get()
            item["introduct"] = tr.xpath("./td[4]//a/text()").get()
            item["detail_url"] = response.urljoin(tr.xpath("./td[4]//a/@href").get())

            item["tousu_date"] = " ".join(tr.xpath("./td[6]/span/text()").getall())
            item["dataSource"] = "315汽车网"
            item["grabtime"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            item["status"] = item["detail_url"] + '-' + str(item["series"]) + '-' + str(item["brand"])
            # print(item)
            yield item

        next_url = response.xpath("//span[contains(text(),'下一页')]/../@href").get()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                dont_filter=True
            )
        else:
            pass
