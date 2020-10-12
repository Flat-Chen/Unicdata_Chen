# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import os

import pandas as pd
from sqlalchemy import create_engine
import pymysql
from pybloom_live import ScalableBloomFilter
from hashlib import md5
from scrapy.exceptions import DropItem
import pymongo
import pathlib


class LuntanPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        # mysql
        self.conn = create_engine(
            f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8')
        # mongo
        # self.connection = pymongo.MongoClient(
        #     settings['MONGODB_SERVER'],
        #     settings['MONGODB_PORT']
        # )
        # self.db = self.connection[settings['MONGODB_DB']]

        # count
        self.mongocounts = 0
        self.dropcounts = 0

        # mongo
        # self.collection = self.db[settings['MONGODB_COLLECTION']]
        # print(settings['MONGODB_COLLECTION'])
        # print("*"*100)
        # bloomfilter
        # num = (int(settings['CRAWL_NUM']) + self.collection.count()) * 1.5
        self.settings = settings

        self.CrawlCar_Num = 1000000
        self.settings = settings
        # bloom file
        filename = str(pathlib.Path.cwd()) + '/blm/' + settings['MYSQL_DB'] + '/' + settings['MYSQL_TABLE'] + '.blm'
        dirname = str(pathlib.Path.cwd()) + '/blm/' + settings['MYSQL_DB']
        # pybloom
        self.df = ScalableBloomFilter(initial_capacity=self.CrawlCar_Num, error_rate=0.01)
        # self.df = BloomFilter(capacity=self.CrawlCar_Num, error_rate=0.01)
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

    def process_item(self, item, spider):
        if spider.name in ['xcar_luntan', 'pcauto_luntan', 'autohome_luntan', 'yiche_luntan', 'lyh',
                           'pcauto_luntan_new']:
            valid = True
            i = md5(item['statusplus'].encode("utf8")).hexdigest()
            returndf = self.df.add(i)
            # if returndf or '一汽' in item["brand"]:
            if returndf:
                valid = False
                # raise DropItem("Drop data {0}!".format(item["detail_url"]))
            else:
                pass
            if valid:
                self.fa.flush()
                self.fa.writelines(i + '\n')
                self.mongocounts += 1
                logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)
                # 数据存入mysql
                items = list()
                items.append(item)
                df = pd.DataFrame(items)
                df.to_sql(name=self.settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)
                logging.log(msg=f"add data in mysql", level=logging.INFO)
                # return item

    def close_spider(self, spider):
        self.conn.dispose()
        self.fa.close()

