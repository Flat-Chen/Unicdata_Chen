__author__ = 'cagey'
import requests

url = "http://m.jingzhengu.com/sale-s131317-r2019-3-1-m20000-c2401-y-j-h"

res = requests.get(url)
print(res.text)



