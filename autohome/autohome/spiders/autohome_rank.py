# -*- coding: utf-8 -*-
from _datetime import datetime
import json
import time

import scrapy

localyears = datetime.now().year
localmonth = datetime.now().month


class AutohomeRankSpider(scrapy.Spider):
    name = 'autohome_rank'
    allowed_domains = ['autohome.com.cn']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeRankSpider, self).__init__(**kwargs)

        self.carnum = 1000000

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'autohome',
        'MONGODB_COLLECTION': f'autohome_rank_{localyears}-{localmonth}',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        yield scrapy.Request(
            url='https://cars.app.autohome.com.cn/cars_v9.1.0/cars/getseriesrankchannel.ashx?pm=2&typeid=0&pluginversion=10.3.0',
            dont_filter=True)

    def parse(self, response):
        data = response.text
        json_data = json.loads(data)
        rank_xiaoliang = json_data['result']['tablist'][0]
        rank_guanzhu = json_data['result']['tablist'][1]

        xiaoliang_dates = rank_xiaoliang['toplist'][0]['list']
        xiaoliang_date_item = dict()
        for xiaoliang_date in xiaoliang_dates:
            key = xiaoliang_date['value']
            value = xiaoliang_date['name']
            xiaoliang_date_item[key] = value
        xiaoliang_date_item[''] = None

        xiaoliang_jiages = rank_xiaoliang['toplist'][1]['list']
        xiaoliang_jiage_item = dict()
        for xiaoliang_jiage in xiaoliang_jiages:
            key = xiaoliang_jiage['value']
            value = xiaoliang_jiage['name']
            xiaoliang_jiage_item[key] = value
        xiaoliang_jiage_item[''] = None

        xiaoliang_changshangs = rank_xiaoliang['toplist'][2]['list']
        xiaoliang_changshang_item = dict()
        for xiaoliang_changshang in xiaoliang_changshangs:
            key = xiaoliang_changshang['value']
            value = xiaoliang_changshang['name']
            xiaoliang_changshang_item[key] = value
        xiaoliang_changshang_item[''] = None

        xiaoliang_bottomlist = rank_xiaoliang['bottomlist']
        xiaoliang_chexing_item = dict()
        for xiaoliang_chexing in xiaoliang_bottomlist:
            if '轿车' in xiaoliang_chexing['name'] or 'SUV' in xiaoliang_chexing['name']:
                cars = xiaoliang_chexing['list']
                for car in cars:
                    key = car['value']
                    value = car['name']
                    xiaoliang_chexing_item[key] = value
            else:
                key = xiaoliang_chexing['value']
                value = xiaoliang_chexing['name']
                xiaoliang_chexing_item[key] = value
        xiaoliang_chexing_item[''] = None

        print(xiaoliang_date_item)
        print(xiaoliang_jiage_item)
        print(xiaoliang_changshang_item)
        print(xiaoliang_chexing_item)
        for date in xiaoliang_date_item:
            for jiage in xiaoliang_jiage_item:
                for changshang in xiaoliang_changshang_item:
                    for chexing in xiaoliang_chexing_item:
                        url = f'https://cars.app.autohome.com.cn/cars_v9.1.0/cars/getseriesranklist.ashx?pageindex=1&pm=2&pluginversion=10.3.0&typeid=1&data={date}&price={jiage}&fcttypeid={changshang}&levelid={chexing}'
                        yield scrapy.Request(url=url, callback=self.last_parse,
                                             meta={'info': (date, jiage, changshang, chexing, xiaoliang_date_item,
                                                            xiaoliang_jiage_item, xiaoliang_changshang_item,
                                                            xiaoliang_chexing_item)}, dont_filter=True)

        guanzhu_jiages = rank_guanzhu['toplist'][0]['list']
        guanzhu_jiage_item = dict()
        for guanzhu_jiage in guanzhu_jiages:
            key = guanzhu_jiage['value']
            value = guanzhu_jiage['name']
            guanzhu_jiage_item[key] = value
        guanzhu_jiage_item[''] = None

        guanzhu_changshangs = rank_guanzhu['toplist'][1]['list']
        guanzhu_changshang_item = dict()
        for guanzhu_changshang in guanzhu_changshangs:
            key = guanzhu_changshang['value']
            value = guanzhu_changshang['name']
            guanzhu_changshang_item[key] = value
        guanzhu_changshang_item[''] = None

        guanzhu_bottomlist = rank_guanzhu['bottomlist']
        guanzhu_chexing_item = dict()
        for guanzhu_chexing in guanzhu_bottomlist:
            if '轿车' in guanzhu_chexing['name'] or 'SUV' in guanzhu_chexing['name']:
                cars = guanzhu_chexing['list']
                for car in cars:
                    key = car['value']
                    value = car['name']
                    guanzhu_chexing_item[key] = value
            else:
                key = guanzhu_chexing['value']
                value = guanzhu_chexing['name']
                guanzhu_chexing_item[key] = value
        guanzhu_chexing_item[''] = None
        print(guanzhu_jiage_item)
        print(guanzhu_changshang_item)
        print(guanzhu_chexing_item)

        rank_item = {'2': '关注榜', '3': '降价榜', '4': '口碑榜'}
        for key_rank in rank_item:
            for key_jiage in guanzhu_jiage_item:
                for key_changshang in guanzhu_changshang_item:
                    for key_chexing in guanzhu_chexing_item:
                        url = f'https://cars.app.autohome.com.cn/cars_v9.1.0/cars/getseriesranklist.ashx?pageindex=1&pm=2&pluginversion=10.3.0&typeid={key_rank}&fcttypeid={key_changshang}&levelid={key_chexing}&price={key_jiage}'
                        yield scrapy.Request(url=url, callback=self.secend_parse,
                                             meta={'info': (key_rank, key_jiage, key_changshang, key_chexing, rank_item,
                                                            guanzhu_jiage_item, guanzhu_changshang_item,
                                                            guanzhu_chexing_item)}, dont_filter=True)

    def secend_parse(self, response):
        key_rank, key_jiage, key_changshang, key_chexing, rank_item, guanzhu_jiage_item, guanzhu_changshang_item, guanzhu_chexing_item = response.meta.get(
            'info')
        item = {}
        item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['rank_name'] = rank_item[key_rank]
        item['price'] = guanzhu_jiage_item[key_jiage]
        item['factory'] = guanzhu_changshang_item[key_changshang]
        item['vehicle'] = guanzhu_chexing_item[key_chexing]
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        for i in json_data['result']['list']:
            item['rank'] = i['lefttitle']
            item['seriesname'] = i['seriesname']
            item['seriesid'] = i['seriesid']
            item['Sort'] = i['Sort']
            item['url'] = response.url
            item['status'] = response.url + '-' + i['seriesimage']
            yield item

    def last_parse(self, response):
        date, jiage, changshang, chexing, xiaoliang_date_item, xiaoliang_jiage_item, xiaoliang_changshang_item, xiaoliang_chexing_item = response.meta.get(
            'info')
        item = {}
        item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['rank_name'] = '销量榜'
        item['rank_date'] = xiaoliang_date_item[date]
        item['price'] = xiaoliang_jiage_item[jiage]
        item['factory'] = xiaoliang_changshang_item[changshang]
        item['vehicle'] = xiaoliang_chexing_item[chexing]
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        for i in json_data['result']['list']:
            item['rank'] = i['lefttitle']
            item['seriesname'] = i['seriesname']
            item['seriesid'] = i['seriesid']
            item['Sort'] = i['Sort']
            item['url'] = response.url
            item['status'] = response.url + '-' + i['seriesimage']
            yield item
