# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pathlib

import pandas as pd
from sqlalchemy import create_engine
import pymongo
import logging

import redis
from pybloom_live import ScalableBloomFilter

from hashlib import md5
import os
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
        if spider.name in ["autohome_error_new", "jzg_price_master"]:
            # if item["newcar_bug_num"] is not None or item["oldcar_bug_num"] is not None or item["oldcar_bug_ratio"] is not None or item["newcar_bug_ratio"] is not None:
            self.collection.insert(dict(item))
            logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
            self.counts += 1
            logging.log(msg="scrapy                    " + str(self.counts) + "                  items",
                        level=logging.INFO)
        else:
            if spider.name in ['all_location', 'jzg_price', 'jzg_price_sh', 'xiaozhu_modellist', 'xiaozhu_gz',
                               'autohome_gz', 'autohome_gz_4city', 'jzg_modellist', 'autohome_error_p',
                               'autohome_rank']:
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
        self.redis_url = 'redis://192.168.2.149:6379/0'
        self.r = redis.Redis.from_url(self.redis_url, decode_responses=True)

    def process_item(self, item, spider):
        self.r.lpush('autohome_gz_4city:start_urls', item['url'])


class GanjiPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        # mysql
        self.conn = create_engine(
            f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8')
        # mongo
        # uri = f'mongodb://{settings["MONGODB_USER"]}:{settings["MONGODB_PWD"]}@{settings["MONGODB_SERVER"]}:{settings["MONGODB_PORT"]}/'
        # self.connection = pymongo.MongoClient(uri)
        # self.connection = pymongo.MongoClient(
        #     settings['MONGODB_SERVER'],
        #     settings['MONGODB_PORT']
        # )
        # db = self.connection[settings['MONGODB_DB']]
        # self.collection = db[settings['MONGODB_COLLECTION']]
        # # count
        self.mongocounts = 0
        self.counts = 0
        self.CrawlCar_Num = 1000000
        self.settings = settings
        self.add_num = 0
        self.drop_num = 0

        # bloom file
        filename = str(pathlib.Path.cwd()) + '/blm/' + settings['MYSQL_DB'] + '/' + settings['MYSQL_TABLE'] + '.blm'
        dirname = str(pathlib.Path.cwd()) + '/blm/' + settings['MYSQL_DB']

        self.df_result = pd.DataFrame()

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

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):

        if spider.name in ['ganji', 'crawl_jingzhengu', 'xiaozhu', 'hry2car', 'che168', 'youxin', 'chesupai',
                           'youxin_master', 'auto51', 'autohome_butie']:
            valid = True
            i = md5(item['status'].encode("utf8")).hexdigest()
            returndf = self.df.add(i)

            field_list = ["carsource", "grab_time", "price1", "mileage", "post_time", "sold_date", "city",
                          "registerdate"]
            data = dict()
            for field in field_list:
                data[field] = item[field] if field in item else None

            if returndf:
                self.drop_num += 1
                valid = False
            else:
                pass
            if valid:
                self.fa.writelines(i + '\n')
                # 数据存入mysql
                items = list()
                items.append(item)
                df = pd.DataFrame(items)
                if spider.name in ['test', ]:
                    self.df_result = pd.concat([self.df_result, df])
                    self.mongocounts += 1
                    logging.log(msg=f"add              {self.mongocounts}              items", level=logging.INFO)
                else:
                    df.to_sql(name=self.settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)
                    self.mongocounts += 1
                    logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)

    def close_spider(self, spider):
        # self.connection.close()
        logging.log(msg=f"drop              {self.drop_num}              items", level=logging.INFO)
        if spider.name in ['test']:
            self.df_result.to_sql(name=self.settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)
        self.conn.dispose()


class LuntanPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        # mysql
        self.conn = create_engine(
            f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8mb4')

        # mongo
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = self.connection[settings['MONGODB_DB']]
        website = settings["WEBSITE"]
        self.collection = db[settings['MONGODB_COLLECTION']]
        # count
        self.mysqlcounts = 0
        self.counts = 0

        self.settings = settings
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
        # mongo要有重字段status的爬虫名字写进去
        if spider.name in ["autohome_dealer", " "]:
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
        # mongo不需要去重的爬虫名字写进去
        elif spider.name in ["autohome_luntan_lost", " "]:
            self.collection.insert(dict(item))
            logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
            self.counts += 1
            logging.log(msg="scrapy                    " + str(self.counts) + "                  items",
                        level=logging.INFO)
            return item
        # mysql有要去重字段status的爬虫名字写进去
        elif spider.name in ['', '']:
            valid = True
            i = md5(item['status'].encode("utf8")).hexdigest()
            returndf = self.df.add(i)
            if returndf:
                valid = False
                raise DropItem("Drop data {0}!".format(item["status"]))
            else:
                self.fa.flush()
                self.fa.writelines(i + '\n')
                self.mysqlcounts += 1
                logging.log(msg=f"scrapy              {self.mysqlcounts}              items", level=logging.INFO)
                # 数据存入mysql
                items = list()
                items.append(item)
                df = pd.DataFrame(items)
                df.to_sql(name=self.settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)
                logging.log(msg=f"add data in mysql", level=logging.INFO)
                return item
        # mysql不需要去重的爬虫名字写进去
        elif spider.name in ['autohome_luntan_20201111', 'autohome_luntan', 'autohome_luntan_video']:
            self.mysqlcounts += 1
            logging.log(msg=f"scrapy              {self.mysqlcounts}              items", level=logging.INFO)
            # 数据存入mysql
            items = list()
            items.append(item)
            df = pd.DataFrame(items)
            df.to_sql(name=self.settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)
            logging.log(msg=f"add data in mysql", level=logging.INFO)
            return item

    def close_spider(self, spider):
        self.connection.close()
        self.fa.close()
