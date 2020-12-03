import logging
import re
import base64
import time
import pytesseract
from PIL import Image
import random
import scrapy
from che300_xcx.items import Che300XcxItem
from redis import Redis
import io

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
        'MONGODB_COLLECTION': 'che300_price_daily',
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        # 'DOWNLOAD_TIMEOUT': 5,
        # 'RETRY_ENABLED': False,
        # 'RETRY_TIMES': 1,
        # 'COOKIES_ENABLED': True,
        # 'REDIS_URL': 'redis://192.168.1.241:6379/14',
        'DOWNLOADER_MIDDLEWARES': {
            # 'che300_xcx.middlewares.Che300XcxProxyMiddleware': 400,
            # 'che300_xcx.middlewares.Che300XcxUserAgentMiddleware': 100,
            'che300_xcx.middlewares.SeleniumMiddleware': 543,
        },
    }

    def start_requests(self):
        url = r.lpop('che300_gz:start_urls')
        yield scrapy.Request(url=url, meta={'url': url})

    def parse(self, response):
        url = response.meta['url']
        item = Che300XcxItem()
        try:
            img_base64_urls = re.findall('.html\(\'<img src="data:image/png;base64,(.*?)" style="width',
                                         response.body.decode())
            item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            url_data = response.url.split('/')
            item['prov'] = url_data[5]
            item['cityid'] = url_data[6]
            item['brand'] = url_data[7]
            item['series'] = url_data[8]
            item['salesdescid'] = url_data[9]
            item['regDate'] = url_data[10]
            item['mile'] = url_data[11]
            item['group'] = response.xpath('//div[@class="active"]/@id').extract_first()
            item['url'] = url
            price_list = []
            for i in img_base64_urls:
                img = base64.urlsafe_b64decode(i)
                image = Image.open(io.BytesIO(img))
                text = pytesseract.image_to_string(image)
                price_list.append(text)

            index_list = [4, 1, 5, 2, 6, 3, 7, 11, 8, 12, 9, 13, 10, 14, 18, 15, 19, 16, 20, 17, 21]
            for i in index_list:
                item[f'price{index_list.index(i) + 1}'] = price_list[i - 1]
            # print(item)
            yield item
        except:
            logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~解析数据失败，url重新加到请求队列尾部~~~~~~~~~~~~~~~~~~~')
            r.rpush('che300_gz:start_urls', url)
        next_url = r.blpop('che300_gz:start_urls')
        if next_url:
            start_url = next_url[1]
            yield scrapy.Request(url=start_url, meta={'url': start_url}, callback=self.parse)
