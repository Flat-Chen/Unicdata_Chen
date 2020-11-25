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

        try:
            chrome_options = Options()
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--proxy-server=' + getProxy())
            chrome_options.add_argument('--proxy-server=' + '81.68.214.148:16128')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_argument(
                "–Referer=https://m.che300.com/estimate/result/3/3/1/1/1168837/2020-3/0.1/1/null/2020/2018")
            # driver = webdriver.Chrome(executable_path=r'/estimate/result/3/3/1/1/1168837/2020-3/0.1/1/')
            url = f'https://m.che300.com/estimate/result/3/3/1/1/{random.choice(vehicle_list)}/2019-3/2/1/null/2020/2018'
            browser = webdriver.Chrome(options=chrome_options)
            cookie1 = "device_id=h51594-a9a6-13b7-b9e8-8ee0; tel=17059143793; pcim=d6780828fb1ed298ad92484369d3128a6c822d94; _dx_uzZo5y=7f687346e5fdd4bf12ca3c4494212c3850b7f2fbb603097f31524246a3d56901c327feaf; _dx_app_f780acccd6e391d352f2076600d5aa16=5fae3c43BXM1tCiabzy6xSgjpckCrSlCcqnQrOG1; PHPSESSID=26b80c0b96c0f24514a037bf43dc19bd454da1a2; Hm_lvt_12b6a0c74b9c210899f69b3429653ed6=1605251770,1605520929; Hm_lvt_f5ec9aea58f25882d61d31eb4b353550=1605251783,1605520929; _che300=xGX1qF%2BixDVqUd2zXUsBLQwsPTeQoUjcGAe%2FL1M3Vn8RwI7aoF%2FFfWi2uRSJ36ZALLZbvzxvU0yT%2FOG5mYY2y9VMvv9mhTmAqeO7FLPjN4hd4nqXfcF9ETiGHtJC%2BEA%2BWvOpoCvVPXGvgoAe4IXML7EPy2WbXKE2yYa%2BNAtmIkLoNc3WS1jj7MPLciQaRkNallIdVIvn9OZ7WYP5Y%2BNZ%2FNRH6WLhFf1DOBLL68mRpA%2FiN0gye3rQe%2BVsdKR9X9RRuSbM9x7k7Zp3mb2G6zjT6OaQ3gTIY3pTxmJaor1w39zP4BE1VNjBCPC%2BUz6b8vAiU1PiD6zy98uPDB5CjRLq1U2jRd0MNziUw0uVuFENyq6GmiZp3eu0cK2CoK0YQfvDlbF%2FoWsEGP4ANEZ%2BNeaJ%2Bqxh8h5S92P7p7jWub6KvAnqjX3CxNoOVdf7OmvAca0i5ey5roWYBJb0wwkgi30xNf2GrCk9Esw1lP3g7Ydv%2Fx7Vw%2FFLa9KNQfZscykoz3LdRVGFiwbniUe7fbgdIJBeqQPjaQDZ%2BxuFvIB%2BoVUPkA24a4jux%2Bk3LBK4YuRR5OFYnkLLYqZ0j2bkmuXESyYcxg%3D%3D5b10e4a8c1108d7ae54d12bea8167022b0d6f91b; zg_did=%7B%22did%22%3A%20%22175c0761d5f128-0032fb81608a41-7f677c6f-1fa400-175c0761d607e8%22%7D; zg_db630a48aa614ee784df54cc5d0cdabb=%7B%22sid%22%3A%201605520928906%2C%22updated%22%3A%201605520934427%2C%22info%22%3A%201605251767662%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.che300.com%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201605520928906%7D; Hm_lpvt_f5ec9aea58f25882d61d31eb4b353550=1605520934; Hm_lpvt_12b6a0c74b9c210899f69b3429653ed6=1605520934; spidercooskieXX12=1605520942; spidercodeCI12X3=94fdb56d6ec83714b463d9297b1772f2"
            cookie2 = '_che300=52lTBBpu15xdlMHkfeL2Y7TAHgMEMy2mHV1j8QqiEvHy36GbMnjMS57gvFlhTaOdCvFSaMXUL1W4Ano5MO%2BLe0OfZ9zoa7rykTxK5f3UmKNkrDW4tsItRcXvBO7lvGBP5DY3PIFfzyPKYXg61wbT6ntAU2Qd92PcXAa9gh%2FC9YWRH69vgJ1A1GlCZzKeScmD4t6YNAgYfeJ6k2N7hofTfmrEfcll5XtFQWJWO5e33w6LFBTb%2BRo0tHpmV%2BvlqavTFJ3GC%2BrmgbSUTFap1A4Y%2B2o6xWLU3yCzeOzOzbbMGXAxgo10aE9jAAHGV0cNjpfWQESJP58tFLmg6Ng3q4%2BxGn6GPpvz%2BUX%2BkkuPjOfzzgJi7kK0Ptx03%2B858lUW0KLOdd2z6uq80ll8v22ExOR4QDymWzuvlDl9OGPyYDORrSSloURB6OiORnXPxO8RMZMzSZsara%2BI0QcUyMvYFQIdK7BvmZl6RkH8OnrHnCnY34ddnfMUn217%2FraPWR%2F4tL%2BnnASyTMiO03aRzMcpGepMp4lleXyX%2B67EdVacnbNaNaaF%2F8MjmpXp%2B4tSZPJHnkqXnOtCVeYh%2BlCBppRyf77jTw%3D%3D6135e9a20559694094d0d04c3e7d74cda214ac05; device_id=h5440d-13b2-2133-c307-46aa; tel=17069135178; pcim=1b3b972a90bc8b3c233e7e524062404f81487462; spidercooskieXX12=1606210998; spidercodeCI12X3=fb0e20806acb7beae6799c2f35409d2b'
            cookie3 = '_che300=SOoVQaNf4%2BsEkXOh6Av%2BbS1FgZNx1OeY%2F8JA77%2B07xEmpi6s5k1uJG1lU5jmXrbTnBcxYCdzlu22CsfL0XQvP9%2BDLX30gtWePrSkTAE6cVBy6U3a%2FC9e%2BpnzfR4KjRmqkQOZNaDyUzNN66dIdP5dPIv63L23pkX9JO%2FGfuNVJogywprwjBv%2Bf9d9S%2BmXxuXUTcNM2km6sFWVu71rIr%2F0aR2vHJ9pBnw4T6NhvtMtiUd2VE96kKXBh%2FYmW7sXyyFhGChNeDsIKdlEQj8LHjyoGas6u9S5bjRnlSXWFGwgNA%2BzwnlqIos2Uyg39kSt1bgVZPbJq2uozTMGIqw7smO9AuokOkMbWFyjutXHyz74%2Ffmc37JzL64MYiWiV5RhJBtocT%2B9VEH0mscO5cIp0f9BkBaV2rNsrOksehWR4T%2BpRIv%2FPWzLn5B1skB64LunzffgfLRy%2BC2jmHIYQ6aRwAGlzwxwZZLflGJr8KQdn7qZJrAPSiP8lWgZuzzd%2FCbYAKnXRm7YlJ59v82iAjJH2lf7Cw9qApOTU3xnuQths11l7w4rTYW4prlnM6AAQHoMVypm578vWH8MAa%2F4W%2F5YPfuk0A%3D%3Dd6d75f981ac3c966f4e66b811fbee19be221018d; device_id=; tel=16534186105; pcim=84ceb450bcd9214ab061669659bac1fc54ba4dde; spidercooskieXX12=1606211385; spidercodeCI12X3=804b84067d9b5ec7daa7a2685890802a'
            browser.get(url)
            cookie = cookie3.split(';')
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
            price_list = []
            for i in img_base64_urls:
                # print(i)
                imgdata = base64.b64decode(i.replace('\n', '').replace('\r', ''))
                file = open('1.jpg', 'wb')
                file.write(imgdata)
                file.close()
                text = pytesseract.image_to_string(Image.open("./1.jpg"), lang="eng").replace(',', '.').replace(
                    '\n\x0c', '').strip()
                # print(text)
                price_list.append(text)
            print(price_list)
            print(count)
            # time.sleep(5)
        except:
            pass


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
