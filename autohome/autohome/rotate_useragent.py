# -*-coding:utf-8-*-

import logging
import json
from scrapy.http import HtmlResponse
import requests
from lxml import etree
import xlrd
"""
避免被ban策略之一：使用useragent池。

使用注意：需在settings.py中进行相应的设置。
"""
from selenium.webdriver.support.ui import Select
import time
import random
import requests
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from selenium import webdriver
from scrapy.utils.project import get_project_settings
settings = get_project_settings()


class RotateUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        print("UA")
        if spider.name not in ["58shop", "58office"]:
            ua = random.choice(self.user_agent_list)
            if ua:
                #显示当前使用的useragent
                #print "********Current UserAgent:%s************" %ua
                #记录
                logging.log(msg='Current UserAgent: ' + ua, level=logging.DEBUG)
                request.headers.setdefault('User-Agent', ua)

    #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
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

    def get_Proxy(self):
        url = 'http://120.27.216.150:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        return proxy

    def process_request(self, request, spider):
        print("selenium")

        if spider.name in ['chegongfang']:
            spider.browser.get(request.url)
            spider.browser.find_element_by_xpath("//*[@id='s-prov']").click()
            time.sleep(2)
            s1 = Select(spider.browser.find_element_by_xpath("//*[@id='s-prov']"))
            s1.select_by_index(0)
            time.sleep(6)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")



        if spider.name in ['get_business_area_for_geo']:
            if request.url == "http://api.map.baidu.com/library/CityList/1.4/examples/CityList.html":
                spider.browser.get(request.url)
                time.sleep(2)
                return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")


        if spider.name in ["weather_tianqihoubao_ry"]:
            if request.url == "http://www.tianqihoubao.com/lishi/":
                res = requests.request("get", request.url)
                res.encoding = "gbk"
                # print(res.content.decode("gbk"))
                return HtmlResponse(body=res.content.decode("gbk"), url=request.url, encoding="utf-8")

        if spider.name in ["chexiangjia_2019"] and request.url != "http://jia.chexiang.com/store/list_PC.htm":
            spider.browser.get(request.url)
            time.sleep(2)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")

        if spider.name in ['autohome_general_store','sunning_mobile_phone', 'all_province', 'telaidian']:
            spider.browser.get(request.url)
            time.sleep(2)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")


        if spider.name in ['autohome_custom_price2']:

            if request.url != "https://www.autohome.com.cn/beijing/":
                spider.browser.get(request.url)
                time.sleep(2)

                code = spider.browser.page_source
                tree = etree.HTML(code)


                text = "<ul>"

                clazzs = tree.xpath("//*[@class='car-lists-item-bottom']/ol/li/span[2]/span[1]/span[1]/span[1]/@class")
                temp_price_string = ""
                for clazz in clazzs:
                    if clazzs.index(clazz) % 3 == 0:
                        temp_price_string = ""

                    script = "return window.getComputedStyle(document.getElementsByClassName('%s')[0], 'before').getPropertyValue('content')" % clazz
                    if clazzs.index(clazz) % 3 == 0:
                        naked_price = spider.browser.execute_script(script)
                        temp_price_string = naked_price
                    if clazzs.index(clazz) % 3 == 1:
                        total_price = spider.browser.execute_script(script)
                        temp_price_string = temp_price_string + "-" + total_price
                    if clazzs.index(clazz) % 3 == 2:
                        guide_price = spider.browser.execute_script(script)
                        temp_price_string = temp_price_string + "-" + guide_price
                        text = text + "<li>%s</li>" % temp_price_string

                text = text + "</ul>"





                return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source.replace("</html>", text + "</html>"), encoding="utf-8")




        if spider.name in ['lianjia_fang']:
            if request.url.find("pg") < 0:
                spider.browser.get(request.url)
                time.sleep(2)
                return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")

        if spider.name in ['']:
            options = webdriver.ChromeOptions()
            options.add_argument(
                'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"')
            options.add_argument('--proxy-server=http://%s' % self.get_Proxy())
            browser = webdriver.Chrome(
                executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe", chrome_options=options)
            browser.set_page_load_timeout(30)
            # self.browser.start_session()
            browser.get(request.url)
            time.sleep(0.5)
            url = browser.current_url
            body = browser.page_source
            browser.quit()
            return HtmlResponse(url=url, body=body, encoding="utf-8")





        if spider.name in ['autohome_users']:
            if request.url.find("account") >= 0:
                spider.browser.get(request.url)
                time.sleep(2)
                while True:
                    if spider.browser.current_url.find("https://www.autohome.com.cn") >= 0:
                        return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                                            encoding="utf-8")
                    else:
                        time.sleep(2)
            else:
                spider.browser.get(request.url)
                time.sleep(0.5)
                return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")




        # if spider.name in ['58_shop', '58_office']:
        #     if request.url.find("changecity") < 0:
        #         # spider.browser.get(request.url)
        #         # time.sleep(8)
        #         # return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")
        #
        #         # cookies = spider.browser.get_cookies()
        #         # try:
        #         #     spider.browser.quit()
        #         # except Exception as e:
        #         #     print(e)
        #
        #         # proxy = self.get_Proxy()
        #         # options = webdriver.ChromeOptions()
        #         # options.add_argument('--proxy-server=http://%s' % proxy)
        #         # options.add_argument(
        #         #     'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"')
        #         # spider.browser = webdriver.Chrome(
        #         #     executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",
        #         #     chrome_options=options)
        #         # spider.browser.set_page_load_timeout(100)
        #
        #         desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        #         desired_capabilities[
        #             "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        #         desired_capabilities["phantomjs.page.settings.loadImages"] = False
        #         proxy = webdriver.Proxy()
        #         proxy.proxy_type = ProxyType.MANUAL
        #         proxy_ip = self.get_Proxy()
        #         print(proxy_ip)
        #         proxy.http_proxy = proxy_ip
        #         proxy.add_to_capabilities(desired_capabilities)
        #         spider.browser.start_session(desired_capabilities)
        #         spider.browser.implicitly_wait(30)
        #         spider.browser.set_page_load_timeout(30)
        #
        #         # spider.browser.delete_all_cookies()
        #         # for item in cookies:
        #         #     print(item)
        #         #     spider.browser.add_cookie(item)
        #
        #         # profile = webdriver.FirefoxProfile()
        #         # profile.add_extension("modify_headers-0.7.1.1-fx.xpi")
        #         # profile.set_preference("extensions.modify_headers.currentVersion", "0.7.1.1-fx")
        #         # profile.set_preference("modifyheaders.config.active", True)
        #         # profile.set_preference("modifyheaders.headers.count", 1)
        #         # profile.set_preference("modifyheaders.headers.action0", "Add")
        #         # profile.set_preference("modifyheaders.headers.name0", "User-Agent")
        #         # profile.set_preference("modifyheaders.headers.value0",
        #         #                        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"')
        #         # profile.set_preference("modifyheaders.headers.enabled0", True)
        #         #
        #         # profile.set_preference('network.proxy.type', 1)
        #         # proxy_ip = self.get_Proxy()
        #         # profile.set_preference('network.proxy.http', proxy_ip[0:-6])
        #         # profile.set_preference('network.proxy.http_port', 18888)
        #         # profile.set_preference('network.proxy.no_proxies_on', 'localhost, 127.0.0.1')
        #         #
        #         # spider.browser = webdriver.Firefox(executable_path=settings['FIREFOX_PATH'], firefox_profile=profile)
        #
        #         try:
        #
        #             spider.browser.get(request.url)
        #             # if request.url.endswith("/zhaozu/"):
        #             #     WebDriverWait(spider.browser, 10).until(
        #             #         EC.presence_of_element_located((By.CLASS_NAME, 'content-wrap')))
        #         except Exception as e:
        #             print(e)
        #             return request
        #         time.sleep(10)
        #         # print(spider.browser.page_source)
        #         return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")
        if spider.name in ['dianping_gas', 'dianping_market'] and request.url.find("shop") >= 0:
            spider.browser.get(request.url)
            # print(spider.browser.page_source)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")
        # if spider.name in ['ttpai']:
        #     spider.browser.get(request.url)
        #     print(spider.browser.page_source)
        #     return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")

        if spider.name in ["insaic"]:
            nb = xlrd.open_workbook("D:/vin.xlsx")
            st = nb.sheet_by_index(0)
            vin_list = st.col_values(3)
            print(vin_list)
            if request.url == "https://svwdim.insaic.com/pages/login.html":
                spider.browser.get(request.url)
                spider.browser.set_window_size(1920, 1080)
                spider.browser.find_element_by_xpath("//*[@id='userName']").send_keys("zhongdiao")
                spider.browser.find_element_by_xpath("//*[@id='password']").send_keys("Pass1234")
                spider.browser.find_element_by_xpath("//*[@id='loginBtn']").click()
                while True:
                    if spider.browser.current_url == "https://svwdim.insaic.com/dim/#!/":
                        spider.browser.find_element_by_xpath("//*[@id='ngdialog2']/div[2]/div/button[1]").click()
                        time.sleep(3)
                        spider.browser.find_element_by_xpath("//*[@id='ngdialog1']/div[2]/div/button[1]").click()
                        time.sleep(3)
                        spider.browser.find_element_by_xpath("//*[@id='ngdialog3']/div[2]/div/button[1]").click()
                        time.sleep(3)
                        spider.browser.get("https://svwdim.insaic.com/policy/#!/delayInsure/apply")
                        while True:
                            if spider.browser.current_url == "https://svwdim.insaic.com/policy/#!/delayInsure/apply":
                                for vin in vin_list[1:]:
                                    spider.browser.find_element_by_xpath("//*[@id='vin']").send_keys(vin)
                                    while True:
                                        if spider.browser.find_element_by_xpath("//*[@id='contactorMobile']").get_attribute("textContent") != "":
                                            return HtmlResponse(url=spider.browser.current_url,
                                                                body=spider.browser.page_source,
                                                                encoding="utf-8")
                                            break
                                        else:
                                            time.sleep(1)
                                break
                            else:
                                time.sleep(1)





