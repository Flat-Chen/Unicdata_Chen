import requests
from requests_html import HTMLSession

session = HTMLSession()


def getProxy():
    # 设置代理
    s = requests.session()
    s.keep_alive = False

    url = 'http://192.168.2.120:5000'
    headers = {
        'Connection': 'close',
    }
    proxy = s.get(url=url, headers=headers, auth=('admin', 'zd123456')).text[0:-6]
    return proxy


proxy = getProxy()
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': '_che300=SOoVQaNf4%2BsEkXOh6Av%2BbS1FgZNx1OeY%2F8JA77%2B07xEmpi6s5k1uJG1lU5jmXrbTnBcxYCdzlu22CsfL0XQvP9%2BDLX30gtWePrSkTAE6cVBy6U3a%2FC9e%2BpnzfR4KjRmqkQOZNaDyUzNN66dIdP5dPIv63L23pkX9JO%2FGfuNVJogywprwjBv%2Bf9d9S%2BmXxuXUTcNM2km6sFWVu71rIr%2F0aR2vHJ9pBnw4T6NhvtMtiUd2VE96kKXBh%2FYmW7sXyyFhGChNeDsIKdlEQj8LHjyoGas6u9S5bjRnlSXWFGwgNA%2BzwnlqIos2Uyg39kSt1bgVZPbJq2uozTMGIqw7smO9AuokOkMbWFyjutXHyz74%2Ffmc37JzL64MYiWiV5RhJBtocT%2B9VEH0mscO5cIp0f9BkBaV2rNsrOksehWR4T%2BpRIv%2FPWzLn5B1skB64LunzffgfLRy%2BC2jmHIYQ6aRwAGlzwxwZZLflGJr8KQdn7qZJrAPSiP8lWgZuzzd%2FCbYAKnXRm7YlJ59v82iAjJH2lf7Cw9qApOTU3xnuQths11l7w4rTYW4prlnM6AAQHoMVypm578vWH8MAa%2F4W%2F5YPfuk0A%3D%3Dd6d75f981ac3c966f4e66b811fbee19be221018d; device_id=; tel=16534186105; pcim=84ceb450bcd9214ab061669659bac1fc54ba4dde; spidercooskieXX12=1606211385; spidercodeCI12X3=804b84067d9b5ec7daa7a2685890802a',
    'Host': 'm.che300.com',
    'Referer': 'https://m.che300.com/estimate/result/3/3/1/1/1146060/2019-3/2/1/null/2020/2018?rt=1605495570129',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
}
# url = 'http://m.che300.com/estimate/result/3/3/1/1/1146060/2019-3/2/1/null/2020/2018?rt=1606211387265'
url = 'http://www.baidu.com'
response = session.get(url=url, headers=headers, proxies={'http': '81.68.214.148:16128'})
response.html.render()
# print(response.cookies.get_dict())
print(response.headers)
print(response.cookies)
print(session)
