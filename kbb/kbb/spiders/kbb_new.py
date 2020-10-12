import scrapy
import time


# 修改了过滤规则
website = 'kbb_new'


class KoubeiSpider(scrapy.Spider):
    name = website

    allowed_domains = ['kbb.com']

    # start_urls = ['https://www.kbb.com/cars-for-sale/cars/used-cars/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)

        self.carnum = 1000000

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'koubei_new',
        'MONGODB_COLLECTION': 'kbb_new',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        for i in range(60):
            url = f'https://www.kbb.com/cars-for-sale/used?listingTypes=USED&searchRadius=0&marketExtension=include&isNewSearch=false&sortBy=derivedpriceDESC&numRecords=25&firstRecord={i * 25}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if '0 Results' in response.text:
            pass
        else:
            cars_url = response.xpath('//div[@class="display-flex justify-content-between"]/a/@href').extract()
            for car_url in cars_url:
                car_url = 'https://www.kbb.com' + car_url
                yield scrapy.Request(url=car_url, callback=self.parse_car)

    def parse_car(self, response):
        item = {}

        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['title'] = response.xpath("//h1/text()").extract_first().strip()
        item['price'] = response.xpath(
            '//div[@class="panel-body"]//span[@class="first-price"]/text()').extract_first().strip()
        lis = response.xpath('//li[@class="list-bordered list-condensed"]')
        value_list = []
        for li in lis:
            value = li.xpath('.//div[@class="col-xs-8"]/text()').extract_first()
            if value == None:
                value = ''
            value_list.append(value)

        item['MILEAGE'] = value_list[0]
        item['DRIVE_TYPE'] = value_list[1]
        item['ENGINE'] = value_list[2]
        item['TRANSMISSION'] = value_list[3]
        item['FUEL_TYPE'] = value_list[4]
        item['EXTERIOR'] = value_list[5]
        item['INTERIOR'] = value_list[6]
        item['VIN'] = value_list[7]
        item['MPG'] = value_list[8]

        item['url'] = response.url
        item['status'] = response.url + '-' + item['price']
        yield item
