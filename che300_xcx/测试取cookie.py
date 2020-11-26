# import requests
#
# # from requests_html import HTMLSession
#
# session = requests.session()
#
#
# def getProxy():
#     # 设置代理
#     s = requests.session()
#     s.keep_alive = False
#
#     url = 'http://192.168.2.120:5000'
#     headers = {
#         'Connection': 'close',
#     }
#     proxy = s.get(url=url, headers=headers, auth=('admin', 'zd123456')).text[0:-6]
#     return proxy
#
#
# proxy = getProxy()
# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Connection': 'keep-alive',
#     'Cookie': '_che300=SOoVQaNf4%2BsEkXOh6Av%2BbS1FgZNx1OeY%2F8JA77%2B07xEmpi6s5k1uJG1lU5jmXrbTnBcxYCdzlu22CsfL0XQvP9%2BDLX30gtWePrSkTAE6cVBy6U3a%2FC9e%2BpnzfR4KjRmqkQOZNaDyUzNN66dIdP5dPIv63L23pkX9JO%2FGfuNVJogywprwjBv%2Bf9d9S%2BmXxuXUTcNM2km6sFWVu71rIr%2F0aR2vHJ9pBnw4T6NhvtMtiUd2VE96kKXBh%2FYmW7sXyyFhGChNeDsIKdlEQj8LHjyoGas6u9S5bjRnlSXWFGwgNA%2BzwnlqIos2Uyg39kSt1bgVZPbJq2uozTMGIqw7smO9AuokOkMbWFyjutXHyz74%2Ffmc37JzL64MYiWiV5RhJBtocT%2B9VEH0mscO5cIp0f9BkBaV2rNsrOksehWR4T%2BpRIv%2FPWzLn5B1skB64LunzffgfLRy%2BC2jmHIYQ6aRwAGlzwxwZZLflGJr8KQdn7qZJrAPSiP8lWgZuzzd%2FCbYAKnXRm7YlJ59v82iAjJH2lf7Cw9qApOTU3xnuQths11l7w4rTYW4prlnM6AAQHoMVypm578vWH8MAa%2F4W%2F5YPfuk0A%3D%3Dd6d75f981ac3c966f4e66b811fbee19be221018d; device_id=; tel=16534186105; pcim=84ceb450bcd9214ab061669659bac1fc54ba4dde; spidercooskieXX12=1606211385; spidercodeCI12X3=804b84067d9b5ec7daa7a2685890802a',
#     'Host': 'm.che300.com',
#     'Referer': 'https://m.che300.com/estimate/result/3/3/1/1/1146060/2019-3/2/1/null/2020/2018?rt=1605495570129',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'same-origin',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
# }
# url = 'http://m.che300.com/estimate/result/3/3/1/1/1146060/2019-3/2/1/null/2020/2018'
# # url = 'http://www.baidu.com'
# response = session.get(url=url, headers=headers, proxies={'http': '81.68.214.148:16128'})
# # response.html.render()
# # print(response.cookies.get_dict())
# print(response.headers['Set-Cookie'])
#
#
#
cookie1 = [{'domain': 'm.che300.com', 'httpOnly': False, 'name': 'PHPSESSID', 'path': '/', 'secure': False,
            'value': 'e244923c55ad042e4a6951c5aabb266cde8e51e5'},
           {'domain': 'm.che300.com', 'expiry': 1606424815, 'httpOnly': False, 'name': '_che300', 'path': '/',
            'secure': False,
            'value': 'R6iRutWQIVb5uBpHRDzerQwUHezAWFLJQeqiTA12UZ72v7PrF3cfuQctPmIVRt%2FyLvTy%2B6UStMDqWBHAZvTrtLxEkeHhIi53XjFHX%2Ba40bBlbMq%2FWnJHACjdrhp2UIjpGoFNA7HU5cFjFXjJOFNq8NYYCavmSinpTP9hYSLsmJ%2FRqzcbi7vB7kU58RViEOFA5lK47DjWeISpx3dZ6Vh7PfJeJ%2Fngwqi0DB3u0g0GqMG%2Fjitw8pTnXkd1MNSVMhtR%2FL6DpMItQQlXqlZM%2FvWEK%2BLt4kRoWfCL0ePqv7L%2BPhGbWSNAi5CsNI4M2kuc52nEEdyNXTmkEC0%2BCQ9j8djEY3EW3sKmozfuGWGYtmncZ7Y7NYuZ8NKheMmKL7OgsmY6m5x2uQPEPyH7xjLCsUQlsxDG%2BzG7keTHI41HTvoeCv0Q%2FgZp%2B4uRpIy8oTQ%2BkGLBPyS1AdV723TGr3%2BZ7iTnZ2aut0z435Rvk9pahUJd0Nvf1jrqO2I3JkPYdzEJDCzsO38x97dMRUX25aMeUDOnJe%2FvhfHO4q00XqriNxUgwCAO7xzesHbs6CUMzUgPY%2FKsK2WKMH6%2BPn%2FFVdMLvdQVRsMnyBkYiMi24j%2Blc4XBdTvQH66of3DU2WX%2FSjl%2B06pQc61828cf8f8458278b380667653e5b644b81078a'},
           {'domain': 'm.che300.com', 'httpOnly': False, 'name': 'spidercodeCI12X3', 'path': '/', 'secure': False,
            'value': '25e85c61f194c7c0c95692e065f8daaa'},
           {'domain': '.che300.com', 'expiry': 1621933614, 'httpOnly': False, 'name': 'pcim', 'path': '/',
            'secure': False, 'value': '46db3306c5f6096d0bc72f86d4bf1e53f270b36f'},
           {'domain': '.che300.com', 'expiry': 1621933614, 'httpOnly': False, 'name': 'tel', 'path': '/',
            'secure': False, 'value': '17059185578'},
           {'domain': 'm.che300.com', 'httpOnly': False, 'name': 'spidercooskieXX12', 'path': '/', 'secure': False,
            'value': '1606381613'},
           {'domain': '.che300.com', 'expiry': 1621933614, 'httpOnly': False, 'name': 'device_id', 'path': '/',
            'secure': False, 'value': 'h5a81f-3aed-0075-f145-484a'}]
