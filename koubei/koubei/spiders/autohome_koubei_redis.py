import time

import scrapy
import redis
from bs4 import BeautifulSoup
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

pool = redis.ConnectionPool(host='192.168.2.149', port=6379, db=2)
con = redis.Redis(connection_pool=pool)


class AutohomeKoubeiRedisSpider(scrapy.Spider):
    name = 'autohome_koubei_redis'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['https://k.autohome.com.cn/detail/view_01cjtv425968rk2d9h74sg0000.html#pvareaid=2112108']

    # redis_key = "autohome_koubei:start_urls"

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeKoubeiRedisSpider, self).__init__(**kwargs)
        self.counts = 0
        self.c = con.client()
        chrome_opts = Options()
        chrome_opts.add_argument('--headless')
        chrome_opts.add_argument('--disable-images')
        chrome_opts.add_argument('--incognito')  # 无痕模式
        chrome_opts.add_argument('--start-maximized')
        chrome_opts.add_argument('--no-sandbox')
        chrome_opts.add_argument(
            '--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"')
        chrome_opts.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(options=chrome_opts,
                                       executable_path=r'C:\Users\13164\Desktop\chromedriver.exe')

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'koubei',
        'MYSQL_TABLE': 'autohome_koubei_chen',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'koubei',
        'MONGODB_COLLECTION': 'autohome_koubei_chen',
        'CrawlCar_Num': 800000,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'DOWNLOAD_TIMEOUT': 10,
        'LOG_LEVEL': 'DEBUG',
        'COOKIES_ENABLED': True,
        'REDIS_URL': 'redis://192.168.2.149:6379/2',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(1)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        content = soup.select('div.text-con')
        for i in content:
            print(i.text)
        # print(content)
        # print(response.text)
        # content = ''.join(response.xpath('//div[@class="text-con"]//text()').getall()).replace('\n', '')
        # replace_text = response.xpath('//style[@type="text/css"]/text()').getall()
        # for text in replace_text:
        #     content.replace(text, '')
        # print(content)
