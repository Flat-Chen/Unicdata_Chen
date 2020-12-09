import logging
import re
import traceback
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver import FirefoxProfile, DesiredCapabilities
import time
import requests


class SeleniumMiddleware(object):
    """
    selenium 动态加载代理ip
    """

    def __init__(self, timeout=30):
        profile = FirefoxProfile()
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        # 去掉提示：Chrome正收到自动测试软件的控制
        options.add_argument('disable-infobars')
        self.wait_time = 0
        # 设置代理
        # profile.set_preference('network.proxy.type', 1)
        # profile.set_preference('network.proxy.http', '81.68.214.148')
        # profile.set_preference('network.proxy.http_port', 16128)
        # profile.set_preference('network.proxy.ssl', '81.68.214.148')
        # profile.set_preference('network.proxy.ssl_port', 16128)
        # 禁止加载照片
        # profile.set_preference('permissions.default.image', 2)
        # 禁止加载css样式表
        # profile.set_preference('permissions.default.stylesheet', 2)
        # options.set_preference("dom.webnotifications.enabled", False)
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

    def close_spider(self):
        try:
            self.browser.quit()
            self.browser.close()
        except:
            pass

    def __del__(self):
        try:
            self.browser.quit()
            self.browser.close()
        except:
            pass

    def process_request(self, safety_url):
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
                self.browser.get(safety_url)
            except Exception as e:
                logging.error("加载页面太慢，停止加载，继续下一步操作", e)
                self.browser.execute_script("window.stop()")
            time.sleep(5)
            while 1:
                url = self.browser.current_url
                print(url, self.wait_time)
                if 'safety' in url:
                    time.sleep(5)
                    self.wait_time = self.wait_time + 5
                else:
                    break
            body = self.browser.page_source
            title = re.findall(r'<title>(.*?)</title>', self.browser.page_source)[0]
            # url = self.browser.current_url
            # print(body)
            print(url)
            print(title)
            print(self.wait_time)

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


url = 'http://safety.autohome.com.cn/userverify/index?locnum=109707&backurl=//club.autohome.com.cn%2Fbbs%2Fthread%2F4baec8922feedb46%2F91901900-1.html'

SeleniumMiddleware().process_request(url)
