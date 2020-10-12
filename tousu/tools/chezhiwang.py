__author__ = 'cagey'
import requests


header = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
def getProxy():
    url='http://120.27.216.150:5000'
    headers = {
        'Connection': 'close',
    }
    proxy = requests.get(url, headers=headers, auth=('admin', 'zd123456')).text[0:-6]
    return proxy

url = "http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-1.shtml"
proxy = getProxy()
print(proxy)
proxy = {"http": proxy}
res = requests.get(url=url, headers=header, proxies=proxy)
print(res.text)