class ProxyMiddleware(object):

    def process_request(self, request, spider):
        print("proxy")
        # if spider.name == "app_rank":
        #     res = requests.request("get", request.url)
        #     return HtmlResponse(url=request.url, body=res.text, encoding="utf-8")

        # if request.meta.has_key('proxy'):
        #     print request.meta['proxy'] + "--proxy"
        if spider.name in ["jzg_price"]:
        # if spider.name in ['jzg_price_test_img_2019_0816', 'gpj_price_new', 'jzg_price_test_img_2019_for_cities4', 'jzg_price_test_error_2019', 'gpj_modellist2', 'tuhu_baoyang_test', 'lianjia_fang','lianjia_village', '58_shop', '58_office', 'che300pro_new', 'cheniu_shop', 'autohome_min_max_price','autohome_custom_price', 'anjuke_shou_fix', 'anjuke_zu_fix', 'gpj_price_test', 'jzg_price_test_img_2019', 'chehang168', 'autohome_error', "autohome_error_p", "chezhiwang_tousu2", "qichemenwang_tousu", "jzg_modellist2"]:
            # print(spider.name)
            print(self.get_Proxy())
            request.meta['proxy'] = "http://" + self.get_Proxy()

        if spider.name in ["weixin_%s" % settings["WEIXIN"]]:
            # print(spider.name)
            print(self.get_Proxy())
            request.meta['proxy'] = "http://" + self.get_Proxy()



    def get_Proxy(self):
        url = 'http://120.27.216.150:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        return proxy

    def process_response(self, request, response, spider):
        print(response.status)
        # print(response.url)
        # print(response.body)
        return response
        # if spider.name in ['58_office', '58_shop']:
        #     if response.status == 302 or response.status >= 400:
        #         print("http://" + self.getProxy())
        #         request.meta['proxy'] = "http://" + self.getProxy()
        #         # request.meta['ip'] = "http://" + self.getProxy()
        #         print(request.meta['proxy'])
        #         return request
        #     else:
        #         return response
        # else:
        #     return response
