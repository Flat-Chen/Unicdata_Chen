# -*- coding: utf-8 -*-
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
from pprint import pprint
from scrapy_redis.utils import bytes_to_str
import redis

website = 'jzg_price'
from scrapy_redis.spiders import RedisSpider

pool = redis.ConnectionPool(host='192.168.1.241', port=6379, db=0)
con = redis.Redis(connection_pool=pool)


# class CarSpider(scrapy.Spider):
class CarSpider(RedisSpider):
    name = website
    start_urls = []
    redis_key = "jzg_price:start_urls"

    def __init__(self, **kwargs):
        super(CarSpider, self).__init__(**kwargs)
        self.c = con.client()
        self.counts = 0
        self.city_count = 0
        self.city_dic = {101: '合肥',
 102: '安庆',
 103: '蚌埠',
 104: '巢湖',
 105: '池州',
 106: '阜阳',
 107: '淮北',
 108: '淮南',
 109: '六安',
 110: '马鞍山',
 113: '铜陵',
 114: '芜湖',
 115: '宣城',
 116: '滁州',
 118: '黄山',
 120: '宿州',
 125: '亳州',
 201: '北京',
 301: '福州',
 302: '厦门',
 303: '龙岩',
 305: '漳州',
 306: '莆田',
 307: '泉州',
 314: '南平',
 315: '宁德',
 318: '三明',
 401: '兰州',
 402: '定西',
 405: '平凉',
 409: '酒泉',
 410: '张掖',
 411: '庆阳',
 412: '武威',
 415: '天水',
 416: '嘉峪关',
 417: '金昌',
 418: '白银',
 421: '陇南',
 422: '甘南',
 501: '广州',
 502: '深圳',
 503: '珠海',
 504: '东莞',
 505: '中山',
 507: '汕头',
 510: '潮州',
 511: '韶关',
 513: '湛江',
 514: '肇庆',
 515: '茂名',
 516: '梅州',
 518: '佛山',
 520: '惠州',
 521: '江门',
 522: '揭阳',
 524: '清远',
 528: '云浮',
 532: '阳江',
 535: '河源',
 552: '汕尾',
 601: '南宁',
 602: '柳州',
 603: '桂林',
 604: '北海',
 605: '百色',
 606: '贺州',
 607: '河池',
 608: '贵港',
 610: '玉林',
 612: '钦州',
 613: '梧州',
 615: '防城港',
 619: '来宾',
 621: '崇左',
 701: '贵阳',
 702: '遵义',
 705: '安顺',
 708: '六盘水',
 714: '黔东南',
 715: '黔南',
 717: '毕节',
 718: '黔西南',
 719: '铜仁',
 801: '海口',
 803: '三亚',
 809: '洋埔',
 810: '琼北',
 811: '琼南',
 901: '石家庄',
 902: '唐山',
 903: '邢台',
 905: '秦皇岛',
 906: '廊坊',
 907: '邯郸',
 908: '衡水',
 909: '沧州',
 910: '保定',
 911: '张家口',
 912: '承德',
 1001: '郑州',
 1002: '洛阳',
 1003: '周口',
 1004: '信阳',
 1005: '新乡',
 1006: '商丘',
 1007: '三门峡',
 1008: '濮阳',
 1009: '南阳',
 1010: '漯河',
 1011: '焦作',
 1013: '开封',
 1014: '安阳',
 1015: '德州',
 1016: '鹤壁',
 1018: '平顶山',
 1021: '驻马店',
 1023: '许昌',
 1101: '哈尔滨',
 1102: '大庆',
 1103: '齐齐哈尔',
 1104: '鹤岗',
 1106: '佳木斯',
 1107: '鸡西',
 1108: '牡丹江',
 1109: '七台河',
 1112: '伊春',
 1113: '黑河',
 1123: '双鸭山',
 1131: '绥化',
 1136: '大兴安岭',
 1201: '武汉',
 1202: '十堰',
 1203: '襄阳',
 1204: '随州',
 1207: '宜昌',
 1208: '黄石',
 1209: '荆门',
 1210: '荆州',
 1216: '鄂州',
 1217: '咸宁',
 1229: '孝感',
 1236: '黄冈',
 1301: '长沙',
 1302: '郴州',
 1303: '常德',
 1304: '衡阳',
 1305: '怀化',
 1306: '娄底',
 1307: '株洲',
 1308: '岳阳',
 1309: '湘潭',
 1310: '邵阳',
 1312: '永州',
 1313: '益阳',
 1315: '张家界',
 1333: '湘西',
 1401: '长春',
 1402: '吉林',
 1403: '通化',
 1405: '辽源',
 1406: '白山',
 1412: '白城',
 1425: '松原',
 1428: '延边',
 1501: '南京',
 1502: '苏州',
 1503: '无锡',
 1505: '常州',
 1507: '淮安',
 1510: '连云港',
 1511: '南通',
 1512: '盐城',
 1513: '扬州',
 1515: '镇江',
 1517: '泰州',
 1518: '徐州',
 1520: '宿迁',
 1601: '南昌',
 1602: '上饶',
 1603: '萍乡',
 1604: '新余',
 1605: '宜春',
 1606: '九江',
 1607: '赣州',
 1609: '吉安',
 1612: '景德镇',
 1613: '抚州',
 1615: '鹰潭',
 1616: '四平',
 1701: '沈阳',
 1702: '丹东',
 1703: '抚顺',
 1704: '阜新',
 1705: '葫芦岛',
 1707: '朝阳',
 1708: '大连',
 1709: '本溪',
 1710: '鞍山',
 1711: '锦州',
 1713: '辽阳',
 1714: '营口',
 1716: '盘锦',
 1717: '铁岭',
 1801: '呼和浩特',
 1802: '包头',
 1803: '赤峰',
 1804: '通辽',
 1805: '乌海',
 1808: '鄂尔多斯',
 1812: '呼伦贝尔',
 1814: '兴安盟',
 1824: '巴彦淖尔',
 1825: '乌兰察布',
 1829: '锡林郭勒',
 1830: '阿拉善盟',
 1901: '银川',
 1902: '吴忠',
 1903: '固原',
 1905: '石嘴山',
 1907: '中卫',
 2001: '西宁',
 2023: '海北',
 2024: '黄南',
 2025: '果洛',
 2026: '玉树',
 2027: '海西',
 2029: '海东',
 2030: '海南',
 2101: '济南',
 2102: '青岛',
 2103: '烟台',
 2104: '威海',
 2105: '潍坊',
 2106: '泰安',
 2107: '枣庄',
 2109: '淄博',
 2110: '东营',
 2112: '菏泽',
 2113: '滨州',
 2114: '聊城',
 2117: '临沂',
 2118: '济宁',
 2120: '日照',
 2132: '莱芜',
 2201: '太原',
 2202: '大同',
 2203: '晋城',
 2204: '晋中',
 2205: '临汾',
 2206: '长治',
 2207: '运城',
 2210: '忻州',
 2218: '阳泉',
 2219: '朔州',
 2227: '吕梁',
 2301: '西安',
 2302: '咸阳',
 2303: '渭南',
 2304: '榆林',
 2305: '宝鸡',
 2306: '安康',
 2307: '汉中',
 2308: '延安',
 2310: '铜川',
 2313: '商洛',
 2401: '上海',
 2501: '成都',
 2502: '绵阳',
 2503: '遂宁',
 2504: '攀枝花',
 2506: '宜宾',
 2507: '雅安',
 2508: '自贡',
 2509: '资阳',
 2510: '广元',
 2511: '德阳',
 2512: '乐山',
 2513: '南充',
 2514: '眉山',
 2516: '巴中',
 2517: '泸州',
 2519: '内江',
 2530: '广安',
 2532: '达州',
 2535: '阿坝',
 2536: '甘孜',
 2537: '凉山',
 2601: '天津',
 2701: '拉萨',
 2703: '日喀则',
 2704: '山南',
 2705: '那曲',
 2707: '阿里',
 2709: '昌都',
 2710: '林芝',
 2801: '乌鲁木齐',
 2803: '克拉玛依',
 2821: '博尔塔拉',
 2822: '巴音郭楞',
 2823: '伊犁',
 2828: '喀什',
 2829: '阿克苏',
 2830: '和田',
 2831: '塔城',
 2832: '吐鲁番',
 2833: '哈密',
 2834: '阿勒泰',
 2835: '新疆克州',
 2901: '昆明',
 2902: '玉溪',
 2903: '曲靖',
 2907: '保山',
 2911: '临沧',
 2914: '文山',
 2915: '西双版纳',
 2918: '昭通',
 2922: '丽江',
 2923: '红河',
 2925: '德宏',
 2927: '怒江',
 2928: '迪庆',
 2929: '普洱',
 3001: '杭州',
 3002: '宁波',
 3003: '温州',
 3005: '嘉兴',
 3006: '金华',
 3009: '丽水',
 3011: '湖州',
 3012: '衢州',
 3015: '台州',
 3016: '绍兴',
 3020: '舟山',
 3101: '重庆',
 419000: '河南直辖',
 422800: '恩施',
 429000: '湖北直辖',
 469000: '海南直辖',
 532300: '楚雄',
 532900: '大理',
 622900: '临夏',
 652300: '昌吉',
 659000: '新疆直辖'}


    # def make_request_from_data(self, data):
    #     """Returns a Request instance from data coming from Redis.
    #     By default, ``data`` is an encoded URL. You can override this method to
    #     provide your own message decoding.
    #     Parameters
    #     ----------
    #     data : bytes
    #         Message from redis.
    #     """
    #     # 重写make_request_from_data函数
    #     # 读取redis_key 发送post请求 返回request对象
    #     url = bytes_to_str(data, self.redis_encoding)
    #     # print(url)
    #     # print("*" * 100)
    #     return scrapy.FormRequest(method="post", url=url)


    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': "192.168.1.94",
        # 'MONGODB_SERVER': "127.0.0.1",
        'MONGODB_DB': 'residual_value',
        'MONGODB_COLLECTION': 'jzg_price_new',
        'CrawlCar_Num': 800000,
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'REDIS_URL': 'redis://192.168.1.241:6379/0'
    }


    # def start_requests(self):
    #     yield scrapy.FormRequest(method="post", url="http://common.jingzhengu.com/area/getProvList", dont_filter=True)
    #
    # def parse(self, response):
    #     provs = json.loads(response.text)
    #     for prov in provs["list"]:
    #         yield scrapy.FormRequest(url='http://common.jingzhengu.com/area/getCityListByProvId',
    #                                  formdata={"provId": str(prov["areaId"])}, callback=self.parse_city)
    #
    # def parse_city(self, response):
    #     cities = json.loads(response.text)
    #     final_city_list = {}
    #     for city in cities["list"]:
    #         # if city["areaName"] in citylist:
    #         final_city_list[city["areaId"]] = city["areaName"]
    #
    #     self.city_count += len(final_city_list)
    #     print(self.city_count)
    #     # print(final_city_list)
    #
    #     print("*"*100)
    #     self.city_dic = {**self.city_dic, **final_city_list}
    #     pprint(self.city_dic)



    def parse(self, response):

        item = JzgPriceItem()
        styleid = re.search(r'-s(.*?)-', response.url).group(1)
        regdate = re.search(r'-r(.*?)-m', response.url).group(1)
        mileage = re.search(r'-m(.*?)-c', response.url).group(1)
        CityId = re.search(r'-c(.*?)-', response.url).group(1)
        type = re.search(r'com/(.*?)-s', response.url).group(1)
        cityname = self.city_dic[int(CityId)]

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
        list_len = self.c.llen('jzg_price:start_urls')
        if list_len > 0:
            start_url = self.c.lpop('jzg_price:start_urls')
            start_url = bytes.decode(start_url)
            yield scrapy.Request(
                url=start_url,
                callback=self.parse,
            )

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