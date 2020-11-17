import base64
import pytesseract
from PIL import Image
import random

# yzm = 'iVBORw0KGgoAAAANSUhEUgAAAFAAAAAUCAMAAAAtBkrlAAABOFBMVEX///+j6ZUAAAD8coJi1m90twh14s0YI/a79vd0SbwpelbSo3KtyBXMP0T0A8h9+04GkODW4CVh4LEWCUd//tHxgzXLV+ITCUPuMqvu+hPReTQdzdg2XkS8ye2zTSocjUdxPZlYFIe6cj/ON9UOTJWJC+iSS3rfkIhI6AirgRWugxnMfKCFrShsxp2FZu7r+ZtZ9257olTurBgobomPln+dcgFMyE/D7rbBGuKjGAPmJyHfEnejQCCxlDTGuvh0m9sAXYosjFc64tUPgWZKt+dCacwxUNQtagzqQ7/PAD2iUVSP+j6d9Kq7ZVfeui5pu+nF5BHfMPPheGNvnXN1CouPDKw7c0cAVY5zEfwAZqYzkeJlEsNsTyPVHBWFMukhvRI5EucTKaUTRnc/0FgrrisA4wiBh9oc2mx0El5yAAABVklEQVQ4jZ2UhY7AIAyGV3aanEty7q45d3fNubu+/xscgw4ZMMg1GYXy92sh26LzB2DWwh0Uc/cMupVAoEWbzq0lMVsPIZ0gcEiJdXhyBpKhlE0LXZrIX/rTJygLAj76K73bghRImJXTRTMGCfHTeJYpjNJ0sVcJVWFAe+now7KlyUa529i3AC+T8QlgxeiwIAskN3ptUi8OOPgdx/HirqvDhfQ2ulQgsWmTSJwYwJa4w5EGKWjiHQ5j7Z4d/ciS2MlGZGkaasuZDvmW3g4hRZhyR/0b0lCyRp9u2wGmBbA1exkVP5ANGQD7m1CjvTaNUsybnoB+Zz4PrBpIDnxBwa8QU+YeHKv57KZnReBeq3ALfRJ4CLBta/9/pn/L82ysC08fR3+Gfsrxc7gCqFXXbcq8mo2v+R1eAPTy9VFuQzOn6WxSBtsN4JiyPsgFUpuT0y/01+r+HywGGquUEsnUAAAAAElFTkSuQmCC'
# imgdata = base64.b64decode(yzm)
# file = open('1.png', 'wb')
# file.write(imgdata)
# file.close()
# text = pytesseract.image_to_string(Image.open("1.png"))
# print(text)
import requests


def getProxy():
    s = requests.session()
    s.keep_alive = False

    url = 'http://120.27.216.150:5000'
    headers = {
        'Connection': 'close',
    }
    proxy = s.get(url=url, headers=headers, auth=('admin', 'zd123456')).text[0:-6]
    return proxy


headers = {
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
url = 'http://dingjia.che300.com/api/lib/web_verify/get_captcha'
proxy = {'http': getProxy()}
response = requests.get(url=url, headers=headers, proxies=proxy)
print(response.text)
