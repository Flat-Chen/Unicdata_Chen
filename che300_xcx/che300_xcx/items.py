import scrapy


class Che300XcxItem(scrapy.Item):
    grabtime = scrapy.Field()
    prov = scrapy.Field()
    cityid = scrapy.Field()
    brand = scrapy.Field()
    series = scrapy.Field()
    salesdescid = scrapy.Field()
    regDate = scrapy.Field()
    mile = scrapy.Field()
    city = scrapy.Field()
    price1 = scrapy.Field()
    price2 = scrapy.Field()
    price3 = scrapy.Field()
    price4 = scrapy.Field()
    price5 = scrapy.Field()
    price6 = scrapy.Field()
    price7 = scrapy.Field()
    price8 = scrapy.Field()
    price9 = scrapy.Field()
    price10 = scrapy.Field()
    price11 = scrapy.Field()
    price12 = scrapy.Field()
    price13 = scrapy.Field()
    price14 = scrapy.Field()
    price15 = scrapy.Field()
    price16 = scrapy.Field()
    price17 = scrapy.Field()
    price18 = scrapy.Field()
    price19 = scrapy.Field()
    price20 = scrapy.Field()
    price21 = scrapy.Field()
    url = scrapy.Field()
    group = scrapy.Field()


class Che300CarItem(scrapy.Item):
    grabtime = scrapy.Field()
    brand = scrapy.Field()
    brand_id = scrapy.Field()
    family_name = scrapy.Field()
    family_id = scrapy.Field()
    vehicle_name = scrapy.Field()
    vehicle_id = scrapy.Field()
    price = scrapy.Field()
    vehicle_year = scrapy.Field()
    min_reg_year = scrapy.Field()
    max_reg_year = scrapy.Field()
    status = scrapy.Field()
