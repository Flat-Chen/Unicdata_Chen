# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
import pymysql
# from .items import AutohomeCustomPriceSpider Item


mysqldb = pymysql.connect("192.168.1.94", "dataUser94", "94dataUser@2020", "newcar_test", port=3306)
dbc = mysqldb.cursor()
sql = "select autohomeid from autohomeall"
dbc.execute(sql)
res = dbc.fetchall()


class AutohomeCustomPriceSpider(scrapy.Spider):
    name = 'autohome_custom_price'
    # allowed_domains = ['autohome.com']
    # start_urls = ['http://autohome.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeCustomPriceSpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        }

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'carbuisness',
        'MYSQL_TABLE': 'autohome_custom_price2',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'carbuisness',
        'MONGODB_COLLECTION': 'autohome_custom_price2',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 1,
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOADER_MIDDLEWARES': {
            'autohome.middlewares.ProxyMiddleware': 300,
        }

    }

    def start_requests(self):
        url = "https://www.autohome.com.cn/shanghai/"
        yield scrapy.Request(
            url=url,
            headers=self.headers
        )

    def parse(self, response):
        for row in res[100:150]:
            url = "https://jiage.autohome.com.cn/price/carlist/p-%s-1-0-0-0-0-1-110100" % row[0]

            yield scrapy.Request(
                url=url,
                meta={"autohomeid": row[0]},
                callback=self.parse_list,
                headers=self.headers
            )

    def parse_list(self, response):
        print("*" * 100)
        price_boxes = response.xpath("//*[@class='car-lists']")
        print("-" * 100)
        print(len(price_boxes))
        for box in price_boxes:
            print("*"*100)
            item = dict()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            # item['status'] = response.url + "-" + str(price_boxes.index(box))
            item['username'] = box.xpath('//*[@class="car-lists-item-use-name-detail "]/text()').extract_first()
            item['autohomeid'] = response.meta["autohomeid"]
            item['userid'] = box.xpath('//*[@class="car-lists-item-use-name-detail "]/@href').re("\d+")[0]
            item['fapiao'] = box.xpath('//*[@class="mark-receipt"]/text()').extract_first()
            brand_and_family = response.xpath("//*[@class='athm-sub-nav__car__name']/a//text()").extract()
            item['car_model'] = "".join(brand_and_family) + box.xpath('//*[@class="car-lists-item-top-middle"]/p/text()').extract_first()

            # item['guide_price'] = response.xpath("/html/ul/li[%d]/text()" % (price_boxes.index(box) + 1)).extract_first().split("-")[2].replace("'", "").replace("'", "")
            # item['total_price'] = response.xpath("/html/ul/li[%d]/text()" % (price_boxes.index(box) + 1)).extract_first().split("-")[1].replace("'", "").replace("'", "")
            # item['naked_price'] = response.xpath("/html/ul/li[%d]/text()" % (price_boxes.index(box) + 1)).extract_first().split("-")[0].replace("'", "").replace("'", "")

            item['guide_price'] = response.css('.hs_kw0_fctPrice1xE::before').get()
            item['total_price'] = response.xpath(".//span[@class='quankuan-num']/text()").get()
            item['naked_price'] = response.xpath(".//span[@class='luochejia-num']/text()").get()
            'body > article > section > div.main-container-left > ul:nth-child(10) > li > div.car-lists-item-bottom > ol > li:nth-child(3) > span.list-details > span > span > span'
            item['jiaoqiangxian'] = box.xpath('li/div[2]/ol/li[6]/span[2]/text()').extract_first()
            item['chechuanshui'] = box.xpath('li/div[2]/ol/li[4]/span[2]/text()').extract_first()
            item['shangyexian'] = box.xpath('li/div[2]/ol/li[7]/span[2]/text()').extract_first()
            item['shangpaifei'] = box.xpath('li/div[2]/ol/li[8]/span[2]/text()').extract_first()
            item['pay_mode'] = box.xpath('li/div[2]/ol/li[9]/span[2]/text()').extract_first()
            # item['promotion_set'] = "".join(box.xpath('li/div[2]/ol/li[10]/span[2]//text()').extract())
            item['buy_date'] = box.xpath('//*[@class="bought-time"]/time/text()').extract_first()
            item['buy_location'] = box.xpath('//*[@class="bought-location"]/text()').extract_first()
            item['dealer'] = box.xpath('//*[@class="business"]/a/text()').extract_first() if box.xpath('//*[@class="business"]/a') else "-"
            item['dealerid'] = box.xpath('//*[@class="business"]/a/@href').re("\d+")[0] if box.xpath('//*[@class="business"]/a') else "-"
            item['tel'] = box.xpath('//*[@class="tel-wrapper grey"]/tel/text()').extract_first() if box.xpath('//*[@class="tel-wrapper grey"]/tel') else "-"
            item['dealer_addr'] = box.xpath('//*[@class="loc-wrapper grey"]/span/text()').extract_first() if box.xpath('//*[@class="loc-wrapper grey"]/span') else "-"
            item['star_level'] = int(box.xpath('//*[@class="score-num"]/@style').re("\d+")[0])/20 if box.xpath('//*[@class="score-num"]') else "-"
            item['service_level'] = box.xpath('//*[@class="evaluate"]/text()').extract_first() if box.xpath('//*[@class="evaluate"]') else "-"
            # item['cutting_skill'] = "".join(box.xpath('li/div[2]/ol/li[11]/span[2]//text()').extract())
            item['cutting_skill'] = "-"
            item['status'] = str(item['autohomeid']) + "-" + str(item['userid']) + "-" + str(
                item['buy_location']) + "-" + str(item['buy_date']) + "-" + str(item['naked_price']) + time.strftime('%Y-%m', time.localtime())

            # print(item)
            yield item

            next_page = response.xpath("//*[@class='nextbtn iconfont iconfont-youjiantou']").get()
            if next_page:
                page_num = re.findall("\-1\-0\-0\-0\-0\-(.*?)\-110100", response.url)[0]
                next_num = int(page_num) + 1
                url = re.sub("\-1\-0\-0\-0\-0\-(.*?)\-110100", str(next_num), response.url)
                yield scrapy.Request(
                    url=url,
                    meta={"autohomeid": response.meta["autohomeid"]},
                    callback=self.parse_list,
                    headers=self.headers
                )



