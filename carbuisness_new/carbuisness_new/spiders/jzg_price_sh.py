# -*- coding: utf-8 -*-
import io
import scrapy
from carbuisness_new.items import JzgPriceItem
import time
import logging
import re
import requests
import pymysql
import pymongo
import pytesseract
from PIL import Image
from scrapy_redis.utils import bytes_to_str
import redis


pool = redis.ConnectionPool(host='192.168.1.241', port=6379, db=0)
con = redis.Redis(connection_pool=pool)


website = 'jzg_price_sh'
from scrapy_redis.spiders import RedisSpider


# class CarSpider(scrapy.Spider):
class CarSpider(RedisSpider):
    name = website
    start_urls = []
    redis_key = "jzg_price_sh:start_urls"

    def __init__(self, **kwargs):
        super(CarSpider, self).__init__(**kwargs)
        self.c = con.client()
        self.counts = 0
        self.city_count = 0
        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["residual_value"]
        self.collection = db["jzg_modellist2"]


    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': "192.168.1.94",
        # 'MONGODB_SERVER': "127.0.0.1",
        'MONGODB_DB': 'residual_value',
        'MONGODB_COLLECTION': 'jzg_price_test_img_2019',
        'CrawlCar_Num': 800000,
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'REDIS_URL': 'redis://192.168.1.241:6379/0'
    }

    def parse(self, response):
        item = JzgPriceItem()
        styleid = re.search(r'-s(.*?)-', response.url).group(1)
        regdate = re.search(r'-r(.*?)-m', response.url).group(1)
        mileage = re.search(r'-m(.*?)-c', response.url).group(1)
        CityId = re.search(r'-c(.*?)-', response.url).group(1)
        cityname = '上海'
        type = re.search(r'com/(.*?)-s', response.url).group(1)

        item['modelid'] = styleid
        item['RegDate'] = regdate
        item['Mileage'] = mileage
        item['CityId'] = CityId
        item['CityName'] = cityname
        item['type'] = type
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["status"] = item["RegDate"] + "-" + item["Mileage"] + "-" + item["CityId"] + "-" + item["modelid"] + "-" + \
                         item['type'] + "-" + time.strftime('%Y-%m', time.localtime())

        if item['type'] == "sell":
            item['C2BMidPrice_sell'] = response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[1]/ul/li[2]/input[@id='hdC2BMidPrice']/@value").extract_first()

            item['C2BLowPrice_sell_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[1]/ul/li[1]/span[3]/img/@src").extract_first().replace(
                "2_2", "2_1"))
            item['C2BLowPrice_sell_img'] = self.parse_img(item['C2BLowPrice_sell_img'],
                                                          item['status'] + "-" + "C2BLowPrice_sell_img")
            item['C2BUpPrice_sell_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[1]/ul/li[3]/span[3]/img/@src").extract_first().replace(
                "2_2", "2_1"))
            item['C2BUpPrice_sell_img'] = self.parse_img(item['C2BUpPrice_sell_img'],
                                                         item['status'] + "-" + "C2BUpPrice_sell_img")
            item['C2CMidPrice_sell_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[2]/ul/li[2]/span[3]/img/@src").extract_first().replace(
                "2_2", "2_1"))
            item['C2CMidPrice_sell_img'] = self.parse_img(item['C2CMidPrice_sell_img'],
                                                          item['status'] + "-" + "C2CMidPrice_sell_img")
            item['C2CLowPrice_sell_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[2]/ul/li[1]/span[3]/img/@src").extract_first().replace(
                "2_2", "2_1"))
            item['C2CLowPrice_sell_img'] = self.parse_img(item['C2CLowPrice_sell_img'],
                                                          item['status'] + "-" + "C2CLowPrice_sell_img")
            item['C2CUpPrice_sell_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[2]/ul/li[3]/span[3]/img/@src").extract_first().replace(
                "2_2", "2_1"))
            item['C2CUpPrice_sell_img'] = self.parse_img(item['C2CUpPrice_sell_img'],
                                                         item['status'] + "-" + "C2CUpPrice_sell_img")
        else:
            item['B2CMidPrice_buy_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[1]/ul/li[2]/span[3]/img/@src").extract_first().replace(
                "1_1", "2_1"))
            item['B2CMidPrice_buy_img'] = self.parse_img(item['B2CMidPrice_buy_img'],
                                                         item['status'] + "-" + "B2CMidPrice_buy_img")
            item['B2CLowPrice_buy_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[1]/ul/li[1]/span[3]/img/@src").extract_first().replace(
                "2_2", "2_1"))
            item['B2CLowPrice_buy_img'] = self.parse_img(item['B2CLowPrice_buy_img'],
                                                         item['status'] + "-" + "B2CLowPrice_buy_img")
            item['B2CUpPrice_buy_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[1]/ul/li[3]/span[3]/img/@src").extract_first().replace(
                "2_2", "2_1"))
            item['B2CUpPrice_buy_img'] = self.parse_img(item['B2CUpPrice_buy_img'],
                                                        item['status'] + "-" + "B2CUpPrice_buy_img")
            item['C2CMidPrice_buy_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[2]/ul/li[2]/span[3]/img/@src").extract_first().replace(
                "2_2", "2_1"))
            item['C2CMidPrice_buy_img'] = self.parse_img(item['C2CMidPrice_buy_img'],
                                                         item['status'] + "-" + "C2CMidPrice_buy_img")
            item['C2CLowPrice_buy_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[2]/ul/li[1]/span[3]/img/@src").extract_first().replace(
                "2_2", "2_1"))
            item['C2CLowPrice_buy_img'] = self.parse_img(item['C2CLowPrice_buy_img'],
                                                         item['status'] + "-" + "C2CLowPrice_buy_img")
            item['C2CUpPrice_buy_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[2]/ul/li[3]/span[3]/img/@src").extract_first().replace(
                "2_2", "2_1"))
            item['C2CUpPrice_buy_img'] = self.parse_img(item['C2CUpPrice_buy_img'],
                                                        item['status'] + "-" + "C2CUpPrice_buy_img")

        # print(item)
        yield item
        list_len = self.c.llen('jzg_price_sh:start_urls')
        if list_len > 0:
            start_url = self.c.lpop('jzg_price_sh:start_urls')
            start_url = bytes.decode(start_url)
            yield scrapy.Request(
                url=start_url,
                callback=self.parse,
            )





    def parse_img(self, url, status):
        # date_str = time.strftime('%Y-%m-%d', time.localtime())

        # img_res = requests.request("get", url=url, headers={
        #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"})

        # data = requests.get(url=img_url).content
        img_res = requests.get(url=url, headers={"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}).content

        image = Image.open(io.BytesIO(img_res))

        # with open("blm/img_temp/%s.jpg" % (status), "ab") as f:
        #     f.write(img_res.content)
        #     f.close()

        try:
            # img = Image.open("blm/img_temp/%s.jpg" % (status))
            # img_str = pytesseract.image_to_string(img)
            img_str = pytesseract.image_to_string(image)
            print(re.findall("^\d+\.\d{2}", img_str)[0])
            # print("*"*100)
            # os.remove("blm/img_temp/%s.jpg" % status)
        except Exception as e:
            logging.log(msg=str(e), level=logging.INFO)
            # os.remove("blm/img_temp/%s.jpg" % status)
            return 0
        return re.findall("^\d+\.\d{2}", img_str)[0]
