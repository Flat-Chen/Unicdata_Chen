# -*- coding: utf-8 -*-
import time

import scrapy

from tousu.items import TousuItem


class A315tousuSpider(scrapy.Spider):
    name = 'a315tousu'
    allowed_domains = ['315qc.com']

    # start_urls = ['http://315qc.com/']

    def __init__(self):
        super(A315tousuSpider, self).__init__()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        self.brand_dic = None
        self.page_num = 1
        self.brand_code = {'名爵': "8305",
                 '荣威': "6875",
                 '斯柯达': "5420",
                 '大众': "8857",
                 '上汽大通': "3977",
                 '别克': "928",
                 '凯迪拉克': "17262",
                 '雪佛兰': "2486",
                 '宝骏': "914",
                 '五菱汽车': "6795",
                 '依维柯': "2652"}


    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        # 'MYSQL_TABLE': 'tousu_all',
        # 'MYSQL_DB': 'saicnqms',
        # 'MYSQL_PORT': '9433',
        # 'MYSQL_SERVER': '124.77.191.6',
        # 'MYSQL_SERVER': '192.168.1.94',
        # 'MYSQL_USER': 'dataUser94',
        # 'MYSQL_PWD': '94dataUser@2020',
        # 'REDIS_URL': 'redis://192.168.1.92:6379/6',
        # 'MYSQL_TABLE': 'a315tousu',
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
        url = "http://315qc.com/Home/Carcomplaints/index"
        for k, v in self.brand_dic.items():
            code = self.brand_code[k]
            # data = {"gjz": k}
            data = {"pinpai": code, 'chexi': '0', 'chexing': '0'}
            yield scrapy.FormRequest(
                # method="POST",
                url=url,
                formdata=data,
                headers=self.headers,
                meta={"v": v, "k": k},
                dont_filter=True
            )

    def parse(self, response):
        cs_name = response.meta["v"]
        k = response.meta["k"]
        # item = TousuItem()
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
            item["csName"] = cs_name
            item["grabtime"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            item["status"] = item["detail_url"] + '-' + str(item["series"]) + '-' + str(item["brand"])
            # print(item)
            yield item

        next_url = response.xpath("//span[contains(text(),'下一页')]/../@href").get()
        if next_url:
            self.page_num += 1
            if self.page_num < 3:
                next_url = response.urljoin(next_url)
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse,
                    meta={"v": cs_name, "k": k},
                    dont_filter=True
                )
            else:
                pass
