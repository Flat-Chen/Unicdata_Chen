import logging
import random
import re
import time
import pymysql
import requests
import scrapy
from fontTools.ttLib import TTFont
from ..proxy import get_Proxy, User_AgentMiddleware
from ..font import get_be_p1_list, get_map1

from ..items import LuntanItem_Dazhogn


class AutohomeLuntanLostSpider(scrapy.Spider):
    name = 'autohome_luntan_lost'
    allowed_domains = ['autohome.com.cn']

    # start_urls = ['http://autohome.com.cn/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeLuntanLostSpider, self).__init__(**kwargs)
        self.num = 0
        self.counts = 0
        self.word_list = ['呢', '近', '八', '着', '更', '短', '三', '少', '是', '大', '好', '上', '十', '低', '不', '的', '六', '很', '坏',
                          '长',
                          '右',
                          '高', '四', '五', '一', '二', '了', '下', '左', '得', '多', '远', '七', '九', '地', '小', '和',
                          '矮']
        self.font_map = {}
        self.headers = {'Referer': 'https://club.autohome.com.cn/',
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': "192.168.1.94",
        'MYSQL_USER': "dataUser94",
        'MYSQL_PWD': "c",
        'MYSQL_PORT': 3306,
        'MYSQL_DB': "saicnqms",
        'MYSQL_TABLE': "luntan_all_copy_lost",
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'luntan',
        'MONGODB_COLLECTION': 'autohome_luntan_lost',
        'CONCURRENT_REQUESTS': 64,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOAD_TIMEOUT': 6,
        # 'RETRY_ENABLED': True,
        # 'RETRY_TIMES': 1,
        # 'COOKIES_ENABLED': True,
        # 'REDIS_URL': 'redis://192.168.1.241:6379/14',
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'luntan.middlewares.LuntanProxyMiddleware': 400,
        #     'luntan.middlewares.LuntanUserAgentMiddleware': 100,
        # },
        # 'ITEM_PIPELINES': {
        'luntan.pipelines.LuntanPipeline': 300,
        #     'luntan.pipelines.RenameTable': 299
        # },
    }

    def start_requests(self):
        self.be_p1 = get_be_p1_list()
        conn = pymysql.connect(
            host='192.168.1.94',
            user='dataUser94',
            password='94dataUser@2020',
            db='saicnqms',
            charset='utf8'
        )
        cur = conn.cursor()
        sql_countAll = "select tiezi_url from chaji_url"
        cur.execute(sql_countAll)
        # print(cur.fetchall())
        countAll = cur.fetchall()
        for urls in countAll:
            yield scrapy.Request(url=urls[0], headers=self.headers, meta={'url': urls[0]})

    def parse(self, response):
        if 'safety' in response.url:
            print('！！！！！！！！！！！！出现了验证码！！！！！！！！！！')
            print('！！！！！！！！！！！！重试这个url！！！！！！！！！！！')
            retry_url = response.meta.get('url')
            yield scrapy.Request(url=retry_url, headers=self.headers, meta={'url': retry_url}, callback=self.parse)
        TFF_text_url = response.xpath("//style[@type='text/css']/text()").extract_first()
        url = re.findall(r"format\('embedded-opentype'\),url\('(.*?)'\) format\('woff'\)", TFF_text_url)
        if url == []:
            return
        if "k3.autoimg.cn" in url[0]:
            font_map = self.text_ttf("https:" + url[0])
        else:
            font_map = self.text_ttf("https://k3.autoimg.cn" + url[0])
        if font_map == 0:
            return
        item = LuntanItem_Dazhogn()
        item["information_source"] = 'autohome'
        item["brand"] = None
        item["factory"] = None
        item["title"] = response.xpath("//div[@id='consnav']/span[4]/text()").extract_first()
        item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["parsetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 处理content
        content_list = response.xpath("//div[@class='conttxt']")
        content_list = content_list.xpath("string(.)").extract()
        # print(content_list)
        item["content"] = ""
        for content in content_list:
            if content == '':
                continue
            else:
                item["content"] += content.strip("\n").strip()
        for font in font_map:
            old = (r"\u" + font["key"].strip("uni").lower())
            item["content"] = re.sub(old, font["value"], item["content"])
        # print(item["content"])
        item["url"] = response.url
        item["user_name"] = response.xpath("//ul[@class='maxw']/li/a/@title").extract_first()
        item["posted_time"] = response.xpath(
            "//span[contains(text(),'发表于')]/following-sibling::span[1]/text()").extract_first()
        item["user_car"] = response.xpath("//div[@class='consnav']/span[2]/a/text()").extract_first().strip("论坛")
        province = response.xpath("//a[@title='查看该地区论坛']/text()").extract_first().split()
        if len(province) == 2:
            item["province"] = province[0]
            item["region"] = province[1]
        else:
            item["province"] = province[0]
            item["region"] = None
        try:
            tieziid = re.findall(r"/(\d*)-1.html", response.url)[0]
        except:
            item["click_num"] = 0
        else:
            item["click_num"] = self.get_click_num(tieziid)
        item["reply_num"] = response.xpath("//font[@id='x-replys']/text()").extract_first()
        item["statusplus"] = str(item["user_name"]) + str(item["title"]) + str(item["posted_time"]) + str(
            item["province"]) + str(item["brand"]) + str(item["click_num"]) + str(item["reply_num"]) + str(17)
        item["content_num"] = response.xpath("//a[@title='查看']/text()").extract_first().split("帖")[0]
        if item["content"] == "":
            return
        else:
            print('````````````````````````' + str(self.num) + '``````````````````````')
            self.num = self.num + 1
            yield item

    def text_ttf(self, url):
        # print(os.listdir())
        # proxy = get_Proxy()
        # proxy = {
        #     "http": "http://" + proxy,
        #     "https": "https://" + proxy
        # }
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

    def get_click_num(self, data):
        url = "https://clubajax.autohome.com.cn/Detail/LoadX_Mini?topicId={}".format(data)

        text = requests.get(url=url, headers=self.headers).json()
        try:
            a = text["topicClicks"]["Views"]
        except:
            a = 0
        return a