cookie2 = [{'domain': '.che300.com', 'httpOnly': False, 'name': 'Hm_lpvt_f5ec9aea58f25882d61d31eb4b353550', 'path': '/',
            'secure': False, 'value': '1606381671'},
           {'domain': '.m.che300.com', 'httpOnly': False, 'name': 'Hm_lpvt_12b6a0c74b9c210899f69b3429653ed6',
            'path': '/', 'secure': False, 'value': '1606381671'},
           {'domain': 'm.che300.com', 'httpOnly': False, 'name': 'spidercodeCI12X3', 'path': '/', 'secure': False,
            'value': '315f2b5b7e56d1bc0a8c4e37dc1d0662'},
           {'domain': '.m.che300.com', 'expiry': 1637917670, 'httpOnly': False,
            'name': 'Hm_lvt_12b6a0c74b9c210899f69b3429653ed6', 'path': '/', 'secure': False, 'value': '1606381671'},
           {'domain': '.che300.com', 'expiry': 1621933669, 'httpOnly': False, 'name': 'device_id', 'path': '/',
            'secure': False, 'value': 'h590f1-2fcf-1d1c-b36e-e77a'},
           {'domain': 'm.che300.com', 'httpOnly': False, 'name': 'PHPSESSID', 'path': '/', 'secure': False,
            'value': '01c5e593a24dabe7d59b152d87419cd2743033f6'},
           {'domain': '.che300.com', 'expiry': 1637917671, 'httpOnly': False,
            'name': 'Hm_lvt_f5ec9aea58f25882d61d31eb4b353550', 'path': '/', 'secure': False, 'value': '1606381671'},
           {'domain': 'm.che300.com', 'httpOnly': False, 'name': 'spidercooskieXX12', 'path': '/', 'secure': False,
            'value': '1606381668'},
           {'domain': 'm.che300.com', 'expiry': 1606424870, 'httpOnly': False, 'name': '_che300', 'path': '/',
            'secure': False,
            'value': '49ggo40vk4h3iJT5%2BLTwAHg6AxVw9Wym1Zwje%2B3EPwjrT5hhpgkguvXpJmYtr7pFE5YoT0wglOzQOd9yoZUJgxmYDIH6ufJSnlE3KnHuO53gn7ZWin%2F8Kn9%2BGIcUvOSVjDjRe0GE7lbyoQkSuaITQCFG9UC8yx4fFd2dv3lW9sLdDxiyf36llWU44fzRxYGDXN%2FQ0OHCoChxFhXlHG3x7cFXfbkqvObbhcTXSuaS72NEP4Tz3iXVfcolVEDJrRmDFEzO1UJFNE3zC4M1P6b%2FzrIrrQHtbT9Da4OF4Bi9njYg%2FH1in2FGfxJhrW72g8bFX3WeG1Q5cSx%2BO5XkX2fr5lsDkJ9HAuEyscTG5l8ME7Jjz2YsbUx%2B5temAqxTb7vj70oKbYGhUEifCdyDrpiBue8IM0ChU9PbFaFrMiY1jgJohpYTKXpV9%2BLg%2BPJ%2BLQxkqDFhClATtA5N%2BwChnxh6eCwQI6gYq5CB%2BWQqe121xvHBuGGuqWkpslbgTGEfCXGHYSM0Z1lz7PrQE8Zunkdh4TKtc%2B8HfukTPmKuE0nGFDxCKbh8efp2%2FwYy2z4bBWXtwOmH2L8jMhOQAlYfTuSNP9izX7wkdu%2B9P4ZGWaObmZ58taaoG8F%2FaJrEKxeyFCr58258945135585a5eb13c550557e41ae6d783a34f'},
           {'domain': '.che300.com', 'expiry': 1637917671, 'httpOnly': False,
            'name': 'zg_db630a48aa614ee784df54cc5d0cdabb', 'path': '/', 'secure': False,
            'value': '%7B%22sid%22%3A%201606381671041%2C%22updated%22%3A%201606381671041%2C%22info%22%3A%201606381671045%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.che300.com%22%7D'},
           {'domain': '.che300.com', 'expiry': 1621933669, 'httpOnly': False, 'name': 'pcim', 'path': '/',
            'secure': False, 'value': 'b72487323c369fbe694f3fbd222ac1abd1a336bf'},
           {'domain': '.che300.com', 'expiry': 1621933669, 'httpOnly': False, 'name': 'tel', 'path': '/',
            'secure': False, 'value': '17059177438'},
           {'domain': '.che300.com', 'expiry': 1637917671, 'httpOnly': False, 'name': 'zg_did', 'path': '/',
            'secure': False,
            'value': '%7B%22did%22%3A%20%2217603cf127a25f-01658fe7a8367e-930346c-1fa400-17603cf127b248%22%7D'}]


def save_cookie(cookie):
    lst = []
    for item in cookie:
        nv = item['name'] + '=' + item['value']
        lst.append(nv)
    cookie_txt = open("che300_cookies.txt", "a")
    cookie_txt.write('; '.join(lst) + '\n')
    print('cookie 已保存...')


save_cookie(cookie2)
