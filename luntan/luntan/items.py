# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LuntanItem(scrapy.Item):
    grabtime = scrapy.Field()
    posted_time = scrapy.Field()
    brand = scrapy.Field()
    factory = scrapy.Field()
    user_car = scrapy.Field()
    forumID = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    username = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
