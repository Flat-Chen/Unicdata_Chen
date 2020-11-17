import re
import time
from multiprocessing import Process

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import base64
import pytesseract
from PIL import Image
import random


def getProxy():
    s = requests.session()
    s.keep_alive = False
    url = 'http://192.168.2.120:5000'
    headers = {'Connection': 'close'}
    proxy = s.get(url=url, headers=headers, auth=('admin', 'zd123456')).text[0:-6]
    return proxy


# 测试用的车型型号
vehicle_list = ['1147294', '1169769', '1156765', '1147453', '1160536', '1149456', '1156765', '1149708', '1146061',
                '1145964', '1181444', '1146059', '1146058', '1148862', '1204732', '1146065', '1157899', '1181451',
                '1146105', '1150809', '1156765', '1146065', '1156765', '1155641', '1147415', '1146242', '1147295',
                '1149412', '1146242', '1146212', '1149603', '1160536', '1147454', '1146210', '1210141', '1181441',
                '1147415', '1146061', '1155641', '1204732', '1146064', '1147452', '1169769', '1181441', '1146063',
                '1204732', '1149602', '1146060', '1148941']

count = 0
def main():
    global count
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    while 1:
        print(count)
        try:
            chrome_options = Options()
            # chrome_options.add_argument('--headless')
            chrome_options.add_argument('--proxy-server=' + getProxy())
            chrome_options.add_argument('--proxy-server=' + '81.68.214.148:16128')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_argument(
                "–Referer=https://m.che300.com/estimate/result/3/3/1/1/1168837/2020-3/0.1/1/null/2020/2018?rt=1605495553819")
            # driver = webdriver.Chrome(executable_path=r'/estimate/result/3/3/1/1/1168837/2020-3/0.1/1/')
            url = f'https://m.che300.com/estimate/result/3/3/1/1/{random.choice(vehicle_list)}/2019-3/2/1/null/2020/2018?rt=1605495570129'
            browser = webdriver.Chrome(options=chrome_options)
            cookie = "device_id=h51594-a9a6-13b7-b9e8-8ee0; tel=17059143793; pcim=d6780828fb1ed298ad92484369d3128a6c822d94; _dx_uzZo5y=7f687346e5fdd4bf12ca3c4494212c3850b7f2fbb603097f31524246a3d56901c327feaf; _dx_app_f780acccd6e391d352f2076600d5aa16=5fae3c43BXM1tCiabzy6xSgjpckCrSlCcqnQrOG1; PHPSESSID=26b80c0b96c0f24514a037bf43dc19bd454da1a2; Hm_lvt_12b6a0c74b9c210899f69b3429653ed6=1605251770,1605520929; Hm_lvt_f5ec9aea58f25882d61d31eb4b353550=1605251783,1605520929; _che300=xGX1qF%2BixDVqUd2zXUsBLQwsPTeQoUjcGAe%2FL1M3Vn8RwI7aoF%2FFfWi2uRSJ36ZALLZbvzxvU0yT%2FOG5mYY2y9VMvv9mhTmAqeO7FLPjN4hd4nqXfcF9ETiGHtJC%2BEA%2BWvOpoCvVPXGvgoAe4IXML7EPy2WbXKE2yYa%2BNAtmIkLoNc3WS1jj7MPLciQaRkNallIdVIvn9OZ7WYP5Y%2BNZ%2FNRH6WLhFf1DOBLL68mRpA%2FiN0gye3rQe%2BVsdKR9X9RRuSbM9x7k7Zp3mb2G6zjT6OaQ3gTIY3pTxmJaor1w39zP4BE1VNjBCPC%2BUz6b8vAiU1PiD6zy98uPDB5CjRLq1U2jRd0MNziUw0uVuFENyq6GmiZp3eu0cK2CoK0YQfvDlbF%2FoWsEGP4ANEZ%2BNeaJ%2Bqxh8h5S92P7p7jWub6KvAnqjX3CxNoOVdf7OmvAca0i5ey5roWYBJb0wwkgi30xNf2GrCk9Esw1lP3g7Ydv%2Fx7Vw%2FFLa9KNQfZscykoz3LdRVGFiwbniUe7fbgdIJBeqQPjaQDZ%2BxuFvIB%2BoVUPkA24a4jux%2Bk3LBK4YuRR5OFYnkLLYqZ0j2bkmuXESyYcxg%3D%3D5b10e4a8c1108d7ae54d12bea8167022b0d6f91b; zg_did=%7B%22did%22%3A%20%22175c0761d5f128-0032fb81608a41-7f677c6f-1fa400-175c0761d607e8%22%7D; zg_db630a48aa614ee784df54cc5d0cdabb=%7B%22sid%22%3A%201605520928906%2C%22updated%22%3A%201605520934427%2C%22info%22%3A%201605251767662%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.che300.com%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201605520928906%7D; Hm_lpvt_f5ec9aea58f25882d61d31eb4b353550=1605520934; Hm_lpvt_12b6a0c74b9c210899f69b3429653ed6=1605520934; spidercooskieXX12=1605520942; spidercodeCI12X3=94fdb56d6ec83714b463d9297b1772f2"
            browser.get(url)
            cookie = cookie.split(';')
            for i in cookie:
                # print({'name': i.split('=')[0], 'value': i.split('=')[1]})
                browser.add_cookie(cookie_dict={'name': i.split('=')[0].strip(), 'value': i.split('=')[1].strip()})

            browser.get(url)
            # time.sleep(8)
            # browser.maximize_window()
            # print(browser.page_source)
            if '异常提示' in browser.page_source:
                print('```````````````````````````````````````````' + count)
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                break
            img_base64_urls = re.findall('.html\(\'<img src="data:image/png;base64,(.*?)" style="width',
                                         browser.page_source)
            count = count + 1
            browser.quit()
            # print(img_base64_urls)
            for i in img_base64_urls:
                # print(i)
                imgdata = base64.b64decode(i.replace('\n', '').replace('\r', ''))
                file = open('1.jpg', 'wb')
                file.write(imgdata)
                file.close()
                text = pytesseract.image_to_string(Image.open("./1.jpg"), lang="eng").replace(',', '.')
                print(text)


        except:
            continue


main()
# if __name__ == '__main__':
#     # 多进程
#     proc = []
#     for i in range(8):
#         proce = Process(target=main)
#         proce.start()
#         proc.append(proce)
#
#     for proce in proc:
#         proce.join()
