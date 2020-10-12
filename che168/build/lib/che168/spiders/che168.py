# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
import redis
import requests
from scrapy_redis.spiders import RedisSpider
from che168.items import Che168Item

pool = redis.ConnectionPool(host='192.168.1.241', port=6379, db=14)
con = redis.Redis(connection_pool=pool)
# c = con.client()

website = 'che168'


class Che168Spider(RedisSpider):
    name = website
    redis_key = "che168:start_urls"

    # allowed_domains = ['che168.com']
    # start_urls = ['https://www.che168.com/dealer/243332/37441572.html?pvareaid=100519&userpid=510000&usercid=511400&offertype=0']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(Che168Spider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {'Referer': 'https://www.che168.com',
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
        self.c = con.client()

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'usedcar_update',
        'MYSQL_TABLE': 'che168_online',
        'WEBSITE': 'che168',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'usedcar_update',
        'MONGODB_COLLECTION': 'che168_online',
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'REDIS_URL': 'redis://192.168.1.241:6379/14',
        'ITEM_PIPELINES': {
            'che168.pipelines.GanjiPipeline': 300,
        },
    }

    def parse(self, response):
        # status check
        if "dealer" not in response.url:
            item = Che168Item()
            item["carid"] = re.findall(r'/(\d*).html', response.url)[0]
            item["car_source"] = "che168"
            item["grab_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["update_time"] = None
            # b = re.findall(r"(\d*)-(\d*)-(\d*)", response.xpath('//div[@class="car-address"]/text()[2]').extract_first())[0]
            item["post_time"] = response.xpath("//*[contains(text(),'发布时间')]/../text()").get()
            item["sold_date"] = None
            item["pagetime"] = "zero"
            item["parsetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["shortdesc"] = response.xpath("//h3[@class='car-brand-name']/text()").get()
            item["pagetitle"] = response.xpath('//title/text()').get().strip("")
            item["url"] = response.url
            item["newcarid"] = response.xpath('//input[@id="car_specid"]/@value').get()
            item["status"] = "sale"
            item["brand"] = response.xpath('//div[@class="bread-crumbs content"]/a[3]/text()').get().replace('二手', '')
            item["series"] = response.xpath('//div[@class="bread-crumbs content"]/a[4]/text()').get().replace('二手', '')
            item["factoryname"] = None
            item["modelname"] = response.xpath('//input[@id="car_carname"]/@value').extract_first()
            item["brandid"] = response.xpath('//input[@id="car_brandid"]/@value').extract_first()
            item["familyid"] = None
            item["seriesid"] = response.xpath('//input[@id="car_seriesid"]/@value').extract_first()
            item["body"] = None
            title = response.xpath("//title/text()").extract_first()
            relt = re.findall(r'(\d+)[\u5e74\u6b3e]', title)[0]
            item['makeyear'] = relt
            try:
                item["registeryear"] = response.xpath(
                    '//div[@class="details"]/ul/li[contains(text(),"首次上牌")]/span/text()').extract_first().split(
                    "-")[0]
            except:
                item["registeryear"] = None
            item["produceyear"] = None
            item["bodystyle"] = None
            item["level"] = response.xpath(
                '//li/span[contains(text(),"车辆级别")]/../text()').extract_first()
            item["fueltype"] = None
            item["driverway"] = response.xpath(
                '//li/span[contains(text(),"驱动方式")]/../text()').extract_first()
            try:
                item["output"] = response.xpath(
                    '//div[@class="details"]/ul/li[contains(text(),"挡位／排量")]/span/text()').extract_first().split("／")[1]
            except:
                item["output"] = None
            item["guideprice"] = None
            specid = response.xpath('//input[@id="car_specid"]/@value')
            cid = response.url.split('=')[-1]
            item['guidepricetax'] = '-'
            if specid:
                url = 'https://apiassess.che168.com/api/NewCarPriceInTax.ashx?_appid=2sc&pid=0&specid={}&cid={}&_callback=dtcommon.load4SPriceCallBack'.format(
                    specid.extract_first(), cid)
                # print(url, "*" * 50)
                res = requests.get(url)
                relt = re.findall(r'\d+\.\d+', res.text)
                if relt:
                    item['guidepricetax'] = relt[0]

            item["doors"] = None
            item["emission"] = response.xpath('//li/span[contains(text(),"排放标准")]/../text()').extract_first()
            item["gear"] = None
            try:
                item["geartype"] = \
                    response.xpath(
                        '//div[@class="details"]/ul/li[contains(text(),"挡位／排量")]/span/text()').extract_first().split(
                        "/")[0]
            except:
                item["geartype"] = None
            item["seats"] = None
            item["length"] = None
            item["width"] = None
            item["height"] = None
            item["gearnumber"] = None
            item["weight"] = None
            item["wheelbase"] = None
            item["generation"] = None
            item["fuelnumber"] = response.xpath(
                '//li/span[contains(text(),"燃油标号")]/../text()').extract_first()
            try:
                item["lwv"] = re.findall(r"(L\d)", response.xpath(
                    '//div[@id="anchor02"]/ul[@class="infotext-list fn-clear"]/li[1]/text()').extract_first())[0]
            except:
                item["lwv"] = None
            try:
                lwvnumber = re.findall(r"[[A-Z](\d?)", item["lwv"])[0]
            except:
                lwvnumber = None
            item["lwvnumber"] = lwvnumber
            item["maxnm"] = None
            item["maxpower"] = None
            try:
                item["maxps"] = re.findall(r"(\d*)马力", response.xpath(
                    '//div[@id="anchor02"]/ul[@class="infotext-list fn-clear"]/li[1]/text()').extract_first())[0]
            except:
                item["maxps"] = None
            item["frontgauge"] = None
            item["compress"] = None
            item["registerdate"] = response.xpath(
                '//div[@class="details"]/ul/li[contains(text(),"首次上牌")]/span/text()').extract_first()
            item["years"] = None
            item["paytype"] = None
            try:
                item["price1"] = response.xpath('//div[@class="car-price"]/ins/text()').extract_first().strip(
                    "¥").strip(
                    " ")
            except:
                item["price1"] = None
            item["pricetag"] = None
            item["mileage"] = response.xpath(
                '//div[@class="details"]/ul/li[contains(text(),"行驶里程")]/span/text()').extract_first()

            item["usage"] = response.xpath('//li/span[contains(text(),"途")]/../text()').extract_first()
            item["color"] = response.xpath(
                '//li/span[contains(text(),"颜　　色")]/../text()').extract_first()
            item["city"] = \
                re.findall(r"city=(.*);", response.xpath('//meta[@name="location"]/@content').extract_first())[0]
            item["prov"] = re.findall(r"province=([\s\S]*?);city",
                                      response.xpath('//meta[@name="location"]/@content').extract_first())[0]
            item["guarantee"] = str(response.xpath('//div[@class="commitment-tag"]/ul/li/span/text()').extract())
            try:
                item["totalcheck_desc"] = response.xpath('//*[@id="remark_small"]/div/text()[1]').extract_first().split(
                    "\n")
            except:
                item["totalcheck_desc"] = None
            totalcheck_desc = ""
            try:
                for i in item["totalcheck_desc"]:
                    totalcheck_desc = totalcheck_desc + i
            except:
                pass
            item["totalcheck_desc"] = totalcheck_desc
            item["totalgrade"] = None
            item["contact_type"] = response.xpath(
                '//div[@class="merchants-title"]/span[@class="name"]/text()').extract_first()
            item["contact_name"] = response.xpath('//input[@id="car_LinkmanName"]/@value').extract_first()
            item["contact_phone"] = None
            item["contact_address"] = response.xpath('//p[@class="address"]/text()').extract_first()
            item["contact_company"] = response.xpath('//div[@class="merchants-title"]/text()').extract_first()
            item["contact_url"] = response.xpath('//p[@class="btn-wrap"]/a/@href').extract_first()
            item["change_date"] = None
            item["change_times"] = \
                response.xpath(
                    '//li/span[contains(text(),"过户次数")]/following-sibling::span/text()').extract_first().split(
                    "次")[0]
            item["insurance1_date"] = None
            item["insurance2_date"] = None
            item["hascheck"] = None
            item["repairinfo"] = response.xpath('//li/span[contains(text(),"维修保养")]/../text()').extract_first()
            item["yearchecktime"] = response.xpath('//li/span[contains(text(),"年检到期")]/../text()').extract_first()
            item["carokcf"] = None
            item["carcard"] = None
            item["carinvoice"] = '测试'
            item["accident_desc"] = None
            item["accident_score"] = None
            item["outer_desc"] = None
            item["safe_desc"] = None
            item["outer_score"] = None
            item["inner_desc"] = None
            item["inner_score"] = None

            item["road_desc"] = None
            item["safe_score"] = None
            item["road_desc"] = None
            item["road_score"] = None
            item["lastposttime"] = None
            item["newcartitle"] = None
            item["newcarurl"] = None
            item["img_url"] = response.xpath("//div[@id='focus-1']/div[@class='focusimg-pic']//img/@src").get()
            item["first_owner"] = None
            item["carno"] = response.xpath('//li[contains(text(),"所在地")]/span/text()').get()
            item["carnotype"] = None
            item["carddate"] = None
            item["changecolor"] = None
            item["outcolor"] = None
            item["innercolor"] = None
            item["desc"] = response.xpath('//div[@id="remark_full"]/div/text()').extract()
            desc = ""
            for i in item["desc"]:
                desc = desc + i + "\\"
            item["desc"] = str(desc)
            item["statusplus"] = item["url"] + "-¥" + item["price1"] + "-" + item["status"] + "-" + item[
                "pagetime"] + str(
                item["road_desc"]) + str(item["post_time"]) + str(1)
            # print(item, "--" * 50)
            yield item

            next_url = self.c.lpop('che168:start_urls')
            if next_url:
                start_url = bytes.decode(next_url)
                yield scrapy.Request(
                    url=start_url,
                    callback=self.parse,
                )
        else:
            item = Che168Item()
            item["carid"] = re.findall(r'/(\d*).html', response.url)[0]
            item["car_source"] = "che168"
            item["grab_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["update_time"] = None

            item["post_time"] = response.xpath("//span[contains(text(),'发布时间')]/../text()").extract_first()
            item["sold_date"] = None
            item["pagetime"] = "zero"
            item["parsetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["shortdesc"] = \
                response.xpath('//div[@class="car-box"]/h3/text()').extract_first().strip("\r\n").strip(
                    " ").strip(
                    "\r\n")
            item["pagetitle"] = response.xpath('//title/text()').extract_first().strip("")
            item["url"] = response.url
            try:
                item["newcarid"] = response.xpath('//input[@id="car_specid"]/@value').extract_first()
            except:
                item["newcarid"] = None
            item["status"] = "sale"
            item["brand"] = \
                response.xpath("//div[@class='bread-crumbs content']/a[4]/text()").extract_first().split("二手")[1]
            item["series"] = \
                response.xpath("//div[@class='bread-crumbs content']/a[4]/text()").extract_first().split("二手")[1]
            item["factoryname"] = None
            item["modelname"] = response.xpath('//input[@id="car_carname"]/@value').extract_first()
            item["brandid"] = response.xpath('//input[@id="car_brandid"]/@value').extract_first()
            item["familyid"] = None
            item["seriesid"] = response.xpath('//input[@id="car_seriesid"]/@value').extract_first()
            item["body"] = None
            title = response.xpath("//title/text()").extract_first()
            relt = re.findall(r'(\d+)[\u5e74\u6b3e]', title)[0]
            item['makeyear'] = relt
            item["registeryear"] = \
                response.xpath(
                    '//p[contains(text(),"上牌时间")]/following-sibling::h4/text()').extract_first().split(
                    "-")[0]
            item["produceyear"] = None
            item["bodystyle"] = None
            item["level"] = response.xpath(
                '//li/span[contains(text(),"车辆级别")]/../text()').extract_first()
            item["fueltype"] = None
            item["driverway"] = response.xpath(
                '//li/span[contains(text(),"驱动方式")]/../text()').extract_first()
            item["output"] = response.xpath(
                '//p[contains(text(),"挡位 / 排量")]/following-sibling::h4/text()').extract_first().split("/")[1]
            item["guideprice"] = None
            specid = response.xpath('//input[@id="car_specid"]/@value')
            cid = response.url.split('=')[-1]
            item['guidepricetax'] = '-'
            if specid:
                url = 'https://apiassess.che168.com/api/NewCarPriceInTax.ashx?_appid=2sc&pid=0&specid={}&cid={}&_callback=dtcommon.load4SPriceCallBack'.format(
                    specid.extract_first(), cid)
                # print(url, "*" * 50)
                res = requests.get(url)
                relt = re.findall(r'\d+\.\d+', res.text)
                if relt:
                    item['guidepricetax'] = relt[0]
                # print(item)
            item["doors"] = None
            item["emission"] = response.xpath('//li/span[contains(text(),"排放标准")]/../text()').extract_first()
            item["gear"] = None
            try:
                item["geartype"] = \
                    response.xpath(
                        '//p[contains(text(),"挡位 / 排量")]/following-sibling::h4/text()').extract_first().split(
                        "/")[0]
            except:
                item["geartype"] = None
            item["seats"] = None
            item["length"] = None
            item["width"] = None
            item["height"] = None
            item["gearnumber"] = None
            item["weight"] = None
            item["wheelbase"] = None
            item["generation"] = None
            item["fuelnumber"] = response.xpath(
                '//li/span[contains(text(),"燃油标号")]/../text()').extract_first()
            item["lwv"] = response.xpath(
                "//span[contains(text(),'机')]/../text()").extract_first().split(" ")[2]
            try:
                lwvnumber = re.findall(r"[[A-Z](\d?)", item["lwv"])[0]
            except:
                lwvnumber = None
            item["lwvnumber"] = lwvnumber
            item["maxnm"] = None
            item["maxpower"] = None
            item["maxps"] = re.findall(r"(\d*)马力", response.xpath(
                "//span[contains(text(),'机')]/../text()").extract_first())[0]
            item["frontgauge"] = None
            item["compress"] = None
            item["registerdate"] = response.xpath(
                '//p[contains(text(),"上牌时间")]/following-sibling::h4/text()').extract_first()
            item["years"] = None
            item["paytype"] = None
            item["price1"] = response.xpath('//span[@class="price"]/text()').extract_first().strip("¥").strip(
                " ")
            item["pricetag"] = None
            item["mileage"] = response.xpath(
                "//span[contains(text(),'表显里程')]/../text()").extract_first()

            item["usage"] = None
            item["color"] = response.xpath(
                "//span[contains(text(),'车身颜色')]/../text()").extract_first()
            item["city"] = \
                re.findall(r"city=(.*);", response.xpath('//meta[@name="location"]/@content').extract_first())[0]
            item["prov"] = re.findall(r"province=([\s\S]*?);city",
                                      response.xpath('//meta[@name="location"]/@content').extract_first())[0]
            item["guarantee"] = str(response.xpath("//div[@class='car-tags tags']/i/text()").extract())
            item["totalcheck_desc"] = None
            item["totalgrade"] = None
            item["contact_type"] = response.xpath(
                "//div[@class='protarit-list']/h4/text()").extract_first()
            item["contact_name"] = response.xpath('//input[@id="car_LinkmanName"]/@value').extract_first()
            item["contact_phone"] = None
            item["contact_address"] = response.xpath("//div[@class='protarit-list']/div/text()").extract_first()
            # item["contact_company"] = response.xpath("//div[@class='protarit-list']/h4/span/text()").extract_first()
            # liangdian = str(response.xpath('//div[@class="bright-list"]//text()').extract())[1:-1].replace(r'\r\n','').strip()
            # if '    ' in liangdian:
            #     liangdian = 'null'
            # print('~~~~~~~~~~~~~', liangdian, type(liangdian))
            item["contact_company"] = '等待另外一个爬虫更新'
            item["contact_url"] = None
            item["change_date"] = None
            item["change_times"] = \
                response.xpath(
                    '//li/span[contains(text(),"过户次数")]/../text()').extract_first().split(
                    "次")[0]
            item["insurance1_date"] = None
            item["insurance2_date"] = None
            item["hascheck"] = None
            item["repairinfo"] = response.xpath('//li/span[contains(text(),"维修保养")]/../text()').extract_first()
            item["yearchecktime"] = response.xpath('//li/span[contains(text(),"年检到期")]/../text()').extract_first()
            item["carokcf"] = None
            item["carcard"] = None
            item["carinvoice"] = None
            item["accident_desc"] = None
            item["accident_score"] = None
            item["outer_desc"] = None
            item["safe_desc"] = None
            item["outer_score"] = None
            item["inner_desc"] = None
            item["inner_score"] = None
            item["road_desc"] = None
            item["safe_score"] = None
            item["road_desc"] = None
            item["road_score"] = None
            item["lastposttime"] = None
            item["newcartitle"] = None
            item["newcarurl"] = None
            item["img_url"] = response.xpath("//div[@class='swiper-slide']//img/@src").get()
            item["first_owner"] = None
            item["carno"] = response.xpath(
                "//p[contains(text(),'车辆所在地')]/following-sibling::h4[1]/text()").get()
            item["carnotype"] = None
            item["carddate"] = None
            item["changecolor"] = None
            item["outcolor"] = None
            item["innercolor"] = None
            item["desc"] = str(response.xpath('//div[@id="remark_full"]/div/text()').extract())
            item["statusplus"] = item["url"] + "-¥" + item["price1"] + "-" + item["status"] + "-" + item[
                "pagetime"] + str(
                item["road_desc"]) + str(item["post_time"]) + str(2)
            yield item
            # print(item)

            next_url = self.c.lpop('che168:start_urls')
            if next_url:
                start_url = bytes.decode(next_url)
                yield scrapy.Request(
                    url=start_url,
                    callback=self.parse,
                )
