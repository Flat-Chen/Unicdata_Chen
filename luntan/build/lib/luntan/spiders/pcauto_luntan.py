import copy
import datetime
import json
import re
import time
from luntan.items import LuntanItem
import scrapy


class PcautoLuntanSpider(scrapy.Spider):
    name = 'pcauto_luntan'
    allowed_domains = ['pcauto.com.cn']
    start_urls = ['http://www.pcauto.com.cn/forum/sitemap/pp/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(PcautoLuntanSpider, self).__init__(**kwargs)
        self.counts = 0
        self.now_year = int(datetime.datetime.now().year)
        self.now_month = int(datetime.datetime.now().month)
        self.headers = {
            'Referer': 'https://bbs.pcauto.com.cn',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            # "Cookie": "visitedfid=17957D20685D22418D20697D23985D23585D17913D17608D17504D17329",
        }

    is_debug = True
    custom_debug_settings = {
        # 'MYSQL_SERVER': '192.168.1.94',
        # 'MYSQL_DB': 'luntan',
        # 'MYSQL_TABLE': 'pcauto_luntan_new',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'luntan',
        'MONGODB_COLLECTION': 'pcauto_luntan',
        'CONCURRENT_REQUESTS': 16,
        # 'DOWNLOAD_DELAY': 1,
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOAD_DELAY': 0.5
    }

    def parse(self, response):
        tr_list = response.xpath("//td[@class='tdCon']/..")
        for tr in tr_list:
            brand = tr.xpath(".//td[@class='tdTit']/i/text()").get()
            dls = tr.xpath('.//td[@class="tdCon"]/dl')
            for dl in dls:
                factory = dl.xpath('.//dt[@class="blue"]/text()').extract_first()
                brand_url = dl.xpath(".//a[@class='hei']/@href").getall()
                familyname = dl.xpath(".//a[@class='hei']/text()").extract_first()
                if brand_url:
                    for url in brand_url:
                        # forumId = '14359'
                        # url = 'https://bbs.pcauto.com.cn/forum-14359.html'
                        url = response.urljoin(url).replace('.html', '-1.html')
                        forumId = re.findall('forum-(.*?).html', url)[0]
                        yield scrapy.Request(
                            url=url,
                            callback=self.brand_parse,
                            headers=self.headers,
                            meta={'info': (brand, factory, forumId, familyname)},
                            dont_filter=True
                        )

    def brand_parse(self, response):
        brand, factory, forumId, familyname = response.meta.get('info')
        tbodys = response.xpath('//table[@class="data_table"]/tbody')
        for tbody in tbodys:
            # title = tbody.xpath('.//span[@class="checkbox_title"]/a/text()').extract_first()
            url = tbody.xpath('.//span[@class="checkbox_title"]/a/@href').extract_first()
            if url:
                url = response.urljoin(url)
                yield scrapy.Request(
                    url=url,
                    callback=self.xiangqing_parse,
                    dont_filter=True,
                    meta={
                        'info': (brand, factory, forumId, familyname)
                    }
                )
        # 论坛判断是否需要翻页
        last_post = response.xpath('//td[@class="lastpost"]/em/text()').getall()[-1].split('-')
        last_post_year = int(last_post[0])
        last_post_month = int(last_post[1])
        if last_post_year == self.now_year:
            if last_post_month + 4 > self.now_month:
                now_url = response.url
                page = int(now_url[-6]) + 1
                new_url = now_url[:-6] + str(page) + '.html'
                yield scrapy.Request(
                    url=new_url,
                    callback=self.brand_parse,
                    headers=self.headers,
                    meta={'info': (brand, factory, forumId, familyname)},
                    dont_filter=True
                )

    def xiangqing_parse(self, response):
        item = LuntanItem()
        brand, factory, forumId, familyname = response.meta.get('info')
        title = response.xpath('//i[@id="subjectTitle"]/text()').extract_first()
        post_time = response.xpath('//div[@class="post_time"]/text()').extract_first()[1:-1].strip().split('于')[
            -1].strip()
        try:
            content = response.xpath('//div[@class="post_msg replyBody"]//text()').extract_first()[1:-1].strip()
        except:
            content = ''
        username = response.xpath('//li[@class="ofw"]/a/text()').extract_first()

        # print(title, brand, factory, forumId, familyname, username)
        # print(post_time, content)
        item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['posted_time'] = post_time
        item['brand'] = brand
        item['factory'] = factory
        item['user_car'] = familyname
        item['forumID'] = forumId
        item['title'] = title
        item['content'] = content
        item['username'] = username
        item['url'] = response.url
        item['status'] = str(username) + str(item["title"]) + str(item["posted_time"]) + str(item["brand"])
        yield item
        # print(item)
