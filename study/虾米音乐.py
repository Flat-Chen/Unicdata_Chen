import os

import requests
from lxml import etree
import re
import json
import hashlib

cookie = 'xm_sg_tk=9d7a23c4e2e396d69568c0532163738b_1611039889329; xm_sg_tk.sig=4GUo_KTkvzJr2OcRwHKojH7-Hm5vIvcvJUIQHD-Blvg;'
serch = input('输入搜索关键字：')
headers = {
    'cookie': cookie,
}

i = 1
while 1:
    print(f'第{i}页')
    url = 'https://www.xiami.com/list?page=' + str(i) + '&query={"searchKey":"' + serch + '"}&scene=search&type=song'
    response_index = requests.get(url)
    html = etree.HTML(response_index.text)
    trs = html.xpath('//tbody/tr')
    for tr in trs:
        song_name = tr.xpath('.//div[@class="song-name em"]//span/text()')[0]
        song_album = ''.join(tr.xpath('.//div[@class="album"]//span//text()'))
        song_url = 'https://www.xiami.com' + tr.xpath('.//div[@class="song-name em"]/a/@href')[0]
        response = requests.get(song_url)
        song_id = re.findall(r'content="https://www.xiami.com/song/([\s\S]*?)">', response.text)[0]
        s = hashlib.md5((headers['cookie'].split('=')[1].split('_')[0] +
                         '_xmMain_/api/song/getPlayInfo_{"songIds":[' +
                         str(song_id) + ']}').encode('utf-8')).hexdigest().lower()
        song_down_url = 'https://www.xiami.com/api/song/getPlayInfo?_q=%7B%22songIds%22:[{}]%7D&_s={}'.format(song_id,
                                                                                                              s)
        response_down = requests.get(song_down_url, headers=headers)
        json_data = json.loads(response_down.text)
        try:
            song_download = json_data['result']['data']['songPlayInfos'][0]['playInfos'][0]['listenFile'] if \
                json_data['result']['data']['songPlayInfos'][0]['playInfos'][0]['listenFile'] else \
                json_data['result']['data']['songPlayInfos'][0]['playInfos'][1]['listenFile']
            dirs = './music'
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            f = open(r"./music/{}.mp3".format((song_name + '-' + song_album).replace('\\', '')), "wb+")
            f.write(requests.get(song_download).content)
            f.close()
            print(song_name, song_album, '下载完成')
        except Exception as e:
            if 'No schema supplied' in str(e):
                print(song_name, song_album, '虾米没有版权 没有下载地址')
            else:
                print(e)
            continue
    if 'true' in html.xpath('//li[@title="下一页"]/@aria-disabled')[0]:
        print(f'一共{i}页都爬取完成 结束')
        break
    i += 1
