# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pathlib
import time

import pymongo
import logging

import redis
from pybloom_live import ScalableBloomFilter

from hashlib import md5
import os

from scrapy import signals
from scrapy.exceptions import DropItem


# from scrapy.utils.project import get_project_settings
# settings = get_project_settings()


class CarbuisnessNewPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        # mongo
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = self.connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.collectionurllog = db[settings['MONGODB_COLLECTION'] + "_urllog"]
        # bloom file
        self.mongocounts = 0
        self.counts = 0
        self.CrawlCar_Num = 1000000
        self.settings = settings
        # bloom file
        filename = str(pathlib.Path.cwd()) + '/blm/' + settings['MYSQL_DB'] + '/' + settings['MYSQL_TABLE'] + '.blm'
        dirname = str(pathlib.Path.cwd()) + '/blm/' + settings['MYSQL_DB']

        self.df = ScalableBloomFilter(initial_capacity=self.CrawlCar_Num, error_rate=0.01)
        # # read
        if os.path.exists(dirname):
            if os.path.exists(filename):
                self.fa = open(filename, "a")
            else:
                pathlib.Path(filename).touch()
                self.fa = open(filename, "a")
        else:
            os.makedirs(dirname)
            pathlib.Path(filename).touch()
            self.fa = open(filename, "a")

        with open(filename, "r") as fr:
            lines = fr.readlines()
            for line in lines:
                line = line.strip('\n')
                self.df.add(line)
        self.counts = 0

    def process_item(self, item, spider):
        if spider.name in ["autohome_error_new", "jzg_price_master", ]:
            # if item["newcar_bug_num"] is not None or item["oldcar_bug_num"] is not None or item["oldcar_bug_ratio"] is not None or item["newcar_bug_ratio"] is not None:
            self.collection.insert(dict(item))
            logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
            self.counts += 1
            logging.log(msg="scrapy                    " + str(self.counts) + "                  items",
                        level=logging.INFO)
        else:
            if spider.name in ['all_location', 'jzg_price', 'jzg_price_sh', 'xiaozhu_modellist', 'xiaozhu_gz',
                               'autohome_gz', 'jzg_modellist']:
                # print("*"*100)
                valid = True
                i = md5(item['status'].encode("utf8")).hexdigest()
                returndf = self.df.add(i)
                if returndf:
                    valid = False
                    raise DropItem("Drop data {0}!".format(item["status"]))
                else:
                    pass
                if valid:
                    self.fa.writelines(i + '\n')
                    self.collection.insert(dict(item))
                    logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
                    self.counts += 1
                    logging.log(msg="scrapy                    " + str(self.counts) + "                  items",
                                level=logging.INFO)
            if spider.name in ['autohome_url']:
                pass

    def close_spider(self, spider):
        self.connection.close()
        self.fa.close()


class MasterPipeline(object):
    def __init__(self):
        self.redis_url = 'redis://192.168.1.241:6379/15'
        self.r = redis.Redis.from_url(self.redis_url, decode_responses=True)

    def process_item(self, item, spider):
        self.r.lpush('autohome_gz:start_urls', item['url'])


# 爬虫开始和结束时候的重命名表
class RenameTable(object):
    # 爬虫开始和结束时的操作
    def __init__(self):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        self = cls()
        crawler.signals.connect(self.begin, signal=signals.spider_opened)  # 绑定信号发生时允许的函数
        crawler.signals.connect(self.closed, signal=signals.spider_closed)
        return self

    # 爬虫开始执行此函数
    def begin(self, spider):
        # 更改表名字-开始
        local_time = time.strftime('%Y-%m-%d', time.localtime())
        connection1 = pymongo.MongoClient('192.168.2.149', 27017)
        db1 = connection1['xiaozhu']
        collection1 = db1['xiaozhu_gz']
        count = collection1.count()
        if count:
            print(count)
            name = 'xiaozhu_gz_' + str(local_time)
            collection1.rename(name)

    # 爬虫结束，执行此函数
    def closed(self, spider):
        # 更改表名字-结束
        local_time = time.strftime('%Y-%m-%d', time.localtime())
        connection2 = pymongo.MongoClient('192.168.2.149', 27017)
        db2 = connection2['xiaozhu']
        collection2 = db2['xiaozhu_gz_update']
        count = collection2.count()
        if count:
            print(count)
            name = 'xiaozhu_gz'
            collection2.rename(name)
