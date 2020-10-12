# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GuaziItem(scrapy.Item):
    grab_time = scrapy.Field()
    brandname = scrapy.Field()
    brand_id = scrapy.Field()
    familyname = scrapy.Field()
    family_id = scrapy.Field()
    vehicle = scrapy.Field()
    vehicle_id = scrapy.Field()
    years = scrapy.Field()
    transmission = scrapy.Field()
    emission_standard = scrapy.Field()
    seats = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()

    ragDate = scrapy.Field()
    mile = scrapy.Field()
    city = scrapy.Field()

    levelA_dealerLowBuyPrice = scrapy.Field()
    levelA_individualHighSoldPrice = scrapy.Field()
    levelA_individualLowSoldPrice = scrapy.Field()

    levelB_dealerLowBuyPrice = scrapy.Field()
    levelB_individualHighSoldPrice = scrapy.Field()
    levelB_individualLowSoldPrice = scrapy.Field()

    levelC_dealerLowBuyPrice = scrapy.Field()
    levelC_individualHighSoldPrice = scrapy.Field()
    levelC_individualLowSoldPrice = scrapy.Field()


