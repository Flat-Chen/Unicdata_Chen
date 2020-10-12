import json
import time

import scrapy


class AutohomeRankGuanzhuSpider(scrapy.Spider):
    name = 'autohome_rank_guanzhu'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['http://autohome.com.cn/']

    def start_requests(self):
        pageindex = '1'
        pm = '2'
        typeid = '2'
        prices = ['', '0', '0-5', '5-8', '8-10', '10-15', '15-20', '20-25', '25-35', '35-50', '50-100', '100-5000']
        fcttypeids = ['0', '1', '2', '3']
        levelids = ['0', '1,2,3,4,5,6', '1', '2', '3', '4', '5', '6', '16,17,18,19,20', '16', '17', '18', '19', '20',
                    '201908', '7', '8', '11', '12', '13', '99']
        cityid = '0'
        provinceid = '0'
        for price in prices:
            for fcttypeid in fcttypeids:
                for levelid in levelids:
                    url = f'https://cars.app.autohome.com.cn/cars_v9.1.0/cars/getseriesranklist.ashx?pageindex={pageindex}&pm={pm}&pluginversion=10.3.0&typeid={typeid}&price={price}&fcttypeid={fcttypeid}&levelid={levelid}&cityid={cityid}&provinceid={provinceid}'
                    yield scrapy.Request(url=url, callback=self.parse,
                                         meta={"info": (pm, typeid, price, fcttypeid, levelid, cityid, provinceid)}, )

    def parse(self, response):
        item = {}
        pm, typeid, price, fcttypeid, levelid, cityid, provinceid = response.meta.get('info')
        typerank = str('')
        fcttype = str('')
        if typeid == '1':
            typerank = '销量榜'
        elif typeid == '2':
            typerank = '关注榜'
        elif typeid == '3':
            typerank = '降价榜'
        elif typeid == '4':
            typerank = '口碑榜'

        if fcttypeid == '0':
            fcttype = '不限厂商'
        elif fcttypeid == '1':
            fcttype = '国产'
        elif fcttypeid == '2':
            fcttype = '合资'
        elif fcttypeid == '3':
            fcttype = '进口'
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        for i in json_data['result']['list']:
            item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['typeid'] = typeid
            item['typerank'] = typerank
            item['pm'] = pm
            item['price'] = price
            item['fcttypeid'] = fcttypeid
            item['fcttype'] = fcttype
            item['rank'] = i['lefttitle']
            item['levelid'] = levelid
            item['seriesname'] = i['seriesname']
            item['seriesid'] = i['seriesid']
            item['Sort'] = i['Sort']
            item['url'] = response.url
            item['status'] = response.url + '-' + i['seriesimage']
            yield item
