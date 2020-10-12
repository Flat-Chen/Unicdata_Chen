# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YicheItem(scrapy.Item):
    grab_time = scrapy.Field()
    brand_id = scrapy.Field()
    brand = scrapy.Field()
    family_id = scrapy.Field()
    familyname = scrapy.Field()
    vehicle_id = scrapy.Field()
    vehicle = scrapy.Field()
    makeyear = scrapy.Field()
    guide_price = scrapy.Field()
    power_type = scrapy.Field()
    engine = scrapy.Field()
    gearbox = scrapy.Field()
    environmental_standards = scrapy.Field()
    number_of_seats = scrapy.Field()
    displacement = scrapy.Field()
    drive_way = scrapy.Field()
    maximum_cruising_range = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
