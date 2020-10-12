# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Tc58Item(scrapy.Item):
    brand_id = scrapy.Field()
    brandname = scrapy.Field()
    country = scrapy.Field()
    familyname = scrapy.Field()
    family_id = scrapy.Field()
    vehicle = scrapy.Field()
    vehicle_id = scrapy.Field()
    year = scrapy.Field()
    guide_price = scrapy.Field()
    grabtime = scrapy.Field()
    url = scrapy.Field()
    order = scrapy.Field
    status = scrapy.Field()

    regDate = scrapy.Field()
    mile = scrapy.Field()
    city = scrapy.Field()
    low_price = scrapy.Field()
    high_price = scrapy.Field()
