# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AutohomeItem(scrapy.Item):
    typeid = scrapy.Field()
    typerank = scrapy.Field()
    price = scrapy.Field()
    fcttypeid = scrapy.Field()
    fcttype = scrapy.Field()
    levelid = scrapy.Field()
    cityid = scrapy.Field()
    provinceid = scrapy.Field()
    seriesname = scrapy.Field()
    seriesid = scrapy.Field()
    Sort = scrapy.Field()
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    rank = scrapy.Field()


class A1688Item(scrapy.Item):
    company = scrapy.Field()
    level = scrapy.Field()
    on_sale = scrapy.Field()
    major_businesses = scrapy.Field()
    city = scrapy.Field()
    region = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
