import json
import time
import requests
import pymongo
from lxml import etree

client = pymongo.MongoClient(host='192.168.2.149', port=27017)
db = client['chaboshi']
collection = db['xianqian']

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
}

url = f'http://m.chaboshi.cn/wap/cityCarRestriction'
response = requests.get(url=url, headers=headers)
text = response.text
html = etree.HTML(text)


def dingmessage():
    # 请求的URL，WebHook地址
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=633758ccd22b7db4d2e9655488af7d3f5d5e0b2a32c701c80fc3cd57981e73a9"
    # 构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    # 构建请求数据
    tex = "-查博士险迁爬虫报错-"
    message = {
        "msgtype": "text",
        "text": {
            "content": tex
        },
        "at": {
            "isAtAll": False
        }
    }
    # 对请求的数据进行json封装
    message_json = json.dumps(message)
    # 发送请求
    info = requests.post(url=webhook, data=message_json, headers=header)
    # 打印返回的结果
    print(info.text)


try:
    lis = html.xpath('.//li[@class="a1"]')
    for li in lis:
        province = li.xpath('./ul/@id')[0]
        brandcitys = li.xpath('.//div[@class="brandCity"]')
        for brandcity in brandcitys:
            city = brandcity.xpath('./text()')[0]
            standard = brandcity.xpath('./span/text()')[0]
            info = brandcity.xpath('./p/text()')[0]
            meta = {
                'grab_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'province': province,
                'city': city,
                'standard': standard,
                'info': info
            }
            result = collection.insert_one(meta)
            print(meta, result)
except:
    dingmessage()