from scrapy.http import HtmlResponse
class TTPaiMiddleware(object):
    def process_request(self, request, spider):
        print("ttpai")
        if spider.name == "ttpai" and request.url == "http://pai.ttpai.cn/":
            if not request.meta.has_key('page'):
                request.meta['page'] = '1'
            res = requests.post("http://pai.ttpai.cn/", data={'status':'1', 'currentPage':request.meta['page']})
            return HtmlResponse(url="http://pai.ttpai.cn/", body=res.text, encoding="utf-8")


class LechebangMiddleware(object):

    def __init__(self):
        self.appCode = 600

    def process_request(self, request, spider):
        json_str = '{"appCode":%d}' % self.appCode
        if request.url == "http://m.lechebang.com/gateway/maintenance/getCitys":
            res = requests.request("post", request.url, json=json.loads(json_str))
            return HtmlResponse(url=request.url, body=res.text, encoding="utf-8")
        if request.url.find("getAllFirstLevelBrandType") >= 0:
            res = requests.request("post", request.url, json=request.meta)
            return HtmlResponse(url=request.url, body=res.text, encoding="utf-8")
        if request.url.find("getBrandProducerCar") >= 0:
            res = requests.request("post", request.url, json=request.meta)
            return HtmlResponse(url=request.url, body=res.text, encoding="utf-8")
        if request.url.find("getCarTypeDetail") >= 0:
            res = requests.request("post", request.url, json=request.meta)
            return HtmlResponse(url=request.url, body=res.text, encoding="utf-8")
        if request.url.find("getMaintenanceManual") >= 0:
            res = requests.request("post", request.url, json=request.meta)
            return HtmlResponse(url=request.url, body=res.text, encoding="utf-8")