# %%
import json
import requests
from lxml import etree


# %% 正规贷款
def zgdk(phone):
    data = {'mobile': phone}
    response = requests.post(url='https://mgjr.360yhzd.com/api/sms/getCode', data=data)
    text = response.text
    if '提交成功' in text:
        print('正规贷款信息发送成功!')
    else:
        print('正规贷款信息发送失败！')


# %% 融多多贷款
def rdd(phone):
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
    response = session.post(url='https://91rongduoduo.com/m/center_code', data=data)
    text = response.text
    if '发送成功' in text:
        print('融多多贷款信息发送成功!')
    else:
        print('融多多贷款信息发送失败！')


# %% 穆帅贷款
def ms(phone):
    session = requests.session()
    url = 'http://msswxx.com/m/mss01'
    text = session.get(url).text
    html = etree.HTML(text)
    usertoken = html.xpath('//input[@id="usertoken"]/@value')[0]
    data = {
        'phone': phone,
        'name': '张伟伟',
        'usertoken': usertoken
    }
    response = session.post(url='http://msswxx.com/m/center_code', data=data)
    text = response.text
    if '发送成功' in text:
        print('穆帅贷款信息发送成功!')
    else:
        print('穆帅贷款信息发送失败！')


# %% 郎宇信息
def lyxx(phone):
    data = {'mobile': phone}
    response = requests.post(url='http://www.lyxxjs.com/msm/code/sendSms.do', data=data)
    text = response.text
    if '发送成功' in text:
        print('郎宇信息信息发送成功!')
    else:
        print('郎宇信息信息发送失败！')


# %%
rdd('18822119471')
zgdk('18822119471')
ms('18822119471')
lyxx('18822119471')
