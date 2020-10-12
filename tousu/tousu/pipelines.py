# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import os
import pathlib
import re
import time

import pandas as pd
from sqlalchemy import create_engine
import pymysql
from pybloom_live import ScalableBloomFilter, BloomFilter
from hashlib import md5
from scrapy.exceptions import DropItem
import pymongo


class TousuPipeline(object):

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
        website = settings["WEBSITE"]
        self.collection = db[settings['MONGODB_COLLECTION']]
        # bloom file
        self.CrawlCar_Num = 1000000
        filename = str(pathlib.Path.cwd()) + '/blm/' + settings['MONGODB_DB'] + '/' + settings[
            'MONGODB_COLLECTION'] + '.blm'
        dirname = str(pathlib.Path.cwd()) + '/blm/' + settings['MONGODB_DB']
        self.df = ScalableBloomFilter(initial_capacity=self.CrawlCar_Num, error_rate=0.01)
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
        if spider.name in ['a315tousu', 'qctsw', 'tousu315che', 'a12345auto', 'all_brand_qctsw', 'all_brand_315tousu',
                           'czw', 'all_brand_tousu315che']:
            valid = True
            i = md5(item['status'].encode("utf8")).hexdigest()
            returndf = self.df.add(i)
            if returndf:
                valid = False
                raise DropItem("Drop data {0}!".format(item["status"]))
            else:
                self.fa.writelines(i + '\n')
                self.collection.insert(dict(item))
                logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
                self.counts += 1
                logging.log(msg="scrapy                    " + str(self.counts) + "                  items",
                            level=logging.INFO)
                return item
        elif spider.name in ["autohome_price_new", "yiche_price", "pcauto_price", "58car_price"]:
            self.collection.insert(dict(item))
            logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
            self.counts += 1
            logging.log(msg="scrapy                    " + str(self.counts) + "                  items",
                        level=logging.INFO)
        else:
            self.collection.insert(dict(item))
            logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
            self.counts += 1
            logging.log(msg="scrapy                    " + str(self.counts) + "                  items",
                        level=logging.INFO)

    def close_spider(self, spider):
        self.connection.close()

        self.fa.close()
