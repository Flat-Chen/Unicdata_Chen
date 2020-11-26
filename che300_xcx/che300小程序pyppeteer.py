import requests
from requests_html import HTMLSession

headers = {
    'Host': 'dingjia.che300.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://m.che300.com',
    'Connection': 'keep-alive',
    'Referer': 'http://m.che300.com/estimate/result/3/3/1/1/1146060/2019-3/2/1/null/2020/2018',
    'Cache-Control': 'max-age=0',
    'TE': 'Trailers',
    'cookie': '_che300=B44P2hgaHG5R7OiuYZMc93%2B3k2ErYRbT0IVfIlL2P0ZMwRSYsqvhsizNU%2FcRmUl6MvUPqrzEm3xMK0%2FS%2BmM6woQijd2IvdqtveHsFzsMWXdW%2BXzCsmlP00X8QxhruimfJv40Z%2FPd5e3TupFETgdjvOyKiGE%2F4F0scNeYGhuJeKarLfPmuelJB%2BWukjNW7lCBaDBB3uo3IKeBN49%2BEBYPh2q6zjldiMah8qFNbO7U9bDV7i3smJomTN2efSzJGwvP77RE7D%2FIIeIyo3XV5Ck4pEXDdTFKL5oTJKU7l%2BiyjgRFZi7nPZ2ZRmbcRyNeIseZ%2B8YJHmRXUOdgjUg4JCjfhJngHa9DQUKNaMEsz7KOIkH3Frl5ERJ883x1%2BHW7Q5PPQgEcARUzItabxyJq7y4QHXuAMq3iUA1fq9foAoI%2BLGcaxwYFe8NBALr6pXMUjQ5fGbPuBQRyKVHxYDic0UwdJaPwa3VN1RDdCsLV2z8UFn9QyJpE57E8eX6Nz%2BN0FE4JgMzgC3oIngIQehhEc5PMfSKf3qFmKHiF2Azg4SF1%2BJoI4fauK26QL0dThpht3Pp7txFGsSKcR76F%2BGf4FQ5nMQ%3D%3D869e30c2de5d2c9f3bc82e6998f14334453cfc78; device_id=h59001-eef9-d63d-da29-b97c; tel=17053817574; pcim=6858243a56e7d68c01814c03c49ff6d9de12156b; spidercooskieXX12=1606297890; spidercodeCI12X3=5dfa606137d26fe3c80c49c4b86ddf39',
}
session = HTMLSession()
url = "http://m.che300.com/estimate/result/3/3/1/1/1146060/2019-3/2/1/null/2020/2018"
response = session.get(url=url, headers=headers)
response.html.render()
print(response.text)
