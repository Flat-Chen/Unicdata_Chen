import requests
import time
from requests_html import HTMLSession

sessions = HTMLSession()



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
    # ':authority': 'm.che300.com',
    # ':method': 'GET',
    # ':path': '/estimate/result/3/3/1/1/1168837/2020-3/0.1/1/null/2020/2018?rt=1605251781923',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie': 'Hm_lvt_f5ec9aea58f25882d61d31eb4b353550=1595925864,1596005831,1596442514; device_id=h51594-a9a6-13b7-b9e8-8ee0; tel=17059143793; pcim=d6780828fb1ed298ad92484369d3128a6c822d94; PHPSESSID=36bd199f70856d1fba8fa346851054e867947c8f; zg_did=%7B%22did%22%3A%20%22175c0761d5f128-0032fb81608a41-7f677c6f-1fa400-175c0761d607e8%22%7D; zg_db630a48aa614ee784df54cc5d0cdabb=%7B%22sid%22%3A%201605251767656%2C%22updated%22%3A%201605251767656%2C%22info%22%3A%201605251767662%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.che300.com%22%7D; Hm_lvt_12b6a0c74b9c210899f69b3429653ed6=1605251770; Hm_lpvt_12b6a0c74b9c210899f69b3429653ed6=1605251770; _che300=Ouq8dx4EP2piOc72uNIH1to0xcj7jc%2BpQBHIPk68QI%2FHB18lBH0McQEFQpr%2BimerySvr9jbsufi4KA82ox%2BLgOZKz5Jo5rvAA3L0RXw85qb6FpwcwPExf0xnRNg%2BILNwhMtZ3eICU2YCag2ua8LHMLcjxCmyLKayGfNMZ611yRU2jbd%2F0oUMEew35QQlnvZ1lhAH4QY4yik%2BKr5eSuQ8xwX6NPUDTB35wVVHFNstYF7QbXoyIzExtGI4pZjOZtSs%2Fb7JRIENYtiFukidILCFAbItKpyusRrIN4Wzlq8uWrCHXm9FD48b7VtB%2BYRVnQrJJ1JHZHOajL4qp7Mr5maUm80uzYq2%2FKA3Fb4up2CzpZFfiACzRWPyUJ8uFrdW7S3CHlXpziAUniDbM%2BIllDWl5qHFtU45VWiGFU0o4CruboHgP3oQ8t%2F4TWHVDNrpHk5pomwd%2FbVhQyU8%2F7r5fDxbLYgMfMfJWIwdJ0%2Bd8TpGHujKnvwJ9AaK0HGRgYtLwUjd5lyxeRfBU52p4enKyjltOlKUsA7slPB1U4%2B9qB2I5RA%3Ddf9bb4103eaeceb358d6290627955458d5e60a89; spidercooskieXX12=1605251781; spidercodeCI12X3=6f0f7ea02093598ac2c29c170c60bdd7',
    'referer': 'https://m.che300.com/estimate/result/3/3/1/1/1168837/2020-3/0.1/1/null/2020/2018?rt=1605251766081',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/86.0.4240.193',
}
url = 'https://m.che300.com/estimate/result/3/3/1/1/1168837/2020-3/0.1/1/null/2020/2018?rt=1605251781923'
proxy = {'http': getProxy()}
response = sessions.get(url=url, headers=headers, proxies=proxy, verify=False)
response.html.render()
# print(response.text)
