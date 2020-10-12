# -*- coding: utf-8 -*-
import scrapy
import time
import json
import io
import os
import scrapy
from carbuisness_new.items import JzgPriceItem
import time
# from scrapy.utils.project import get_project_settings
import logging
import json
import re
import requests
# import MySQLdb
import pymysql
import pymongo
import datetime
import pytesseract
from PIL import Image
from scrapy_redis.utils import bytes_to_str


# from .item import JzgTestSpider Item


class JzgTestSpider(scrapy.Spider):
    name = 'jzg_test'
    allowed_domains = ['appraise.jingzhengu.com']

    # start_urls = ['http://appraise.jingzhengu.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(JzgTestSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': "192.168.1.94",
        # 'MONGODB_SERVER': "127.0.0.1",
        'MONGODB_DB': 'residual_value',
        'MONGODB_COLLECTION': 'jzg_price_new',
        'CrawlCar_Num': 800000,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'REDIS_URL': 'redis://192.168.1.241:6379',
        # 'DUPEFILTER_CLASS': 'None',
        # 'SCHEDULER': 'None',
    }

    def start_requests(self):
        url = 'https://www.baidu.com/'
        yield scrapy.Request(url=url)
        # yield scrapy.FormRequest(method="post", url="http://common.jingzhengu.com/area/getProvList")

    def parse(self, response):
        formdata = {
            "sourcetype": "3",
            "regdate": "2019-12-1",
            "cityname": 'shanghai',
            "CityId": '2401',
            "styleid": '10009507',
            "uid": "0",
            "op": "GetValuationInfo",
            "mileage": '20000',
            # "sign": "27B900C60B10581444D6F55126074414"
        }
        # print(formdata)
        url_sell = 'http://appraise.jingzhengu.com/sale-s10009507-r2019-10-1-m20000-c2401-y-j-h'
        url_buy = 'http://appraise.jingzhengu.com/buy-s10009507-r2019-10-1-m20000-c2401-y-j-h'

        # url_sell = "http://appraise.jingzhengu.com/sale-s%s-r%s-m%s-c%s-y-j-h" % (
        #     formdata['styleid'], formdata['regdate'], formdata['mileage'], formdata['CityId'])
        # url_buy = "http://appraise.jingzhengu.com/buy-s%s-r%s-m%s-c%s-y-j-h" % (
        #     formdata['styleid'], formdata['regdate'], formdata['mileage'], formdata['CityId'])
        # print(url)
        yield scrapy.Request(url=url_sell, meta=dict({"type": "sell"}, **formdata), callback=self.parse_price)
        yield scrapy.Request(url=url_buy, meta=dict({"type": "buy"}, **formdata), callback=self.parse_price)

    def parse_img(self, url, status):

        date_str = time.strftime('%Y-%m-%d', time.localtime())
        img_res = requests.get(url=url, headers={"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}).content
        image = Image.open(io.BytesIO(img_res))


        # img_res = requests.request("get", url=url, headers={
        #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"})
        # with open("blm/img_temp/%s.jpg" % (status), "ab") as f:
        #     f.write(img_res.content)
        #     f.close()

        try:
            # img = Image.open("blm/img_temp/%s.jpg" % (status))
            # img_str = pytesseract.image_to_string(img)
            img_str = pytesseract.image_to_string(image)
            print(re.findall("^\d+\.\d{2}", img_str)[0])
            # os.remove("blm/img_temp/%s.jpg" % status)
        except Exception as e:
            logging.log(msg=str(e), level=logging.INFO)
            # os.remove("blm/img_temp/%s.jpg" % status)
            return 0
        return re.findall("^\d+\.\d{2}", img_str)[0]

    def parse_price(self, response):

        # print(response.text)
        # res = json.loads(response.text)
        item = JzgPriceItem()
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        # item['brandid'] = res["MakeId"]
        # item['familyid'] = res["ModelId"]
        item['modelid'] = response.meta["styleid"]
        # item['brandname'] = res["MakeName"]
        # item['familyname'] = res["ModelName"]
        # item['model_full_name'] = res["ModelFullName"]
        # item['HBBZ'] = res["HBBZ"]
        # item['RegDateTime'] = res["RegDateTime"]
        item['RegDate'] = response.meta["regdate"]
        # item['MarketMonthNum'] = res["MarketMonthNum"]
        item['Mileage'] = response.meta["mileage"]
        # item['ProvId'] = res["ProvId"]
        # item['ProvName'] = res["ProvName"]
        item['CityId'] = response.meta["CityId"]
        item['CityName'] = response.meta["cityname"]
        # item['NowMsrp'] = res["NowMsrp"]
        # item['C2BALowPrice'] = res["C2BALowPrice"]
        # item['C2BAMidPrice'] = res["C2BAMidPrice"]
        # item['C2BAUpPrice'] = res["C2BAUpPrice"]
        # item['C2BBLowPrice'] = res["C2BBLowPrice"]
        # item['C2BBMidPrice'] = res["C2BBMidPrice"]
        # item['C2BBUpPrice'] = res["C2BBUpPrice"]
        # item['C2BCLowPrice'] = res["C2BCLowPrice"]
        # item['C2BCMidPrice'] = res["C2BCMidPrice"]
        # item['C2BCUpPrice'] = res["C2BCUpPrice"]
        # item['C2CALowPrice'] = res["C2CALowPrice"]
        # item['C2CAMidPrice'] = res["C2CAMidPrice"]
        # item['C2CAUpPrice'] = res["C2CAUpPrice"]
        # item['C2CBLowPrice'] = res["C2CBLowPrice"]
        # item['C2CBMidPrice'] = res["C2CBMidPrice"]
        # item['C2CBUpPrice'] = res["C2CBUpPrice"]
        # item['C2CCLowPrice'] = res["C2CCLowPrice"]
        # item['C2CCMidPrice'] = res["C2CCMidPrice"]
        # item['C2CCUpPrice'] = res["C2CCUpPrice"]
        # item['PriceLevel'] = res["PriceLevel"]
        # item['BaoZhilvRank'] = res["BaoZhilvRank"]
        # item['BaoZhilvCityId'] = res["BaoZhilvCityId"]
        # item['BaoZhilvCityName'] = res["BaoZhilvCityName"]
        # item['BaoZhilvLevel'] = res["BaoZhilvLevel"]
        # item['BaoZhilvLevelName'] = res["BaoZhilvLevelName"]
        # item['BaoZhilvPercentage ']= res["BaoZhilvPercentage"]
        # item['maxPrice'] = res["maxPrice"]
        # item['minLoanRate'] = res["minLoanRate"]
        # item['ShareUrl'] = res["ShareUrl"]
        # item['PlatNumber'] = res["PlatNumber"]
        item['type'] = response.meta['type']

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

        print(item)
        # yield item
