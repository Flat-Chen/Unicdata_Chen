import time

import requests
import json
import base64
from PIL import Image
import matplotlib.pyplot as plt
import pytesseract


def getProxy():
    # 设置代理
    s = requests.session()
    s.keep_alive = False

    url = 'http://192.168.2.120:5000'
    headers = {
        'Connection': 'close',
    }
    proxy = s.get(url=url, headers=headers, auth=('admin', 'zd123456')).text[0:-6]
    return proxy


class Login:
    def __init__(self, session, proxy, phone):
        self.headers = {
            'Host': 'dingjia.che300.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://m.che300.com',
            'Connection': 'keep-alive',
            'Referer': 'https://m.che300.com/login_page?redirect_url=https%3A%2F%2Fm.che300.com%2Festimate%2Fresult%2F3%2F3%2F1%2F1%2F1147294%2F2019-3%2F2%2F1%2Fnull%2F2020%2F2018%3Frt%3D1605599950195',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
        }
        self.session = session
        self.getProxy = proxy
        self.phone = phone
        self.cookie_txt = open("che300_cookies.txt", "a")

    @classmethod
    def get_Proxy(cls):
        url = 'http://192.168.2.120:5000'
        #         url = 'http://120.27.216.150:5000'
        headers = {
            'Connection': 'close',
        }
        proxy = requests.get(url, headers=headers, auth=('admin', 'zd123456'), timeout=30).text[0:-6]
        return proxy

    # 程序完成，自动结束程序
    def __del__(self):
        self.cookie_txt.close()

    def get_captcha(self):
        # 获取验证码及key
        url = 'http://dingjia.che300.com/api/lib/web_verify/get_captcha/'
        response = self.session.get(url=url, headers=self.headers, proxies={'http': self.getProxy})
        try:
            json_data = json.loads(response.text)
        except:
            print(response.text)
        captcha = json_data['data']['captcha']
        key = json_data['data']['key']
        img_base64 = captcha.split(';base64,')[1]
        imgdata = base64.b64decode(img_base64)
        file = open('yzm.png', 'wb')
        file.write(imgdata)
        file.close()
        # 查看验证码图片
        # image_obj = Image.open('yzm.png')
        # image_obj.show()
        image_obj = Image.open('yzm.png')
        img = image_obj.convert("L")  # 转灰度
        pixdata = img.load()
        w, h = img.size
        threshold = 20  # 该阈值不适合所有验证码，具体阈值请根据验证码情况设置
        # 遍历所有像素，大于阈值的为黑色
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        yzm_text = pytesseract.image_to_string(img, lang="eng").strip().replace(' ', '')
        return yzm_text, key

    def check_captcha(self):
        yzm_text, key = self.get_captcha()
        # print(yzm_text, key)
        url = 'http://dingjia.che300.com/api/lib/web_verify/check_captcha'
        data = {
            'tel': self.phone,
            'captcha': yzm_text,
            'key': key
        }
        response = self.session.post(url=url, data=data, headers=self.headers, proxies={'http': self.getProxy})
        print(response.text)
        if '"msg":"ok"' in response.text:
            print('验证成功')
            print(response.cookies)

    def login_by_code(self):
        yzm_code = 111111
        url = 'http://dingjia.che300.com/api/lib/web_verify/login_by_code'
        data = {
            'tel': self.phone,
            'code': yzm_code
        }


if __name__ == '__main__':
    for i in range(10):
        try:
            proxy = getProxy()
            session = requests.session()
            phone = '18876542121'
            login = Login(session, proxy, phone)
            login.check_captcha()
            time.sleep(1)
        except:
            continue
