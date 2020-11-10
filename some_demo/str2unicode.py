# str1 = r'\u7701\u4efd\u4e2d\u6587\u540d'
# str2 = str1.encode('utf-8').decode('unicode_escape')
# print(str1)
# print(str2)

import json

dict1 = {'value': '省份中文名'}
dict2 = json.dumps(dict1, ensure_ascii=False)
dict3 = json.dumps(dict1)

print(dict1, type(dict1))
print(dict2, type(dict2))
print(dict3, type(dict3))
