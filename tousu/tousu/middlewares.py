# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
import json
import random

from selenium.webdriver import FirefoxProfile
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import time
import traceback
from scrapy.http import HtmlResponse
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging


def getProxy():
    url = 'http://192.168.2.120:5000'
    # url = 'http://120.27.216.150:5000'
    headers = {
        'Connection': 'close',
    }
    proxy = requests.get(url, headers=headers, auth=('admin', 'zd123456')).text[0:-6]
    return proxy


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        if spider.name in ['a12345auto', 'all_brand_qctsw', 'czw', 'all_brand_tousu315che']:
            proxy = getProxy()
            request.meta['proxy'] = "http://" + proxy
            # print(request.headers)
            print(f'proxy success : {proxy}!')

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        if response.status == 403:
            request.meta['proxy'] = "http://" + getProxy()
            print('proxy success !')
            return request
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response


class SeleniumMiddleware(object):
    """
    selenium 动态加载代理ip
    """
    def __init__(self, timeout=30):
        profile = FirefoxProfile()
        options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        # 去掉提示：Chrome正收到自动测试软件的控制
        options.add_argument('disable-infobars')
        # 禁止加载照片
        profile.set_preference('permissions.default.image', 2)
        # 禁止加载css样式表
        profile.set_preference('permissions.default.stylesheet', 2)
        options.set_preference("dom.webnotifications.enabled", False)
        # 修改页面加载策略
        # none表示将br.get方法改为非阻塞模式，在页面加载过程中也可以给br发送指令，如获取url，pagesource等资源。

        # self.browser = webdriver.Firefox(firefox_profile=profile, firefox_options=options,
        #                                  executable_path='')

        self.browser = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
        self.timeout = timeout
        # self.browser.maximize_window()
        self.browser.set_page_load_timeout(self.timeout)  # 设置页面加载超时
        self.browser.set_script_timeout(self.timeout)  # 设置页面异步js执行超时
        # self.wait = WebDriverWait(self.browser, self.timeout, poll_frequency=0.5)

    def close_spider(self, spider):
        self.browser.quit()
        self.browser.close()

    def __del__(self):
        self.browser.quit()
        self.browser.close()

    def process_request(self, request, spider):
        if spider.name in ['a12345auto']:
            proxy, ip, port = self.get_Proxy()
            self.set_proxy(self.browser, ip=ip, port=port)
            # browser = self.browser
            # 显示等待
            # self.wait.until(lambda browser: browser.find_element_by_class_name('tslb_b'))
            # 隐形等待
            # browser.implicitly_wait(10)
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
                # 此处访问你需要的URL
                self.browser.get(request.url)
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
        # url = 'http://192.168.2.120:5000'
        url = 'http://120.27.216.150:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        ip = proxy.split(":")[0]
        port = proxy.split(":")[1]
        return proxy, ip, port

    def set_proxy(self, driver, ip='', port=0):
        driver.get("about:config")
        script = '''
                    var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
                    prefs.setIntPref("network.proxy.type", 1);
                    prefs.setCharPref("network.proxy.http", "{ip}");
                    prefs.setIntPref("network.proxy.http_port", "{port}");
                    prefs.setCharPref("network.proxy.ssl", "{ip}");
                    prefs.setIntPref("network.proxy.ssl_port", "{port}");
                    prefs.setCharPref("network.proxy.ftp", "{ip}");
                    prefs.setIntPref("network.proxy.ftp_port", "{port}");
        　　　　　　　 prefs.setBoolPref("general.useragent.site_specific_overrides",true);
        　　　　　　　 prefs.setBoolPref("general.useragent.updates.enabled",true);
                    '''.format(ip=ip, port=port)
        driver.execute_script(script)
