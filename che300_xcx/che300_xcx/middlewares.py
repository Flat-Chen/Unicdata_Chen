import logging
import random
import json
import time
import traceback
import cv2
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import redis
import requests
from lxml import etree
from scrapy.http import TextResponse
from redis import Redis
from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver import Chrome, ActionChains, FirefoxProfile
from selenium.webdriver.chrome.options import Options
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

    def process_request(self, request, spider):
        ua = random.choice(user_agent_list)
        request.headers.setdefault('User-Agent', ua)


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


class CaptchaMiddleware(object):
    """
        selenium 动态加载代理ip 、 cookie
        """

    def __init__(self):
        self.count = 0
        self.continuous_count = 0
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        # 去掉提示：Chrome正收到自动测试软件的控制
        # chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--proxy-server=192.168.2.144:16127')
        ua = random.choice(user_agent_list)
        chrome_options.add_argument('user-agent=' + ua)
        # prefs = {
        #     'profile.default_content_setting_values': {
        #         'images': 1,
        #         'permissions.default.stylesheet': 1,
        #         'javascript': 1
        #     }
        # }
        # chrome_options.add_experimental_option('prefs', prefs)
        self.browser = Chrome(options=chrome_options)

        # 擦除浏览器指纹
        with open('stealth.min.js') as f:
            self.clean_js = f.read()

        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": self.clean_js
        })

    def close_spider(self, spider):
        try:
            self.browser.close()
        except:
            pass

    def __del__(self):
        try:
            self.browser.quit()
            self.browser.close()
        except:
            pass

    def get_yzm(self, driver):
        html = etree.HTML(driver.page_source)
        slider = html.xpath('//div[@id="dx_captcha_basic_sub-slider_1"]/img/@src')[0]
        # print(slider)
        response = requests.get(slider)
        with open('slider.png', 'wb') as f:
            f.write(response.content)
        f.close()
        # 保存下来做研究
        # with open(f'./img/{self.count}_slider.png', 'wb') as f:
        #     f.write(response.content)
        # f.close()
        ele = driver.find_element_by_id('dx_captcha_basic_bg_1')
        ele.screenshot('yzm.png')
        # # 保存下来做研究
        # copyfile('yzm.png', f'./img/{self.count}_captcha.png')

    def run(self):
        # 计算验证码缺口位置
        # parameter to seperate template area from find temple area
        cropcol = 65

        # path2files = '/home/junyi/R/RPA/yolo/c3/'
        target_rgb_raw = cv2.imread('yzm.png')
        target_rgb = target_rgb_raw[:, :cropcol, :]
        template_gray = cv2.imread('slider.png', 0)

        # PART1 - find y area where figures are located, in order to crop out unnecessary parts

        # target: find green area with mask filter
        target_rgb = target_rgb_raw[:, :cropcol, :]
        hsv = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2HSV)
        lower_green = np.array([30, 60, 60])
        upper_green = np.array([78, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # target: do erode+dilate in order to delete noise

        # first try erode+dilate on 3x3
        kernel = np.ones((3, 3), np.uint8)
        maskm = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # if first fail, second try erode+dilate on 1x1
        if np.min(np.where(maskm.sum(1) > 0)) >= 118:
            kernel = np.ones((1, 1), np.uint8)
            maskm = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # if second fail, do not run any erode+dilate
        if np.min(np.where(maskm.sum(1) > 0)) >= 118 or len(np.where(maskm.sum(1) > 0)[0]) <= 25:
            # if np.min(np.where(maskm.sum(1)>0))>=118:
            maskm = mask

        # define y area where figures are located
        index_step = 10
        top_index = np.min(np.where(maskm.sum(1) > 0)) - index_step
        bot_index = top_index + index_step + index_step + 40

        # PART2 - clean template

        ret, template_threshed = cv2.threshold(template_gray, 70, 250, cv2.THRESH_BINARY)
        contour, hier = cv2.findContours(template_threshed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contour:
            cv2.drawContours(template_threshed, [cnt], 0, 255, -1)
        template_gray0 = template_gray * (template_threshed / 255).astype(np.uint8)
        xvals = np.where(template_gray0.any(axis=0))
        xvals1 = max(0, np.min(xvals) - 5)
        xvals2 = np.max(xvals) + 5
        yvals = np.where(template_gray0.any(axis=1))
        yvals1 = max(0, np.min(yvals) - 5)
        yvals2 = np.max(yvals) + 5
        template_gray01 = template_gray0[yvals1:yvals2, xvals1:xvals2]

        template_gray2 = np.delete(template_gray01, np.where(~template_gray01.any(axis=1)), axis=0)
        template_gray2 = np.delete(template_gray2, np.where(~template_gray2.any(axis=0)), axis=1)
        template_gray2 = cv2.resize(template_gray2, (40, 40)).astype(np.uint8)
        template_gray1 = template_gray2.copy()
        template_gray2[template_gray2 > 0] = 255
        w, h = template_gray2.shape[::-1]
        edges = cv2.Canny(template_gray2, 50, 150, apertureSize=3)

        template_gray01[template_gray01 > 0] = 255
        edges1 = cv2.Canny(template_gray01, 50, 150, apertureSize=3)
        edges1 = np.delete(edges1, np.where(~edges1.any(axis=1)), axis=0)
        edges1 = np.delete(edges1, np.where(~edges1.any(axis=0)), axis=1)
        edges1 = cv2.resize(edges1, (40, 40)).astype(np.uint8)
        edges1[edges1 > 0] = 255

        # PART3 - clean crop out target

        # crop out unnecessary parts and apply threshold functions
        target_rgb = target_rgb_raw[top_index:bot_index, cropcol:, :]
        target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
        ret, threshed0 = cv2.threshold(target_gray, 50, 255, cv2.THRESH_TOZERO)
        ret, threshed0 = cv2.threshold(threshed0, 55, 60, cv2.THRESH_TOZERO)
        thresh = cv2.adaptiveThreshold(threshed0, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 6)
        th3 = cv2.adaptiveThreshold(threshed0, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 11)

        # PART4 - match target contours with template contours

        df = pd.DataFrame()

        # run 4 models
        res1 = cv2.matchTemplate(thresh, edges, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res1)
        df = df.append(pd.Series([min_val] + list(min_loc)), ignore_index=True)
        df = df.append(pd.Series([max_val] + list(max_loc)), ignore_index=True)

        res2 = cv2.matchTemplate(thresh, edges1, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res2)
        df = df.append(pd.Series([min_val] + list(min_loc)), ignore_index=True)
        df = df.append(pd.Series([max_val] + list(max_loc)), ignore_index=True)

        res2 = cv2.matchTemplate(threshed0, edges, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res2)
        df = df.append(pd.Series([min_val] + list(min_loc)), ignore_index=True)
        df = df.append(pd.Series([max_val] + list(max_loc)), ignore_index=True)

        res2 = cv2.matchTemplate(threshed0, edges1, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res2)
        df = df.append(pd.Series([min_val] + list(min_loc)), ignore_index=True)
        df = df.append(pd.Series([max_val] + list(max_loc)), ignore_index=True)

        res2 = cv2.matchTemplate(th3, edges, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res2)
        df = df.append(pd.Series([min_val] + list(min_loc)), ignore_index=True)
        df = df.append(pd.Series([max_val] + list(max_loc)), ignore_index=True)

        res2 = cv2.matchTemplate(th3, edges1, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res2)
        df = df.append(pd.Series([min_val] + list(min_loc)), ignore_index=True)
        df = df.append(pd.Series([max_val] + list(max_loc)), ignore_index=True)

        # select top result based on correlation coef and topleft point location
        df.columns = ['coef', 'x', 'y']
        df['coef_abs'] = df.coef.abs()

        if df.coef_abs.max() >= 4e6:
            df = df[df.coef_abs >= 4e6]
        if (df.y > 0).sum():
            df = df[df.y > 0]
        if (df.y > 7).sum():
            df = df[df.y > 7]
        if (df.x > 0).sum():
            df = df[df.x > 0]
        if (df.y < 18).sum():
            df = df[df.y < 18]

        df = df.sort_values(by=['coef_abs'], ascending=False)
        top_left = (df.iloc[0, :].values[1:3])
        top_left = tuple(np.int16(top_left))
        distance = top_left[0]

        # plot debug
        # bottom_right = (top_left[0] + w, top_left[1] + h)
        # cv2.rectangle(target_gray, top_left, bottom_right, 255, 2)
        # x = [distance + (w / 2)]
        # plt.subplot(211), plt.imshow(template_gray)
        # plt.subplot(212), plt.imshow(target_gray), plt.plot(x, 30, '*', linewidth=5000, color='firebrick')
        return (distance + 50)

    def get_removing(self, removing):
        list_ren1 = [(0, 0), (4, 0), (8, 1), (13, 1), (20, 2), (29, 2), (37, 2), (45, 2), (58, 3), (66, 3), (73, 3),
                     (80, 3), (87, 3), (94, 3), (101, 3), (107, 3), (113, 3), (120, 3), (128, 3), (133, 4), (143, 6),
                     (147, 7), (149, 7), (151, 7), (155, 7), (159, 8), (163, 9), (165, 9), (169, 10), (172, 10),
                     (175, 10), (180, 10), (186, 11), (190, 11), (194, 12), (197, 12), (199, 12), (202, 12), (204, 12),
                     (205, 12), (206, 12), (207, 12), (208, 12), (210, 12), (212, 12), (214, 12), (215, 12), (216, 12),
                     (217, 12), (218, 12), (219, 12), (220, 12), (221, 12), (222, 12), (223, 12), (224, 12), (225, 12),
                     (226, 12), (227, 12), (228, 12), (229, 12)]
        list_ren2 = [(0, 0), (3, 0), (10, 0), (14, 1), (18, 1), (25, 2), (28, 2), (29, 2), (30, 2), (31, 2), (32, 3),
                     (34, 3), (35, 3), (37, 3), (40, 3), (41, 3), (48, 3), (51, 3), (53, 3), (54, 3), (55, 4), (56, 4),
                     (57, 4), (58, 4), (60, 4), (63, 4), (66, 4), (67, 4), (69, 4), (70, 4), (72, 4), (75, 4), (76, 4),
                     (79, 4), (80, 4), (82, 4), (85, 4), (90, 4), (96, 4), (100, 4), (101, 4), (102, 4), (106, 4),
                     (108, 4), (109, 4), (110, 5), (112, 5), (115, 5), (117, 5), (120, 5), (123, 6), (126, 6), (129, 7),
                     (131, 7), (132, 7), (133, 7), (134, 7), (136, 7), (137, 7), (139, 7), (141, 7), (143, 7), (145, 7),
                     (148, 7), (149, 7), (151, 7), (152, 7), (153, 7), (154, 7), (155, 7), (157, 7), (160, 7), (162, 7),
                     (163, 7), (166, 7), (170, 7), (174, 7), (175, 7), (176, 7), (177, 7), (178, 7), (179, 7), (180, 7),
                     (181, 7), (182, 7), (183, 7), (184, 7), (185, 7), (186, 7), (187, 7), (188, 7), (189, 7), (190, 6),
                     (191, 6), (192, 6)]
        list_ren3 = [(0, 0), (7, 0), (25, 0), (49, 0), (71, 0), (89, 0), (109, 0), (122, 1), (138, 2), (153, 5),
                     (168, 6), (183, 6), (200, 7), (216, 8), (226, 8), (231, 10), (233, 10), (236, 10), (239, 10),
                     (242, 10), (243, 10), (245, 10), (246, 9), (247, 9), (248, 8), (250, 8), (251, 8), (252, 8),
                     (255, 8), (256, 8), (259, 7), (261, 7), (261, 6)]
        list_ren4 = [(0, 0), (2, 0), (3, 0), (5, 0), (6, 0), (8, 0), (9, 0), (11, 0), (12, 0), (13, 0), (14, 0),
                     (15, 0), (21, 0), (28, 0), (34, 0), (37, 0), (40, 0), (46, 0), (49, 0), (53, 0), (57, 0), (61, 0),
                     (65, 0), (70, 0), (74, 1), (77, 1), (79, 1), (80, 1), (82, 1), (84, 1), (87, 1), (90, 1), (93, 3),
                     (97, 4), (98, 4), (99, 4), (100, 4), (101, 4), (103, 4), (105, 4), (106, 5), (107, 5), (110, 5),
                     (112, 5), (113, 5), (114, 5), (115, 5), (117, 5), (119, 5), (121, 5), (122, 5), (123, 5), (124, 5),
                     (125, 5), (128, 5), (129, 5), (131, 5), (134, 6), (135, 6), (136, 6), (137, 6), (137, 7), (139, 7),
                     (141, 7), (144, 8), (147, 8), (149, 9), (150, 9), (151, 10), (153, 10), (155, 10), (157, 11),
                     (160, 11), (161, 11), (163, 11), (167, 13), (169, 13), (171, 13), (173, 13), (174, 13)]
        list_ren = random.choice([list_ren1, list_ren2, list_ren3, list_ren4])
        q = removing / list_ren[-1][0]
        list_moni = []
        for i in list_ren:
            x = int(i[0] * q)
            y = int(i[1] * q)
            list_moni.append((x, y))
        return list_moni

    def move(self, driver, list_moni):
        btn = driver.find_element_by_id("dx_captcha_basic_slider_1")
        mouse_action = ActionChains(driver).click_and_hold(btn)
        movedx = 0
        movedy = 0
        for i in list_moni:
            mouse_action.move_by_offset(i[0] - movedx, i[1] - movedy)
            movedx = i[0]
            movedy = i[1]
        time.sleep(0.48)
        mouse_action.release().perform()

    def process_request(self, request, spider):
        # if 'forbidden' in request.url:
        #     logging.warning('！！！！！！出现验证码 进入中间件处理！！！！！')
        #     # 此处访问要请求的url
        try:
            self.browser.get(request.url)
            # time.sleep(0.1)
            if 'forbidden' in self.browser.current_url:
                # self.browser.delete_all_cookies()
                # logging.info('................清除所有cookie..............')
                self.continuous_count = 0
                logging.warning('·····················出现验证码，开始处理滑块！··············')
                time.sleep(15)
                for i in range(10):
                    time.sleep(2)
                    if '价格区间分布' in self.browser.page_source:
                        logging.info('===============滑块通过成功==============')
                        break
                    if 'id="dx_captcha_basic_wrapper_1"' not in self.browser.page_source:
                        self.browser.refresh()
                        logging.warning('！！！！！！验证码模块未加载出来 刷新页面！！！！！')
                    try:
                        # # 等待一段时间让验证码图片加载出来
                        # time.sleep(2)
                        self.get_yzm(self.browser)
                        # 用来保存验证码样本的计数
                        # self.count = self.count + 1
                    except:
                        logging.warning('！！！！！！代理过慢，验证码未加载出来！！！！！')
                        if '加载失败' in self.browser.page_source:
                            flash = self.browser.find_element_by_xpath("//div[@id='dx_captcha_basic_state-box_1']/a")
                            ActionChains(self.browser).click(flash).perform()
                            logging.warning('！！！！！！验证码加载失败，点击重试！！！！！')

                        elif '该网页无法正常运作' in self.browser.page_source:
                            self.browser.refresh()
                            logging.warning('！！！！！！网页崩溃，刷新页面！！！！！')
                        # time.sleep(2)
                        continue
                    try:
                        removing = self.run()
                    except ValueError:
                        logging.warning('！！！！！！未识别到缺口位置，刷新到下一张验证码重试！！！！！')
                        flash = self.browser.find_element_by_id("dx_captcha_basic_btn-refresh_1")
                        ActionChains(self.browser).click(flash).perform()
                        # time.sleep(1)
                        continue
                    list_moni = self.get_removing(removing)
                    logging.info('-------->-------->正在移动滑块<--------<--------')
                    self.move(self.browser, list_moni)
                    # time.sleep(3)
            else:
                self.continuous_count += 1
                logging.info(f'**************上个验证码通过成功后，连续{self.continuous_count}个url没有出现验证码***************')
        except:
            logging.error("加载页面太慢，停止加载，继续下一步操作")
            self.browser.execute_script("window.stop()")
        url = self.browser.current_url
        body = self.browser.page_source

        return TextResponse(url=url, body=body, encoding="utf-8", request=request)


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
            # 判断距离最后一次使用是否超过一小时 3600
            if hoursCount >= 7200:
                # 第一次使用add cookie 后面直接请求不用再add
                if self.cookie_count == 0:
                    driver.get('http://m.che300.com/estimate/result/3/3/12/209/32814/2019-12/2/1/null/2016/2019')
                    cookie_split = self.cookie.split('; ')
                    for i in cookie_split:
                        # print({'name': i.split('=')[0], 'value': i.split('=')[1]})
                        driver.add_cookie(
                            cookie_dict={'name': i.split('=')[0].strip(), 'value': i.split('=')[1].strip()})
                elif self.cookie_count == 10:
                    logging.warning('=====================该cookie以达到10次 为避免封号 换下一个==============')
                    cookie_dict1 = {"cookie": self.cookie, "last_use_time": self.local_time}
                    r.rpush('che300_gz:cookies', str(cookie_dict1).replace("'", '"'))
                    self.cookie_count = 0
                    self.cookie_str = self.r.blpop("che300_gz:cookies")[1]
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
