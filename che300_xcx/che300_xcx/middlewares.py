# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import random

import redis
import requests
from scrapy.http.headers import Headers
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

logger = logging.getLogger(__name__)


class Che300XcxProxyMiddleware(object):
    def __init__(self):
        self.count = 0
        self.proxy = "http://" + getProxy()

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            self.proxy = "http://" + getProxy()
            request.meta['proxy'] = self.proxy
            print(f'Get a new ip {self.proxy}!')
            return request

    def process_request(self, request, spider):
        # 要使用代理的爬虫名字写进去
        # if spider.name in ['', '']:
        # proxy = getProxy()
        # request.meta['proxy'] = "http://" + proxy
        proxy = getProxy()
        request.meta['proxy'] = "http://" + proxy

    def process_response(self, request, response, spider):
        if response.status in [500]:
            print(response.url)
        return response


def getProxy():
    s = requests.session()
    s.keep_alive = False
    url_list = ['http://192.168.2.120:5000']
    url = url_list[0]
    headers = {
        'Connection': 'close',
    }
    proxy = s.get(url, headers=headers, auth=('admin', 'zd123456')).text[0:-6]
    return proxy


class Che300XcxUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(user_agent_list)
        request.headers.setdefault('User-Agent',
                                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
        cookie1 = 'device_id=h52ac0-418c-a1b7-10b5-b67e; pcim=e8f8f86ec7aba7e90bf67c1cddc7a6c5ef86d292; tel=17059155843; PHPSESSID=9e27a6faeeb6806f211c3270d3fcc8bb2ebf6efd; Hm_lvt_12b6a0c74b9c210899f69b3429653ed6=1605254329; Hm_lvt_f5ec9aea58f25882d61d31eb4b353550=1605254330; Hm_lvt_f33b83d5b301d5a0c3e722bd9d89acc8=1606450498; Hm_lpvt_f33b83d5b301d5a0c3e722bd9d89acc8=1606463853; spidercooskieXX12=1606463908; spidercodeCI12X3=ad337693b2ed2abd577c71c55798613c; _che300=ywBRMQDBupubEqc0KC93oGzVF%2FAAC74JclA4VUy%2BeCTEW0IQqnWHyDBaj0QYHGqjo9OPTVfuD5aaU10ycpmatzt%2FV21zMY3kN3ZP0VGyiFVlBjOSQrZ2U2zEqh7AQOaLiMT9%2B50HEWVj1zzOAv3%2BevgplR%2Bx8yi7p0Jtq%2BP6cozVx9vzxwyrYtVLFR%2By9uqyOafvU4fgP0y%2BiqXHW2jU%2F5I13cEuB9S1jMW4WyKF2pIkIjAvYAr1RK0KUZEKizYG1onChuYSQ1oym7Y7Gh1%2Fne%2FKUNpeiG0CqE7%2FkuKwovppqPF8N%2BHkDHUMh3N5cREnaq57Z69fvxBP4OQGlrkHZLbZcED1zAi%2BDecOolcY3Qsn%2FT9xyBbHfIuB%2FkhNICUmjuu86leibCK5ofyZk0WCQRu1aTyb%2FTWNHQj024aWnNFVR3%2FWbo5%2BO7jY1zo%2FA5sM%2Bczrir0SAz2%2F%2Ftca0L%2Fkqtm7MXYVDK%2BQI%2FYfegVY5xJ%2FXHPe1yxdBnChxUw9LNlvQ2ROtrVZy2NCEhIODC01LYEGkzX9H1riENiJkl46hLlQwgiMpTsk1prIEWyzMDVW4aBx%2BFwy1RbYnhO%2F1sZ1jybgxoQRB%2BCIu1BtglM33pDhCljkkny%2FIuJcSPgISACwe8a74c7d5a6e865e6cc6b8841c45c1852a37a2a5; Hm_lpvt_12b6a0c74b9c210899f69b3429653ed6=1606463910; Hm_lpvt_f5ec9aea58f25882d61d31eb4b353550=1606463910; zg_did=%7B%22did%22%3A%20%22175c09d367c5d0-057410193f4edd-230346c-1fa400-175c09d367d89%22%7D; zg_db630a48aa614ee784df54cc5d0cdabb=%7B%22sid%22%3A%201606463910336%2C%22updated%22%3A%201606463910336%2C%22info%22%3A%201606201534921%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.che300.com%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201606463910336%7D'
        cookie_list = cookie1.split('; ')
        cookie_dict = {}
        for i in cookie_list:
            cookie_dict[i.split('=')[0]] = i.split('=')[1]
        request.cookies = cookie_dict


user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
]


class Che300XcxSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Che300XcxDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
