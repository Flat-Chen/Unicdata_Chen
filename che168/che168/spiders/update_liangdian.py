# -*- coding: utf-8 -*-
import pymysql
import scrapy
import re
import json

coon = pymysql.connect(
    host='192.168.1.94',
    user='dataUser94',
    password='94dataUser@2020',
    database='usedcar_update',
    charset='utf8'
)
cursor = coon.cursor()
sql = '''
SELECT id,carid,url
FROM che168_online
WHERE contact_company = '等待另外一个爬虫更新' OR contact_company LIKE '%店%'
'''
cursor.execute(sql)
countAll = cursor.fetchall()
# print('一共有' + str(len(countAll)) + '条数据要更新')


# print(countAll)


class UpdateLiangdianSpider(scrapy.Spider):
    name = 'update_liangdian'
    allowed_domains = ['che168.com']

    # start_urls = ['http://che168.com/']

    def __init__(self, **kwargs):
        super(UpdateLiangdianSpider, self).__init__(**kwargs)
        self.counts = 0
        self.counts_None = 0

    def start_requests(self):
        for id, carid, url in countAll:
            updatae_url = f'https://www.che168.com/Handler/CarInfo/GetOptionConfig.ashx?v=20190815222&infoid={carid}'
            yield scrapy.Request(url=updatae_url, meta={'info': (id, carid, url)})

    def parse(self, response):
        id, carid, url = response.meta.get('info')
        if 'div' in response.text:
            data = ','.join(set(re.findall(r'<p>(.*?)</p>', response.text))).replace('查看全部', '').replace(',,', ',')
            data = re.sub(r'^,', '', data)
            liangdian = '{"liangdian":"' + data + '"}'
        else:
            liangdian = '{"liangdian": "null"}'
        # liangdian = json.dumps(liangdian)
        sql_upd = 'update che168_online set contact_company =%s where id =%s'

        cursor.execute(sql_upd, (liangdian, id))
        coon.commit()
        self.counts = self.counts + 1
        print(f'已经更新了{self.counts}条数据')
        print(id, carid, liangdian, url)
