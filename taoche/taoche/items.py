# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaocheItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    grabtime = scrapy.Field()
    brandname = scrapy.Field()
    brand_id = scrapy.Field()
    familyname = scrapy.Field()
    family_id = scrapy.Field()
    factoryname = scrapy.Field()
    vehicle = scrapy.Field()
    vehicle_id = scrapy.Field()

    makeyear = scrapy.Field()
    carRegDate = scrapy.Field()
    mileage = scrapy.Field()
    city = scrapy.Field()

    salePrice = scrapy.Field()
    normalMinPrice = scrapy.Field()
    normalMaxPrice = scrapy.Field()
    betterMinPrice = scrapy.Field()
    betterMaxPrice = scrapy.Field()
    bestMinPrice = scrapy.Field()
    etterMaxPrice = scrapy.Field()

    url = scrapy.Field()
    status = scrapy.Field()
