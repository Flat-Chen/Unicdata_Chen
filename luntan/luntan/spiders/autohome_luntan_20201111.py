import logging
import random
import re
import time
import pymysql
import requests
import pymongo
import scrapy
from pandas import DataFrame
from fontTools.ttLib import TTFont
from ..proxy import get_Proxy, User_AgentMiddleware
from ..font import get_be_p1_list, get_map1
from ..items import LuntanItem_Dazhogn


class AutohomeLuntan20201111Spider(scrapy.Spider):
    name = 'autohome_luntan_20201111'

    # allowed_domains = ['autohome.com.cn']

    # start_urls = ['http://autohome.com.cn/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeLuntan20201111Spider, self).__init__(**kwargs)
        self.num = 1
        self.counts = 0
        self.word_list = ['呢', '近', '八', '着', '更', '短', '三', '少', '是', '大', '好', '上', '十', '低', '不', '的', '六', '很', '坏',
                          '长',
                          '右',
                          '高', '四', '五', '一', '二', '了', '下', '左', '得', '多', '远', '七', '九', '地', '小', '和',
                          '矮']
        self.font_map = {}
        self.headers = {'Referer': 'https://club.autohome.com.cn/',
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
        connection = pymongo.MongoClient('192.168.2.149', 27017)
        db = connection["luntan"]
        collection = db["autohome_luntan_url_2020_11"]
        self.collection = collection

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': "192.168.1.94",
        'MYSQL_USER': "dataUser94",
        'MYSQL_PWD': "94dataUser@2020",
        'MYSQL_PORT': 3306,
        'MYSQL_DB': "saicnqms",
        'MYSQL_TABLE': "luntan_all_copy",
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'luntan',
        'MONGODB_COLLECTION': 'luntan_autohome_lost4',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOAD_TIMEOUT': 10,
        # 'RETRY_ENABLED': True,
        # 'RETRY_TIMES': 1,
        # 'COOKIES_ENABLED': True,
        # 'REDIS_URL': 'redis://192.168.1.241:6379/14',
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'luntan.middlewares.LuntanProxyMiddleware': 400,
        #     'luntan.middlewares.LuntanUserAgentMiddleware': 100,
        #     'luntan.middlewares.MyproxiesSpiderMiddleware': 200,
        # },
        # 'ITEM_PIPELINES': {
        'luntan.pipelines.LuntanPipeline': 300,
        #     'luntan.pipelines.RenameTable': 299
        # },
    }

    def start_requests(self):
        self.be_p1 = get_be_p1_list()
        lost_urls = self.collection.find(
            ({"$and": [{"posted_time": {'$gte': "2020-11-01"}}, {"content": None}, {"isvideo": 0}]}))
        # lost_urls = self.collection.find({"posted_time": {'$gte': "2020-11-01"}})
        lost_urls_list = list(lost_urls)
        for lost_url in lost_urls_list:
            url = lost_url['url']
            # url = 'http://club.autohome.com.cn/bbs/thread/3101adb3de85c9c0/91759895-1.html'
            meta = {'brand': lost_url['brand'], 'factory': lost_url['factory'], 'url': url, '_id': lost_url['_id']}
            # meta = {'brand': '荣威', 'factory': '上汽乘用车', 'url': url}
            yield scrapy.Request(url=url, meta=meta, headers=self.headers, dont_filter=True)
            # break

    def parse(self, response):
        brand = response.meta['brand']
        factory = response.meta['factory']
        _id = response.meta['_id']
        if 'safety' in response.url:
            print('！！！！！！！！！！！！出现了验证码！！！！！！！！！！')
            print('！！！！！！！！！！！！重试这个url！！！！！！！！！！！')
            self.collection.update({"_id": _id}, {"$set": {'content': 'yzm'}})
            retry_url = response.meta['url']
            yield scrapy.Request(url=retry_url, headers=self.headers,
                                 meta={'url': retry_url, 'brand': brand, 'factory': factory, '_id': _id},
                                 callback=self.parse, dont_filter=True)
        else:
            # print(response.text)
            # TFF_text_url = response.xpath("//style[@type='text/css']/text()").extract_first()
            # print(TFF_text_url)
            url = re.findall(r"format\('embedded-opentype'\),url\('(.*?)'\) format\('woff'\)", response.text)
            # print(url)
            if url == []:
                print(response.url)
                print('url是空列表')
                self.collection.update({"_id": _id}, {"$set": {'content': 'url is None'}})
                return
            if "k3.autoimg.cn" in url[0]:
                font_map = self.text_ttf("https:" + url[0])
            else:
                font_map = self.text_ttf("https://k3.autoimg.cn" + url[0])
            if font_map == 0:
                print('font_map为零')
                self.collection.update({"_id": _id}, {"$set": {'content': 'font_map is None'}})
                return
            item = LuntanItem_Dazhogn()
            item["information_source"] = 'autohome'
            item["brand"] = brand
            item["factory"] = factory
            try:
                item["title"] = re.findall(r'<title>(.*?)</title>', response.text)[0]
            except:
                self.collection.update({"_id": _id}, {"$set": {'content': 'Title is None'}})
            item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["parsetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 处理content
            content_list = response.xpath("//div[@class='tz-paragraph']")
            content_list = content_list.xpath("string(.)").extract()
            # print(content_list)
            item["content"] = ""
            for content in content_list:
                if content == '':
                    print('内容为空 舍弃')
                    continue
                else:
                    item["content"] += content.strip("\n").strip()
            for font in font_map:
                old = (r"\u" + font["key"].strip("uni").lower())
                item["content"] = re.sub(old, font["value"], item["content"])
            # print(item["content"])
            item["url"] = response.url
            item["posted_time"] = response.xpath('//span[@class="post-handle-publish"]/strong/text()').extract_first()
            try:
                item["user_car"] = response.xpath("//div[@class='consnav']/span[2]/a/text()").extract_first().strip(
                    "论坛")
            except:
                item["user_car"] = response.xpath(
                    '//div[@class="toolbar-left-bbs fn-fl"]/a/text()').extract_first().strip(
                    "论坛")

            item["reply_num"] = response.xpath('//span[@class="post-handle-reply"]//text()').extract_first()

            item["content_num"] = response.xpath('//span[@class="post-handle-view"]//text()').extract_first()
            item["click_num"] = item["content_num"]
            # print(item)
            topicMemberId = re.findall(r'topicMemberId:(.\d*),', response.text)

            if item["content"] == "":
                print('------------------------------------------内容为空，pass-----------------------------------')
                self.collection.update({"_id": _id}, {"$set": {'content': 'Content is None'}})
            else:
                try:
                    topicMemberId = topicMemberId[0].strip()
                    uesr_url = f'https://club.autohome.com.cn/frontnc/user/getdetailusertpl/{topicMemberId}-0'
                    yield scrapy.Request(url=uesr_url, callback=self.username, meta={'item': item, '_id': _id})
                except:
                    print('------------------------------------------用户信息非AJAX，pass-----------------------------------')
                    self.collection.update({"_id": _id}, {"$set": {'content': 'UserName not AJAX'}})

    def username(self, response):
        item = response.meta.get('item')
        _id = response.meta.get('_id')
        item["user_name"] = response.xpath('//a[@class="name"]/text()').extract_first()
        # print(item['user_name'])
        province = response.xpath('//div[@class="user-profile"]/a/text()').extract_first().split()
        # print(province)
        if len(province) == 2:
            item["province"] = province[0]
            item["region"] = province[1]
        else:
            item["province"] = province[0]
            item["region"] = None
        print('````````````````````````' + str(self.num) + '``````````````````````')
        self.num = self.num + 1
        item["statusplus"] = str(item["user_name"]) + str(item["title"]) + str(item["posted_time"]) + str(
            item["province"]) + str(item["brand"]) + str(item["reply_num"]) + str(17)
        yield item
        # print(item)
        self.collection.update({"_id": _id}, {"$set": {'content': 'success'}})

    def text_ttf(self, url):
        User_Agent = {'User-Agent': User_AgentMiddleware.get_ug()}
        try:
            text = requests.get(url=url, headers=User_Agent)
        except:
            logging.log(msg='Proxy request timeout Wait for two seconds', level=logging.INFO)
            return 0
        else:
            # window
            with open("./luntan/text_dazhong1.ttf", "bw")as f:
                f.write(text.content)
            # linux
            # with open("/home/home/mywork/font/luntan/text_dazhong1.ttf", "bw")as f:
            #     f.write(text.content)
            #     window
            font = TTFont("./luntan/text_dazhong1.ttf")
            # linxu
            # font = TTFont("/home/home/mywork/font/luntan/text_dazhong1.ttf")
            # window
            font.saveXML("text_dazhong1.xml")
            # linux
            # font.saveXML("/home/home/mywork/font/luntan/text_dazhong1.xml")
            font_map = get_map1(self.be_p1, self.word_list)
            # print(font_map, "/\\" * 50)
            return font_map
