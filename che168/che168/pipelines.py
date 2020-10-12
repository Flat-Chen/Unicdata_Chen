# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import pandas as pd
from sqlalchemy import create_engine
from scrapy.exceptions import DropItem
from pybloom_live import ScalableBloomFilter
from hashlib import md5
import pathlib
import os
import time
import json
import re
import pymysql
import scrapy
from scrapy import signals


class UsedcarNewPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        # 获取配置中的时间片个数，默认为12个，1分钟
        idle_number = crawler.settings.getint('IDLE_NUMBER', 6)
        # 实例化扩展对象
        ext = cls(crawler.settings, idle_number, crawler)
        # 将扩展对象连接到信号， 将signals.spider_idle 与 spider_idle() 方法关联起来。
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)
        return ext

    def __init__(self, settings, idle_number, crawler):
        self.engine = create_engine(
            f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8')
        self.table = settings['WEBSITE'] + '_online'

        website = settings["WEBSITE"]
        conn = pymysql.connect("192.168.1.94", "root", "Datauser@2017", 'usedcar_update', port=3306, charset="utf8")
        # conn = pymysql.connect("124.77.191.6", "root", "Datauser@2017", 'usedcar_update', port=9433, charset="utf8")
        cs = conn.cursor()
        if website not in ["1111", ]:
            sql = f'select colname, tag, mainstring, restring, strip from parse_conf_20190527 where website="{website}"'
        else:
            sql = f'select colname, tag, mainstring, restring, strip from parse_conf where website="{website}"'
        cs.execute(sql)
        self.results = cs.fetchall()
        cs.close()
        conn.close()

        # 爬取时间
        self.start_date = time.strftime('%Y-%m-%d %X', time.localtime())
        self.end_date = time.strftime('%Y-%m-%d %X', time.localtime())
        self.scrapy_date = None

        # redis 信号
        self.crawler = crawler
        self.idle_number = idle_number
        self.idle_list = []
        self.idle_count = 0

        self.items = []
        self.CrawlCar_Num = 10000000
        self.mongocounts = 0
        self.settings = settings
        self.add_num = 0
        self.drop_num = 0
        self.log_dict = {
            "projectName": "used-car-scrapy",
            "logProgram": '',
            "logProgramPath": str(pathlib.Path.cwd()),
            "logPath": "/home/logs/usedcar_new",
            "logTime": '',
            "logMessage": "",
            "logServer": "192.168.1.241",
            "logObjectType": "UsedCarPaChong",
            "logObject": {
                "field": '',
                "info": {
                    "dataBaseType": 'mysql',
                    "dataBaseName": '',
                    "tableName": '',
                    "saveStatus": ''
                }
            }
        }
        # bloom file
        filename = str(pathlib.Path.cwd()) + '/blm/' + settings['MYSQL_DB'] + '/' + settings['MYSQL_TABLE'] + '.blm'
        dirname = str(pathlib.Path.cwd()) + '/blm/' + settings['MYSQL_DB']

        self.bf = ScalableBloomFilter(initial_capacity=self.CrawlCar_Num, error_rate=0.01)
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
                self.bf.add(line)

    def process_item(self, item, spider):
        if spider.name in ['ttpai']:
            self.log_dict["logServer"] = "192.168.1.241"
        if spider.name in ['anxinpai']:
            self.log_dict["logServer"] = "192.168.1.249"
        if spider.name in ['car_street']:
            self.log_dict["logServer"] = "192.168.1.248"
        if spider.name in ['taoche']:
            self.log_dict["logServer"] = "192.168.1.92"

        if spider.name in ['youxin', 'anxinpai', 'taoche', 'youxinpai', 'ttpai', 'car_street', 'chezhibao2']:
            valid = True
            try:
                i = md5(item['statusplus'].encode("utf8")).hexdigest()
            except:
                i = md5(item['status'].encode("utf8")).hexdigest()
            returndf = self.bf.add(i)
            self.log_dict["logProgram"] = spider.name
            self.log_dict["logTime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            self.log_dict["logType"] = 'INFO'
            self.log_dict["logMessage"] = "successful"
            self.log_dict["logObject"]["info"]["tableName"] = spider.name + '_online'
            self.log_dict["logObject"]["info"]["dataBaseName"] = "usedcar_update"

            if returndf:
                self.drop_num += 1
                valid = False
                field_list = ["carsource", "grab_time", "price1", "mileage", "post_time", "sold_date", "city",
                              "registerdate"]
                data = dict()
                for field in field_list:
                    data[field] = item[field].replace(' ', '').replace('\r', '').replace('\n',
                                                                                         '') if field in item else None
                data["grab_time"] = time.strftime('%Y-%m-%d %X', time.localtime())
                self.log_dict["logObject"]["field"] = data
                self.log_dict["logObject"]["field"]["carsource"] = item["website"]
                # self.log_dict["logObject"]["info"]["saveStatus"] = "false"
                self.log_dict["logObject"]["info"]["saveStatus"] = "true"
                logging.log(msg=json.dumps(self.log_dict, ensure_ascii=False), level=logging.INFO)
                # raise DropItem("Drop data {0}!".format(item["url"]))
            else:
                pass
            if valid:
                parsed_item = self.parse_text(item)
                self.items.append(parsed_item)
                self.items = self.save_data(self.items, self.settings['MYSQL_TABLE'], 1)

                self.fa.writelines(i + '\n')
                self.mongocounts += 1
                logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)

    def spider_idle(self, spider):
        self.idle_count += 1  # 空闲计数
        self.idle_list.append(time.time())  # 每次触发 spider_idle时，记录下触发时间戳
        idle_list_len = len(self.idle_list)  # 获取当前已经连续触发的次数
        print(self.scrapy_date)
        logging.info(self.scrapy_date)
        # print(idle_list_len)
        # print(self.idle_count)
        # print(self.idle_list[-1] - self.idle_list[-2])
        # 判断 当前触发时间与上次触发时间 之间的间隔是否大于5秒，如果大于5秒，说明redis 中还有key
        if idle_list_len > 2 and not (1 < (self.idle_list[-1] - self.idle_list[-2]) < 6):
            self.idle_list = [self.idle_list[-1]]
            self.idle_count = 1

        elif idle_list_len == self.idle_number + 1:
            # 空跑一分钟后记录结束时间
            self.end_date = time.strftime('%Y-%m-%d %X', time.localtime())
            self.scrapy_date = f'{self.start_date}  -   {self.end_date}'
            self.start_date = time.strftime('%Y-%m-%d %X', time.localtime())
            print(self.scrapy_date)
            print("*" * 100)

        elif idle_list_len > self.idle_number + 12:
            # 空跑一分钟后重置起始时间
            self.start_date = time.strftime('%Y-%m-%d %X', time.localtime())
            self.idle_count = 0

            # 触发n次以后,开始存取数据
            # if spider.name in ['ouyeel_detail', 'ouyeel_jj']:
            #     self.df_end.to_sql(name=self.settings['MONGODB_COLLECTION'] + '_tmp', con=self.conn, if_exists="append", index=False)
            #     logging.log(msg=f"add              {self.mongocounts}             mysql", level=logging.INFO)
            #     self.df_end = pd.DataFrame()
            #     print("*" * 100)
            # # 连续触发的次数达到配置次数后关闭爬虫
            # # 执行关闭爬虫操作
            # self.crawler.engine.close_spider(spider, 'closespider_pagecount')

    def close_spider(self, spider):
        self.save_data(self.items, self.table, 1)
        self.fa.close()

    def save_data(self, items, tablename, savesize=1):
        if len(items) >= savesize:
            try:
                print(items)
                print("*" * 100)
                item = dict(items[0])
                field_list = ["carsource", "grab_time", "price1", "mileage", "post_time", "sold_date", "city",
                              "registerdate"]
                data = dict()
                for field in field_list:
                    data[field] = item[field].replace(' ', '').replace('\r', '').replace('\n',
                                                                                         '') if field in item else None

                data["grab_time"] = time.strftime('%Y-%m-%d %X', time.localtime())
                self.log_dict["logObject"]["field"] = data
                self.log_dict["logObject"]["field"]["carsource"] = item["car_source"]
                # self.log_dict["logObject"]["info"]["saveStatus"] = "true"
                self.log_dict["logObject"]["info"]["saveStatus"] = "false"

                logging.log(msg=json.dumps(self.log_dict, ensure_ascii=False), level=logging.INFO)
                df = pd.DataFrame(items)
                df.to_sql(name=tablename, con=self.engine, if_exists='append', index=False)
                logging.log(msg="add to SQL", level=logging.INFO)
            except Exception as e:
                print(e)
                # print(items)
            items = []
        return items

    def parse_text(self, item):
        parse_item_list = self.parse_conf()
        parsed_item = self.parse_routine(parse_item_list, item)
        return parsed_item

    def parse_conf(self):
        item_list = []
        for row in self.results:
            caritem = dict()
            caritem['colname'] = row[0]
            caritem['tag'] = row[1]
            caritem['mainstring'] = row[2]
            caritem['restring'] = row[3]
            caritem['strip'] = row[4]
            item_list.append(caritem)
        return item_list

    def parse_routine(self, parse_item_list, item):
        caritemcontent = dict()
        for caritem in parse_item_list:
            caritemcontent[caritem['colname']] = self.parse_data(caritem, item)
        return caritemcontent

    def parse_data(self, caritem, item):
        col = caritem['colname']
        tag = caritem['tag']
        mainstring = caritem['mainstring']
        restring = caritem['restring']
        strip = caritem['strip']

        html = scrapy.selector.Selector(text=item["datasave"])
        caritemdata = None

        if tag == "time":
            caritemdata = time.strftime(mainstring, time.localtime())

        elif tag == "item":
            try:
                caritemdata = item[mainstring]
            except KeyError as e:
                print('itemKeyError:', mainstring)
                print(e)

        elif tag == "value":
            caritemdata = mainstring

        elif tag == "xpath":
            try:
                caritemdata = html.xpath(mainstring).extract_first()
            except Exception as e:
                print(str(e))
                print(col, ' xpath: ', mainstring)

        #
        if restring and caritemdata:
            restring = eval("u'%s'" % restring)
            try:
                caritemdata = re.findall(restring, caritemdata)[0]
            except Exception as e:
                print(str(e))
                print(col, ' restring: ', restring, caritemdata)
        # strip
        if strip and caritemdata:
            caritemdata = caritemdata.strip()

        return caritemdata


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

        self.log_dict = {
            "projectName": "used-car-scrapy",
            "logProgram": '',
            "logProgramPath": str(pathlib.Path.cwd()),
            "logPath": "/home/logs/usedcar_new",
            "logTime": '',
            "logMessage": "",
            "logServer": "192.168.1.241",
            "logObjectType": "UsedCarPaChong",
            "logObject": {
                "field": '',
                "info": {
                    "dataBaseType": 'mysql',
                    "dataBaseName": '',
                    "tableName": '',
                    "saveStatus": ''
                }
            }
        }

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
        if spider.name in ['chesupai']:
            self.log_dict["logServer"] = "192.168.1.241"
        if spider.name in ['anxinpai']:
            self.log_dict["logServer"] = "192.168.1.249"
        if spider.name in ['crawl_jingzhengu', 'ganji']:
            self.log_dict["logServer"] = "192.168.1.248"
        if spider.name in ['xiaozhu', 'hry2car']:
            self.log_dict["logServer"] = "192.168.1.92"

        if spider.name in ['ganji', 'crawl_jingzhengu', 'xiaozhu', 'hry2car', 'che168', 'youxin', 'chesupai',
                           'youxin_master', 'auto51']:
            valid = True
            i = md5(item['statusplus'].encode("utf8")).hexdigest()
            returndf = self.df.add(i)

            self.log_dict["logProgram"] = spider.name
            self.log_dict["logTime"] = item["grab_time"]
            self.log_dict["logType"] = 'INFO'
            self.log_dict["logMessage"] = "successful"
            field_list = ["carsource", "grab_time", "price1", "mileage", "post_time", "sold_date", "city",
                          "registerdate"]
            data = dict()
            for field in field_list:
                data[field] = item[field] if field in item else None
            self.log_dict["logObject"]["field"] = data
            self.log_dict["logObject"]["field"]["carsource"] = item["car_source"]
            self.log_dict["logObject"]["info"]["dataBaseName"] = "usedcar_update"
            self.log_dict["logObject"]["info"]["tableName"] = spider.name + '_online'

            if returndf:
                self.drop_num += 1
                valid = False
                # self.log_dict["logObject"]["info"]["saveStatus"] = "false"
                self.log_dict["logObject"]["info"]["saveStatus"] = "true"
                logging.log(msg=json.dumps(self.log_dict, ensure_ascii=False), level=logging.INFO)
                # raise DropItem("Drop data {0}!".format(item["url"]))
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
                    # self.log_dict["logObject"]["info"]["saveStatus"] = "true"
                    self.log_dict["logObject"]["info"]["saveStatus"] = "false"
                    logging.log(msg=json.dumps(self.log_dict, ensure_ascii=False), level=logging.INFO)
                    df.to_sql(name=self.settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)
                    self.mongocounts += 1
                    logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)

    def close_spider(self, spider):
        # self.connection.close()
        logging.log(msg=f"drop              {self.drop_num}              items", level=logging.INFO)
        if spider.name in ['test']:
            self.df_result.to_sql(name=self.settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)
        self.conn.dispose()


class ScrapyRedisPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        # 获取配置中的时间片个数，默认为12个，1分钟
        idle_number = crawler.settings.getint('IDLE_NUMBER', 6)
        # 实例化扩展对象
        ext = cls(crawler.settings, idle_number, crawler)
        # 将扩展对象连接到信号， 将signals.spider_idle 与 spider_idle() 方法关联起来。
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)
        return ext

    def __init__(self, settings, idle_number, crawler):
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

        # 爬取时间
        self.start_date = time.strftime('%Y-%m-%d %X', time.localtime())
        self.end_date = time.strftime('%Y-%m-%d %X', time.localtime())
        self.scrapy_date = None

        # redis 信号
        self.crawler = crawler
        self.idle_number = idle_number
        self.idle_list = []
        self.idle_count = 0

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
        if spider.name in ['che168', 'youxin']:
            valid = True
            i = md5(item['statusplus'].encode("utf8")).hexdigest()
            returndf = self.df.add(i)
            if returndf:
                self.drop_num += 1
                valid = False
                raise DropItem("Drop data {0}!".format(item["statusplus"]))
            else:
                pass
            if valid:
                self.fa.writelines(i + '\n')
                # 数据存入mysql
                items = list()
                items.append(item)
                df = pd.DataFrame(items)
                if spider.name in ['test']:
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

    def spider_idle(self, spider):
        self.idle_count += 1  # 空闲计数
        self.idle_list.append(time.time())  # 每次触发 spider_idle时，记录下触发时间戳
        idle_list_len = len(self.idle_list)  # 获取当前已经连续触发的次数
        print(self.scrapy_date)
        logging.info(self.scrapy_date)
        # print(idle_list_len)
        # print(self.idle_count)
        # print(self.idle_list[-1] - self.idle_list[-2])
        # 判断 当前触发时间与上次触发时间 之间的间隔是否大于5秒，如果大于5秒，说明redis 中还有key
        if idle_list_len > 2 and not (1 < (self.idle_list[-1] - self.idle_list[-2]) < 6):
            self.idle_list = [self.idle_list[-1]]
            self.idle_count = 1

        elif idle_list_len == self.idle_number + 1:
            # 空跑一分钟后记录结束时间
            self.end_date = time.strftime('%Y-%m-%d %X', time.localtime())
            self.scrapy_date = f'{self.start_date}  -   {self.end_date}'
            self.start_date = time.strftime('%Y-%m-%d %X', time.localtime())
            print(self.scrapy_date)
            print("*" * 100)

        elif idle_list_len > self.idle_number + 12:
            # 空跑一分钟后重置起始时间
            self.start_date = time.strftime('%Y-%m-%d %X', time.localtime())
            self.idle_count = 0


class GuaziPipeline(object):
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
        if spider.name in ["guazi_car", "guazi_gz"]:
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
        elif spider.name in ["che168_attention", "yiche_price", "pcauto_price", "58car_price"]:
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
