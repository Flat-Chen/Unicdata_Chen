import re
import time
import requests
import json
import base64
from PIL import Image
import pytesseract
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Login:
    def __init__(self, **kwargs):
        self.cookie_txt = open("che300_cookies.txt", "a")
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--proxy-server=' + self.getProxy())
        # self.chrome_options.add_argument('--proxy-server=' + '81.68.214.148:16128')
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.chrome_options.add_argument(
            "–Referer=https://m.che300.com/estimate/result/3/3/1/1/1168837/2020-3/0.1/1/null/2020/2018")
        url = f'https://m.che300.com/estimate/result/3/3/1/1/1156765/2019-3/2/1/null/2020/2018'
        self.browser = webdriver.Chrome(options=self.chrome_options)
        self.browser.get(url)
        self.phone = self.get_phone()

    # 程序完成，自动结束程序
    def __del__(self):
        self.browser.close()
        self.cookie_txt.close()

    @classmethod
    def getProxy(cls):
        url = 'http://192.168.2.120:5000'
        # url = 'http://120.27.216.150:5000'
        headers = {
            'Connection': 'close',
        }
        proxy = requests.get(url, headers=headers, auth=('admin', 'zd123456'), timeout=30).text[0:-6]
        return proxy

    def get_phone(self):
        # 获取手机号
        phone_url = 'http://45.125.46.39:8000/api/yh_qh/id=27762&operator=0&Region=0&card=0&phone=&loop=1&filer=&token=404f60e7cb3f47502753c7b627761555'
        response = requests.get(phone_url)
        response.encoding = response.apparent_encoding
        try:
            print(response.text)
            phone = response.text.split('|')[1]
            return phone
        except Exception as e:
            print('请检查接码平台...', repr(e))

    def get_code(self, phone):
        # 获取短信验证码
        code_url = f'http://45.125.46.39:8000/api/yh_qm/id=27762&phone={phone}&t=zhongd2020&token=404f60e7cb3f47502753c7b627761555'
        try:
            for i in range(24):
                response = requests.get(code_url)
                response.encoding = response.apparent_encoding
                text = response.text.split('|')[1]
                print(text)
                if '验证码为' in text:
                    code = re.findall(r'验证码为：(.*?), 本验证码30分钟内有效', text)[0]
                    print(code)
                    return code
                    break
                else:
                    time.sleep(5)
        except:
            print('请检查接码平台，取验证码出了问题。。。。')

    def lh_phone(self, phone):
        # 拉黑手机号
        lh_url = f'http://45.125.46.39:107/api/yh_lh/id=27762&phone={phone}&token=404f60e7cb3f47502753c7b627761555'
        response = requests.get(url=lh_url)
        response.encoding = response.apparent_encoding
        print(response.text)

    def save_cookie(self, cookie):
        lst = []
        for item in cookie:
            nv = item['name'] + '=' + item['value']
            lst.append(nv)

        self.cookie_txt.write('; '.join(lst) + '\n')
        print('cookie 已保存...')

    def start(self):
        while 1:
            try:
                img_base64 = \
                    re.findall(r'class="refresh"> <img src="data:image/png;base64,(.*?)" class="picCode"></div>',
                               self.browser.page_source)[0]
            except:
                continue

            self.browser.find_element_by_xpath("//input[@name='telnum']").send_keys(self.phone)
            imgdata = base64.b64decode(img_base64)
            file = open('yzm.png', 'wb')
            file.write(imgdata)
            file.close()
            image_obj = Image.open('yzm.png')
            img = image_obj.convert("L")  # 转灰度
            pixdata = img.load()
            w, h = img.size
            threshold = 4  # 该阈值不适合所有验证码，具体阈值请根据验证码情况设置
            # 遍历所有像素，大于阈值的为黑色
            for y in range(h):
                for x in range(w):
                    if pixdata[x, y] < threshold:
                        pixdata[x, y] = 0
                    else:
                        pixdata[x, y] = 255
            yzm_text = pytesseract.image_to_string(img, lang="eng").strip().replace(' ', '')
            print(yzm_text)
            if len(yzm_text) < 4:
                self.browser.find_element_by_xpath('//img[@class="refresh"]').click()
                continue
            else:
                yzm_text = yzm_text[:4]
                self.browser.find_element_by_xpath("//input[@name='check_word']").send_keys(yzm_text)
                try:
                    self.browser.find_element_by_xpath('//span[@class="checkword_button active"]').click()
                except:
                    continue
                time.sleep(2)
                if '秒后再试' in self.browser.page_source:
                    code = self.get_code(self.phone)
                    self.browser.find_element_by_xpath('//input[@placeholder="请输入验证码"]').send_keys(code)
                    time.sleep(2)
                    self.browser.find_element_by_xpath('//div[@class="login_button active"]').click()
                    self.lh_phone(self.phone)
                    time.sleep(5)
                    cookie = self.browser.get_cookies()
                    print(cookie)
                    self.save_cookie(cookie)
                    self.browser.quit()
                    break


if __name__ == '__main__':
    for i in range(20):
        Login().start()
        time.sleep(5)
# import re
# from tqdm import tqdm
# from redis import Redis

# redis_cli = Redis(host="192.168.1.248", port=6379, db=3)
# with open('/home/machao/公共的/田泽瑞/田泽瑞--交接/牛牛汽车/cookies', 'r') as f:
#     lines = f.readlines()
#     for line in tqdm(lines):
#         if line != '\n':
#             redis_cli.sadd("niuniu_cookie", line)
