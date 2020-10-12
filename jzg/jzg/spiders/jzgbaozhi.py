# -*- coding: utf-8 -*-
import json
import time

import scrapy


class JzgbaozhiSpider(scrapy.Spider):
    name = 'jzgbaozhi'
    allowed_domains = ['jingzhengu.com']

    # start_urls = ['https://news.jingzhengu.com/toolpage/baozhi.html']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(JzgbaozhiSpider, self).__init__(**kwargs)
        self.counts = 0
        self.item_counts = 0
        self.city_list = ['201', '2401', '501', '2501']  # 北京、上海、广州、成都

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'jzg',
        'MYSQL_TABLE': 'jzg_baozhi',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'jzg',
        'MONGODB_COLLECTION': 'jzg_baozhi',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        for city in self.city_list:
            for pageIndex in range(1, 500):
                url = f'https://news.jingzhengu.com/toolpage/getBZLRank?pageIndex={pageIndex}&pageSize=6&modelLevel=0&cityId={city}'
                yield scrapy.Request(url=url, meta={'info': (city, pageIndex)})

    def parse(self, response):
        city, pageIndex = response.meta.get('info')
        data = response.text
        json_data = json.loads(data)
        if json_data['list'] == []:
            # print(f'第{pageIndex}页已经没有数据了！！！')
            pass
        else:
            for data_list in json_data['list']:
                item = {}
                makeId = data_list['makeId']
                makeName = data_list['makeName']
                modelId = data_list['modelId']
                modelName = data_list['modelName']
                rank = data_list['rank']
                year_1 = data_list['detailList'][0]['residualRatio']
                year_2 = data_list['detailList'][1]['residualRatio']
                year_3 = data_list['appraiseRankingChildVo3']['residualRatio']
                year_4 = data_list['detailList'][3]['residualRatio']
                year_5 = data_list['detailList'][4]['residualRatio']
                recCount = data_list['recCount']
                lowPrice = data_list['lowPrice']
                upPrice = data_list['upPrice']
                item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                if city == '201':
                    item['city'] = '北京'
                elif city == '2401':
                    item['city'] = '上海'
                elif city == '501':
                    item['city'] = '广州'
                elif city == '2501':
                    item['city'] = '成都'
                item['rank'] = rank
                item['brandname'] = makeName
                item['brand_id'] = makeId
                item['familyname'] = modelName
                item['family_id'] = modelId
                item['year1'] = year_1
                item['year2'] = year_2
                item['year3'] = year_3
                item['year4'] = year_4
                item['year5'] = year_5
                item['recCount'] = recCount
                item['lowPrice'] = lowPrice
                item['upPrice'] = upPrice
                item['url'] = response.url
                item['status'] = response.url + '-' + time.strftime("%Y-%m-%d", time.localtime()) + '-' + str(modelId)
                print(item)
                yield item
                self.item_counts = self.item_counts + 1
        print(self.item_counts)
