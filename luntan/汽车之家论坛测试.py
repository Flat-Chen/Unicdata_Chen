import requests
import json

headers = {'Referer': 'https://club.autohome.com.cn/',
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}

url = 'https://club.autohome.com.cn/frontapi/topics/getByBbsId?pageindex=2&pagesize=100&bbs=c&bbsid=692&fields=topicid%2Ctitle%2Cpost_memberid%2Cpost_membername%2Cpostdate%2Cispoll%2Cispic%2Cisrefine%2Creplycount%2Cviewcount%2Cvideoid%2Cisvideo%2Cvideoinfo%2Cqainfo%2Ctags%2Ctopictype%2Cimgs%2Cjximgs%2Curl%2Cpiccount%2Cisjingxuan%2Cissolve%2Cliveid%2Clivecover%2Ctopicimgs&orderby=topicid-'

response = requests.get(url=url, headers=headers)

pinglun_url_dict = json.loads(response.text)

for pinglun_url in pinglun_url_dict["result"]["list"]:
    item = {}
    if pinglun_url['isvideo'] is 1:
        # print(pinglun_url['isvideo'])
        pass

    else:
        # print(pinglun_url['isvideo'])
        item['posted_time'] = pinglun_url['postdate']
        item['tiezi_url'] = url = pinglun_url["url"]
        print(pinglun_url['title'])
