import json
import requests
import docker


def dingmessage(tex):
    # 请求的URL，WebHook地址
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=19bfd85d8430457c13e778f5cc7d3ff2686914288b5b2464ce353e088206a655"
    # 构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    # 构建请求数据
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
    client = docker.from_env()
    container = client.containers.get('autohome_koubei_0916')
    container.start()
    tex = '-dpcker爬虫 autohome_koubei启动成功-'
    dingmessage(tex)
except Exception as e:
    tex = '-docker爬虫启动出错 {}-'.format(e)
    dingmessage(tex)
