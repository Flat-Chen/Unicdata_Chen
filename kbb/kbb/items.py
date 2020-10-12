# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KbbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    grabtime = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    MILEAGE = scrapy.Field()
    DRIVE_TYPE = scrapy.Field()
    ENGINE = scrapy.Field()
    TRANSMISSION = scrapy.Field()
    FUEL_TYPE = scrapy.Field()
    EXTERIOR = scrapy.Field()
    INTERIOR = scrapy.Field()
    VIN = scrapy.Field()
    MPG = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
