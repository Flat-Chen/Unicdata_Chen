# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DasoucheItem(scrapy.Item):
    brand_id = scrapy.Field()
    brandname = scrapy.Field()
    country = scrapy.Field()
    familyname = scrapy.Field()
    family_id = scrapy.Field()
    factory = scrapy.Field()
    level = scrapy.Field()
    vehicle = scrapy.Field()
    vehicle_id = scrapy.Field()
    year = scrapy.Field()
    guidePrice = scrapy.Field()
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()

    redDate = scrapy.Field()
    mile = scrapy.Field()
    city = scrapy.Field()
    normal = scrapy.Field()
    good = scrapy.Field()
    excellent = scrapy.Field()
    future_price = scrapy.Field()
