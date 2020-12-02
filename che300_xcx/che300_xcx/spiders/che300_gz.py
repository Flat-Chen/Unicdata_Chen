import re
import base64
import time

import pytesseract
from PIL import Image
import random
import scrapy
from gerapy_pyppeteer import PyppeteerRequest
from che300_xcx.items import Che300XcxItem
from redis import Redis

redis_url = 'redis://192.168.2.149:6379/8'
r = Redis.from_url(redis_url, decode_responses=True)


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
        'CONCURRENT_REQUESTS': 32,
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
        url = r.lpop('che300_gz:start_urls')
        yield PyppeteerRequest(url=url, meta={'url': url}, sleep=2)

    def parse(self, response):
        url = response.meta['url']
        item = Che300XcxItem()
        try:
            img_base64_urls = re.findall('.html\(\'<img src="data:image/png;base64,(.*?)" style="width', response.text)
            # img_base64_urls = re.findall('data:image/png;base64,(.*?)" style="width: 70px', response.text)
            # print(response.text)
            # print(img_base64_urls)
            'https://m.che300.com/estimate/result/3/3/15/36132/1527710/2020-11/0.1/1/null/2020/2020?rt=1606872801904'
            item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            url_data = response.url.split('/')
            item['vehicle'] = url_data[9]
            item['city'] = '上海'
            item['regdate'] = url_data[10]
            item['mile'] = url_data[11]
            item['url'] = url
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
                # print(item)
            yield item
        except:
            print('解析数据失败，url重新加到请求队列尾部')
            r.rpush('che300_gz:start_urls', url)
        next_url = r.blpop('che300_gz:start_urls')
        if next_url:
            start_url = next_url[1]
            yield PyppeteerRequest(url=start_url, meta={'url': start_url}, callback=self.parse, sleep=2)
