import re
import time
import requests
import json
import base64
from PIL import Image
import pytesseract


class Login:
    def __init__(self, **kwargs):
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
        # self.getProxy = '81.68.214.148:16128'
        self.phone = phone
        # self.cookie_txt = open("che300_cookies.txt", "a")

    @classmethod
    def getProxy(cls):
        # url = 'http://192.168.2.120:5000'
        url = 'http://120.27.216.150:5000'
        headers = {
            'Connection': 'close',
        }
        proxy = requests.get(url, headers=headers, auth=('admin', 'zd123456'), timeout=30).text[0:-6]
        return proxy

    def get_captcha(self):
        # 获取验证码及key
        url = 'http://dingjia.che300.com/api/lib/web_verify/get_captcha/'
        response = self.session.get(url=url, headers=self.headers, proxies={'http': self.get_Proxy()})
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
        threshold = 8  # 该阈值不适合所有验证码，具体阈值请根据验证码情况设置
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
        # 验证验证码受否正确 正确即可获得短信验证码
        while 1:
            yzm_text, key = self.get_captcha()
            # print(yzm_text, key)
            url = 'http://dingjia.che300.com/api/lib/web_verify/check_captcha'
            data = {
                'tel': self.phone,
                'captcha': yzm_text,
                'key': key
            }
            response = self.session.post(url=url, data=data, headers=self.headers, proxies={'http': self.get_Proxy()})
            print(response.text)
            if '"msg":"ok"' in response.text:
                print('验证成功')
                break
            else:
                print('验证失败，重试！')

    def login_by_code(self, code):
        url = 'http://dingjia.che300.com/api/lib/web_verify/login_by_code'
        data = {
            'tel': self.phone,
            'code': code
        }
        response = self.session.post(url=url, data=data, headers=self.headers, proxies={'http': self.get_Proxy()})
        print(data)
        print('注册验证接码平台验证码')
        print(response.text)
        print('``````````````````````````````准备开始获取cookie```````````````````````````````')
        last_url = 'http://m.che300.com/estimate/result/3/3/1/1/1146060/2019-3/2/1/null/2020/2018'
        response = self.session.get(url=last_url, headers=self.headers, proxies={'https': self.get_Proxy()})
        print(response.text)
        print(response.headers['Set-Cookie'])
        return response.headers['Set-Cookie']


class jiema:
    def __init__(self, **kwargs):
        pass

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


if __name__ == '__main__':
    jiema = jiema()
    phone = jiema.get_phone()
    print(phone)
    session = requests.session()
    login = Login()
    login.check_captcha()
    code = jiema.get_code(phone)
    print(code)
    jiema.lh_phone(phone)
    cookie = login.login_by_code(code)
    print(cookie)
