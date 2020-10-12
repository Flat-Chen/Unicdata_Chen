# -*- coding: utf-8 -*-
import scrapy

import time
from tousu.items import TousuItem


class QctswSpider(scrapy.Spider):
    name = 'qctsw'
    allowed_domains = ['qctsw.com']

    def __init__(self):
        super(QctswSpider, self).__init__()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        self.brand_dic = None
        self.page_num = 1

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        # 'REDIS_URL': 'redis://192.168.1.92:6379/6',
        # 'MYSQL_TABLE': 'tousu_all',
        # 'MYSQL_DB': 'saicnqms',
        # 'MYSQL_PORT': '9433',
        # 'MYSQL_SERVER': '124.77.191.6',
        # 'MYSQL_SERVER': '192.168.1.94',
        # 'MYSQL_USER': 'dataUser94',
        # 'MYSQL_PWD': '94dataUser@2020',
        # 'MYSQL_TABLE': 'qctsw',
        # 'MYSQL_DB': 'saicnqms',
        "MONGODB_SERVER": "192.168.2.149",
        "MONGODB_PORT": 27017,
        "MONGODB_DB": "tousu",
        "MONGODB_COLLECTION": "shangqi_tousu",
        'AUTOTHROTTLE_START_DELAY': 16,
        'DOWNLOAD_DELAY': 0,
    }

    def start_requests(self):
        self.brand_dic = self.settings.get("BRAND_DIC")
        for k, v in self.brand_dic.items():
            if k == '五菱汽车':
                url = f"http://www.qctsw.com/doTousu_frontSearchTousu?keyword={'五菱'}"
            else:
                url = f"http://www.qctsw.com/doTousu_frontSearchTousu?keyword={k}"
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                meta={"v": v, "k": k},
                dont_filter=True
            )

    def parse(self, response):
        v = response.meta["v"]
        k = response.meta["k"]
        li_list = response.xpath("//div[@class='tousuList']//li")
        for li in li_list:
            item = TousuItem()
            detail_url = response.urljoin(li.xpath("./h3/a/@href").get())
            item["detail_url"] = detail_url.replace('https', 'http') if 'https' in detail_url else detail_url
            item["csName"] = v
            # item["brand"] = k
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail_url,
                meta={"item": item},
                headers=self.headers
            )
        next_url = response.xpath("//*[contains(text(),'下一页')]/@href").get()

        if next_url:
            self.page_num += 1
            if self.page_num < 3:
                next_url = response.urljoin(response.xpath("//*[contains(text(),'下一页')]/@href").get())
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse,
                    meta={"v": v, "k": k},
                    headers=self.headers,
                    dont_filter=True
                )
            else:
                pass

    def parse_detail_url(self, response):
        item = response.meta["item"]
        item["brand"] = response.xpath("//*[contains(text(),'投诉品牌')]/following-sibling::td[1]/a[1]/text()").get()
        item["tousu_date"] = response.xpath(
            "//*[contains(text(),'投诉时间')]/following-sibling::td[1]/text()").get().replace("\r", "").replace("\n",
                                                                                                            "").replace(
            "\t", "")
        item["introduct"] = ",".join(
            [x for x in response.xpath("//*[contains(text(),'投诉问题')]/following-sibling::td[1]//text()").getall() if
             "\n" not in x])
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

        # item[""] = response.xpath("").get()
        # print(item)
        yield item
