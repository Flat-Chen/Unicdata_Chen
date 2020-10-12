import json
import time

import pymysql
import scrapy


class Che168AttentionSpider(scrapy.Spider):
    name = 'che168_attention'
    allowed_domains = ['che168.com']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(Che168AttentionSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'usedcar_update',
        'MYSQL_TABLE': 'che168_online',
        'WEBSITE': 'che168_attention',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'Attention',
        'MONGODB_COLLECTION': 'che168',
        'CONCURRENT_REQUESTS': 32,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'ITEM_PIPELINES': {
            'che168.pipelines.GuaziPipeline': 300,
        },
    }

    def start_requests(self):
        coon = pymysql.connect(
            host='192.168.1.94',
            user='dataUser94',
            password='94dataUser@2020',
            database='newcar_test',
            charset='utf8'
        )
        cursor = coon.cursor()
        sql = '''
        SELECT familyid
        FROM autohomeall
        '''
        cursor.execute(sql)
        countAll = cursor.fetchall()
        brand_list = []
        for count in countAll:
            brand_list.append(count[0])
        #     去重
        family_list = list(set(brand_list))
        for familyid in family_list:
            url = f'https://carif.api.autohome.com.cn/Attention/LoadAttentionData.ashx?seriesids={familyid}'
            yield scrapy.Request(url=url)

    def parse(self, response):
        item = dict()
        json_data = json.loads(response.text)
        for data in json_data['result']:
            seriesid = data['seriesid']
            for specattentions in data['specattentions']:
                specid = specattentions['specid']
                attention = specattentions['attention']
                specstate = specattentions['specstate']
                print(specid, attention, specstate, seriesid)
                item['specid'] = specid
                item['attention'] = attention
                item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['seriesid'] = seriesid
                item['url'] = response.url
                item['specstate'] = specstate
                yield item
