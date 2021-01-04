# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

import pandas as pd
import pymongo
import logging
import redis
import requests
from pybloom_live import ScalableBloomFilter
from hashlib import md5
import pathlib
import os
import time
from sqlalchemy import create_engine
from scrapy import signals
from scrapy.exceptions import DropItem


class Che300XcxPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        # mysql
        self.conn = create_engine(
            f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8')

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
        if spider.name in ["che300_car", ""]:
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
        elif spider.name in ["che300_gz", "che300_modelinfo", 'che300_price_daily']:
            self.collection.insert(dict(item))
            logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
            self.counts += 1
            logging.log(msg="scrapy                    " + str(self.counts) + "                  items",
                        level=logging.INFO)
            return item
        # mysql有要去重字段status的爬虫名字写进去
        elif spider.name in ['', ' ']:
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
        elif spider.name in ['baidu', '']:
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


def dingmessage(tex):
    # 请求的URL，WebHook地址
    # log通知群
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=19bfd85d8430457c13e778f5cc7d3ff2686914288b5b2464ce353e088206a655"
    # 测试地址
    # webhook = 'https://oapi.dingtalk.com/robot/send?access_token=633758ccd22b7db4d2e9655488af7d3f5d5e0b2a32c701c80fc3cd57981e73a9'
    # 构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    # 构建请求数据
    message = {
        "msgtype": "text",
        "text": {
            "content": tex
        },
        "at": {
            "isAtAll": False
        }
    }
    # 对请求的数据进行json封装
    message_json = json.dumps(message)
    # 发送请求
    info = requests.post(url=webhook, data=message_json, headers=header)
    # 打印返回的结果
    print(info.text)


# 爬虫开始和结束时候的重命名表 只写了mongo的 存储表名要以_update结尾
class RenameTable(object):
    # 爬虫开始和结束时的操作
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        self = cls(crawler.settings)
        crawler.signals.connect(self.begin, signal=signals.spider_opened)  # 绑定信号发生时允许的函数
        crawler.signals.connect(self.closed, signal=signals.spider_closed)
        return self

    # 爬虫开始执行此函数
    def begin(self, spider):
        # 更改表名字-开始
        local_time = time.strftime('%Y-%m-%d', time.localtime())
        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dingmessage('-{} 爬虫已启动-\n-{}-'.format(spider.name, times))
        connection1 = pymongo.MongoClient(self.settings['MONGODB_SERVER'], self.settings['MONGODB_PORT'])
        db1 = connection1[self.settings['MONGODB_DB']]
        try:
            collection1 = db1[self.settings['MONGODB_COLLECTION'].strip('_update')]
            count = collection1.count()
            if count:
                print(count)
                name = self.settings['MONGODB_COLLECTION'].strip('_update') + '_' + str(local_time)
                collection1.rename(name)
        except:
            pass

    # 爬虫结束，执行此函数
    def closed(self, spider):
        # 更改表名字-结束
        local_time = time.strftime('%Y-%m-%d', time.localtime())
        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        connection2 = pymongo.MongoClient(self.settings['MONGODB_SERVER'], self.settings['MONGODB_PORT'])
        db2 = connection2[self.settings['MONGODB_DB']]
        collection2 = db2[self.settings['MONGODB_COLLECTION']]
        count = collection2.count()
        if count:
            print(count)
            name = self.settings['MONGODB_COLLECTION'].strip('_update')
            collection2.rename(name)
        dingmessage('-{} 爬虫已运行结束-\n-共抓取{}条数据-\n-存储位置mongo-{}-{}-{}-\n-{}-'.
                    format(spider.name, count, self.settings['MONGODB_SERVER'], self.settings['MONGODB_DB'],
                           self.settings['MONGODB_COLLECTION'].strip('_update'), times))


# 推URL到redis里面 分布式爬虫
class MasterPipeline(object):
    def __init__(self):
        self.redis_url = 'redis://192.168.2.149:6379/2'
        self.r = redis.Redis.from_url(self.redis_url, decode_responses=True)

    def process_item(self, item, spider):
        self.r.lpush('dasouche_gz_4city:start_urls', item['url'])
