# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HuaxiaItem(scrapy.Item):
    grab_time = scrapy.Field()
    brandname = scrapy.Field()
    brand_id = scrapy.Field()
    factoryname = scrapy.Field()
    family_id = scrapy.Field()
    familyname = scrapy.Field()
    vehicle = scrapy.Field()
    vehicle_id = scrapy.Field()
    years = scrapy.Field()
    displacement = scrapy.Field()
    guideprice = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()

    year = scrapy.Field()
    month = scrapy.Field()
    mile = scrapy.Field()
    city = scrapy.Field()
    purchasing_price = scrapy.Field()
    Individual_transaction_price = scrapy.Field()
    retail_price = scrapy.Field()
    newcar_price = scrapy.Field()
