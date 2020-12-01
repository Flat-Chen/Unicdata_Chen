import re
import base64
import time

import pytesseract
from PIL import Image
import random
import scrapy
from gerapy_pyppeteer import PyppeteerRequest
from che300_xcx.items import Che300XcxItem


class Che300GzSpider(scrapy.Spider):
    name = 'che300_gz'
    allowed_domains = ['che300.com']

    # start_urls = ['http://che300.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(Che300GzSpider, self).__init__(**kwargs)
        self.counts = 0
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'device_id=h52ac0-418c-a1b7-10b5-b67e; pcim=e8f8f86ec7aba7e90bf67c1cddc7a6c5ef86d292; tel=17059155843; PHPSESSID=9e27a6faeeb6806f211c3270d3fcc8bb2ebf6efd; Hm_lvt_12b6a0c74b9c210899f69b3429653ed6=1605254329; Hm_lvt_f5ec9aea58f25882d61d31eb4b353550=1605254330; Hm_lvt_f33b83d5b301d5a0c3e722bd9d89acc8=1606450498; Hm_lpvt_f33b83d5b301d5a0c3e722bd9d89acc8=1606463853; spidercooskieXX12=1606463908; spidercodeCI12X3=ad337693b2ed2abd577c71c55798613c; _che300=ywBRMQDBupubEqc0KC93oGzVF%2FAAC74JclA4VUy%2BeCTEW0IQqnWHyDBaj0QYHGqjo9OPTVfuD5aaU10ycpmatzt%2FV21zMY3kN3ZP0VGyiFVlBjOSQrZ2U2zEqh7AQOaLiMT9%2B50HEWVj1zzOAv3%2BevgplR%2Bx8yi7p0Jtq%2BP6cozVx9vzxwyrYtVLFR%2By9uqyOafvU4fgP0y%2BiqXHW2jU%2F5I13cEuB9S1jMW4WyKF2pIkIjAvYAr1RK0KUZEKizYG1onChuYSQ1oym7Y7Gh1%2Fne%2FKUNpeiG0CqE7%2FkuKwovppqPF8N%2BHkDHUMh3N5cREnaq57Z69fvxBP4OQGlrkHZLbZcED1zAi%2BDecOolcY3Qsn%2FT9xyBbHfIuB%2FkhNICUmjuu86leibCK5ofyZk0WCQRu1aTyb%2FTWNHQj024aWnNFVR3%2FWbo5%2BO7jY1zo%2FA5sM%2Bczrir0SAz2%2F%2Ftca0L%2Fkqtm7MXYVDK%2BQI%2FYfegVY5xJ%2FXHPe1yxdBnChxUw9LNlvQ2ROtrVZy2NCEhIODC01LYEGkzX9H1riENiJkl46hLlQwgiMpTsk1prIEWyzMDVW4aBx%2BFwy1RbYnhO%2F1sZ1jybgxoQRB%2BCIu1BtglM33pDhCljkkny%2FIuJcSPgISACwe8a74c7d5a6e865e6cc6b8841c45c1852a37a2a5; Hm_lpvt_12b6a0c74b9c210899f69b3429653ed6=1606463910; Hm_lpvt_f5ec9aea58f25882d61d31eb4b353550=1606463910; zg_did=%7B%22did%22%3A%20%22175c09d367c5d0-057410193f4edd-230346c-1fa400-175c09d367d89%22%7D; zg_db630a48aa614ee784df54cc5d0cdabb=%7B%22sid%22%3A%201606463910336%2C%22updated%22%3A%201606463910336%2C%22info%22%3A%201606201534921%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.che300.com%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201606463910336%7D',
            'referer': 'https://m.che300.com/estimate/result/3/3/1/1/1146060/2019-3/2/1/null/2020/2018',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        }

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': "192.168.1.94",
        'MYSQL_USER': "dataUser94",
        'MYSQL_PWD': "94dataUser@2020",
        'MYSQL_PORT': 3306,
        'MYSQL_DB': "che300",
        'MYSQL_TABLE': "che300_gz",
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'che300',
        'MONGODB_COLLECTION': 'che300_gz',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        # 'DOWNLOAD_TIMEOUT': 5,
        # 'RETRY_ENABLED': False,
        # 'RETRY_TIMES': 1,
        # 'COOKIES_ENABLED': True,
        # 'REDIS_URL': 'redis://192.168.1.241:6379/14',
        'DOWNLOADER_MIDDLEWARES': {
            'che300_xcx.middlewares.Che300XcxProxyMiddleware': 400,
            'che300_xcx.middlewares.Che300XcxUserAgentMiddleware': 100,
            'gerapy_pyppeteer.downloadermiddlewares.PyppeteerMiddleware': 543,
        },
        # 'ITEM_PIPELINES': {
        #       'che300_xcx.pipelines.Che300XcxPipeline': 300,
        #     'che300_xcx.pipelines.RenameTable': 299
        # },
    }

    def start_requests(self):
        url = 'https://m.che300.com/estimate/result/3/3/1/1/1146060/2019-3/2/1/null/2020/2018'
        # url = 'https://www.che300.com/pinggu/v1c1m1128945r2018-3g4?click=homepage&rt=1606388157943'
        yield PyppeteerRequest(url=url)
        # yield scrapy.Request(url)

    def parse(self, response):
        item = Che300XcxItem()
        img_base64_urls = re.findall('.html\(\'<img src="data:image/png;base64,(.*?)" style="width', response.text)
        # img_base64_urls = re.findall('data:image/png;base64,(.*?)" style="width: 70px', response.text)
        # print(response.text)
        # print(img_base64_urls)
        item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['vehicle'] = '1146060'
        item['city'] = '上海'
        item['regdate'] = '2019-3'
        price_list = []
        for i in img_base64_urls:
            # print(i)
            imgdata = base64.b64decode(i.replace('\n', '').replace('\r', ''))
            file = open('1.jpg', 'wb')
            file.write(imgdata)
            file.close()
            text = pytesseract.image_to_string(Image.open("./1.jpg"), lang="eng").replace(',', '.').replace(
                '\n\x0c', '').strip()
            # print(text)
            price_list.append(text)
        # print(price_list)
        for i in range(1, 22):
            item[f'price{i}'] = price_list[i - 1]
        print(item)
