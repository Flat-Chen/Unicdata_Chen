# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JzgItem(scrapy.Item):
    grab_time = scrapy.Field()
    city = scrapy.Field()
    ranke = scrapy.Field()
    makeName = scrapy.Field()
    makeId = scrapy.Field()
    modelName = scrapy.Field()
    modelId = scrapy.Field()
    year_1 = scrapy.Field()
    year_2 = scrapy.Field()
    year_3 = scrapy.Field()
    year_4 = scrapy.Field()
    year_5 = scrapy.Field()
    recCount = scrapy.Field()
    lowPrice = scrapy.Field()
    upPrice = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
