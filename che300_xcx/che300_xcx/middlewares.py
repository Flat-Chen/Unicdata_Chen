# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import random
import json
import time
import traceback

import redis
import requests
from scrapy.http import TextResponse
from scrapy.http.headers import Headers
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from redis import Redis
from scrapy import signals
from selenium.webdriver.support.wait import WebDriverWait
from twisted.internet.error import TimeoutError
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from twisted.internet.error import TimeoutError, TCPTimedOutError

redis_url = 'redis://192.168.2.149:6379/8'
r = Redis.from_url(redis_url, decode_responses=True)
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
    def __init__(self):
        self.count = 0
        self.cookie_str = r.lpop("che300_gz:cookies")

    def process_request(self, request, spider):
        ua = random.choice(user_agent_list)
        request.headers.setdefault('User-Agent',
                                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
        cookie_json = json.loads(self.cookie_str)
        cookie = cookie_json['cookie'].replace('\n', '')
        last_use_time = cookie_json['last_use_time']
        time1 = time.mktime(time.strptime(last_use_time, "%Y-%m-%d %H:%M:%S"))
        local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        time2 = time.mktime(time.strptime(local_time, "%Y-%m-%d %H:%M:%S"))
        hoursCount = (time2 - time1)
        if hoursCount >= 3600:
            cookie_list = cookie.split('; ')
            cookie_dict = {}
            for i in cookie_list:
                cookie_dict[i.split('=')[0]] = i.split('=')[1]
                # print(cookie_dict)
            request.cookies = cookie_dict
            self.count = self.count + 1
            print('====================该cookie使用次数:', self.count)
            if self.count >= 50:
                print('该cookie请求达到50次 换下一个')
                cookie_dict1 = {"cookie": cookie, "last_use_time": local_time}
                r.rpush('che300_gz:cookies', str(cookie_dict1).replace("'", '"'))
                self.count = 0
                self.cookie_str = r.lpop("che300_gz:cookies")
        else:
            # 间隔小于一小时 重新放入队列尾端
            r.rpush('che300_gz:cookies', self.cookie_str)
            print('该cookie使用间隔小于一小时 重新放入队列尾端！')
            self.cookie_str = r.lpop("che300_gz:cookies")


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


class SeleniumMiddleware(object):
    """
    selenium 动态加载代理ip 、 cookie
    """

    def __init__(self, timeout=30):
        redis_url = 'redis://192.168.2.149:6379/8'
        self.r = Redis.from_url(redis_url, decode_responses=True)
        self.cookie_count = 0
        self.cookie_str = self.r.blpop("che300_gz:cookies")[1]

        profile = FirefoxProfile()
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        # 去掉提示：Chrome正收到自动测试软件的控制
        options.add_argument('disable-infobars')

        # 设置代理
        # profile.set_preference('network.proxy.type', 1)
        # profile.set_preference('network.proxy.http', '81.68.214.148')
        # profile.set_preference('network.proxy.http_port', 16128)
        # profile.set_preference('network.proxy.ssl', '81.68.214.148')
        # profile.set_preference('network.proxy.ssl_port', 16128)

        # 禁止加载照片
        profile.set_preference('permissions.default.image', 2)
        # 禁止加载css样式表
        profile.set_preference('permissions.default.stylesheet', 2)
        options.set_preference("dom.webnotifications.enabled", False)
        # 修改页面加载策略
        # none表示将br.get方法改为非阻塞模式，在页面加载过程中也可以给br发送指令，如获取url，pagesource等资源。
        # desired_capabilities = DesiredCapabilities.FIREFOX  # 修改页面加载策略页面加载策略
        # desired_capabilities["pageLoadStrategy"] = "none"

        # self.browser = webdriver.Firefox(firefox_profile=profile, firefox_options=options,
        #                                  executable_path='/usr/bin/firefox')

        self.browser = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
        # 首先加载要添加cookie的网站, 然后添加cookie字典
        self.timeout = timeout
        # self.browser.maximize_window()
        self.browser.set_page_load_timeout(self.timeout)  # 设置页面加载超时
        self.browser.set_script_timeout(self.timeout)  # 设置页面异步js执行超时
        # self.wait = WebDriverWait(self.browser, self.timeout, poll_frequency=0.5)

    def close_spider(self, spider):
        self.r.close()
        try:
            self.browser.quit()
            self.browser.close()
        except:
            pass

    def __del__(self):
        r.rpush('che300_gz:cookies', self.cookie_str)
        self.r.close()
        try:
            self.browser.quit()
            self.browser.close()
        except:
            pass

    def get_cookie(self, driver):
        while 1:
            cookie_json = json.loads(self.cookie_str)
            self.cookie = cookie_json['cookie'].replace('\n', '')
            last_use_time = cookie_json['last_use_time']
            time1 = time.mktime(time.strptime(last_use_time, "%Y-%m-%d %H:%M:%S"))
            self.local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            time2 = time.mktime(time.strptime(self.local_time, "%Y-%m-%d %H:%M:%S"))
            hoursCount = (time2 - time1)
            # 判断距离最后一次使用是否超过一小时
            if hoursCount >= 3600:
                # 第一次使用add cookie 后面直接请求不用再add
                if self.cookie_count == 0:
                    driver.get('http://m.che300.com/estimate/result/3/3/12/209/32814/2019-12/2/1/null/2016/2019')
                    cookie_split = self.cookie.split('; ')
                    for i in cookie_split:
                        # print({'name': i.split('=')[0], 'value': i.split('=')[1]})
                        driver.add_cookie(
                            cookie_dict={'name': i.split('=')[0].strip(), 'value': i.split('=')[1].strip()})
                self.cookie_count = self.cookie_count + 1
                logging.info('========================该cookie使用次数:{}===================='.format(self.cookie_count))
                break
            else:
                # 间隔小于一小时 重新放入队列尾端
                self.r.rpush('che300_gz:cookies', self.cookie_str)
                logging.warning('===================该cookie使用间隔小于一小时 重新放入队列尾端！=================')
                self.cookie_str = self.r.blpop("che300_gz:cookies")[1]
                time.sleep(0.5)
                self.cookie_count = 0

    def process_request(self, request, spider):
        if spider.name in ['che300_gz']:
            proxy, ip, port = self.get_Proxy()
            self.set_proxy(self.browser, ip=ip, port=port)
            main_win = self.browser.current_window_handle  # 记录当前窗口的句柄
            all_win = self.browser.window_handles
            try:
                if len(all_win) == 1:
                    logging.info("-------------------弹出保护罩-------------------")
                    js = 'window.open("https://www.baidu.com");'
                    self.browser.execute_script(js)
                    # 还是定位在main_win上的
                    for win in all_win:
                        if main_win != win:
                            print('保护罩WIN', win, 'Main', main_win)
                            self.browser.switch_to.window(main_win)

                # 此处访问要请求的url
                try:
                    self.get_cookie(self.browser)
                    self.browser.get(request.url)
                    if '异常提示' in self.browser.page_source:
                        logging.warning('=====================该cookie以达到最大请求次数 换下一个==============')
                        cookie_dict1 = {"cookie": self.cookie, "last_use_time": self.local_time}
                        r.rpush('che300_gz:cookies', str(cookie_dict1).replace("'", '"'))
                        self.cookie_count = 0
                        self.cookie_str = self.r.blpop("che300_gz:cookies")[1]
                except:
                    logging.error("加载页面太慢，停止加载，继续下一步操作")
                    self.browser.execute_script("window.stop()")
                url = self.browser.current_url
                body = self.browser.page_source

                return HtmlResponse(url=url, body=body, encoding="utf-8")
            except:
                # 超时
                logging.info("-------------------Time out-------------------")
                # 切换新的浏览器窗口
                for win in all_win:
                    if main_win != win:
                        logging.info("-------------------切换到保护罩-------------------")
                        print('WIN', win, 'Main', main_win)
                        self.browser.close()
                        self.browser.switch_to.window(win)
                        main_win = win

                js = 'window.open("https://www.baidu.com");'
                self.browser.execute_script(js)
                if 'time' in str(traceback.format_exc()):
                    # print('页面访问超时')
                    logging.info("-------------------页面访问超时-------------------")

    def get_Proxy(self):
        url = 'http://192.168.2.120:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        try:
            ip = proxy.split(":")[0]
            port = proxy.split(":")[1]
        except Exception as e:
            logging.error('取代理时出错了，暂时将自己的代理顶上', repr(e))
            ip = '81.68.214.148'
            port = '16128'
        return proxy, ip, port

    def set_proxy(self, driver, ip='', port=0):
        try:
            driver.get("about:config")
        except:
            logging.error("动态加载IP时，页面加载页面太慢，停止加载，继续下一步操作")
            self.browser.execute_script("window.stop()")
        script = '''var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
                        prefs.setIntPref("network.proxy.type", 1);
                        prefs.setCharPref("network.proxy.http", "{ip}");
                        prefs.setIntPref("network.proxy.http_port", "{port}");
                        prefs.setCharPref("network.proxy.ssl", "{ip}");
                        prefs.setIntPref("network.proxy.ssl_port", "{port}");
                        prefs.setCharPref("network.proxy.ftp", "{ip}");
                        prefs.setIntPref("network.proxy.ftp_port", "{port}");
            　　　　　　 prefs.setBoolPref("general.useragent.site_specific_overrides",true);
            　　　　　　 prefs.setBoolPref("general.useragent.updates.enabled",true);
                        prefs.setBoolPref("browser.cache.disk.enable", false);
                        prefs.setBoolPref("browser.cache.memory.enable", false);
                        prefs.setBoolPref("browser.cache.offline.enable", false);
                '''.format(ip=ip, port=port)
        try:
            driver.execute_script(script)
        except Exception as e:
            logging.error('设置动态代理时出错！！！', repr(e))

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            return request
        elif isinstance(exception, TCPTimedOutError):
            return request


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
        if isinstance(exception, TimeoutError):
            return request
        elif isinstance(exception, TCPTimedOutError):
            return request

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
