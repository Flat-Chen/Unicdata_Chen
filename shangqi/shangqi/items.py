# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShangqiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LuntanItem(scrapy.Item):
    # define the fields for your item here like:
    grabtime = scrapy.Field()  # 抓取时间
    parsetime = scrapy.Field()  # 解析时间
    content = scrapy.Field()
    url = scrapy.Field()
    user_name = scrapy.Field()
    posted_time = scrapy.Field()
    user_car = scrapy.Field()
    province = scrapy.Field()
    region = scrapy.Field()
    click_num = scrapy.Field()
    reply_num = scrapy.Field()
    title = scrapy.Field()
    content_num = scrapy.Field()
    md5 = scrapy.Field()
    statusplus = scrapy.Field()
    information_source = scrapy.Field()
    brand = scrapy.Field()

