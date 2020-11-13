import time
import scrapy
import json


class AutohomeDealerSpider(scrapy.Spider):
    name = 'autohome_dealer'
    allowed_domains = ['autohome.com.cn']
    start_urls = [
        'https://dealer.autohome.com.cn/DealerList/GetAreasAjax?provinceId=0&cityId=340100&brandid=0&manufactoryid=0&seriesid=0&isSales=0']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeDealerSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': "192.168.1.94",
        'MYSQL_USER': "dataUser94",
        'MYSQL_PWD': "94dataUser@2020",
        'MYSQL_PORT': 3306,
        'MYSQL_DB': "autohome",
        'MYSQL_TABLE': "autohome_dealer",
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'network',
        'MONGODB_COLLECTION': 'autohome_dealer',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def parse(self, response):
        json_data = json.loads(response.text)
        AreaInfoGroups = json_data['AreaInfoGroups']
        for Values in AreaInfoGroups:
            for provinces in Values['Values']:
                procince = provinces['Name']
                for citys in provinces['Cities']:
                    city_id = citys['Id']
                    city_count = citys['Count']
                    city = citys['Name']
                    city_pinyin = citys['Pinyin']
                    for i in range(1, int(city_count / 15) + 2):
                        url = f'https://dealer.autohome.com.cn/{city_pinyin}/0/0/0/0/{i}/1/0/0.html'
                        yield scrapy.Request(url=url, callback=self.parse_dealer,
                                             meta={'info': (procince, city, city_pinyin, city_id, city_count)})

    def parse_dealer(self, response):
        item = {}
        procince, city, city_pinyin, city_id, city_count = response.meta.get('info')
        # print(procince, city, city_pinyin, city_id, city_count)
        lis = response.xpath('//li[@class="list-item"]')
        for li in lis:
            shopname = li.xpath('.//li[@class="tit-row"]/a/span/text()').extract_first()
            try:
                shop_url = 'https' + li.xpath('.//li[@class="tit-row"]/a/@href').extract_first()
            except:
                shop_url = None
            shop_id = li.xpath('./@id').extract_first()
            shop_type = li.xpath('.//li[@class="tit-row"]/span[1]/text()').extract_first()
            mainbrand = li.xpath('.//ul[@class="info-wrap"]/li[2]/span/em/text()').extract_first()
            sell_online = li.xpath('.//a[@class="link link-spacing"]/text()').extract_first()
            tel = li.xpath('.//span[@class="tel"]/text()').extract_first()
            business_hours = li.xpath('.//span[@class="gray"]/text()').extract_first()
            sales_regions = '-'.join(li.xpath('.//span[@class="sale-whole"]//text()').extract()) \
                .replace(' ', '').replace('\n', '').replace('\r', '')
            location = li.xpath('.//span[@class="info-addr"]/text()').extract_first()
            promotion = li.xpath('.//li[5]/a[@class="link"]/text()').extract_first()
            # print(shopname, shop_id, shop_type, mainbrand, sell_online, tel, business_hours, sales_regions, location,promotion)
            item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['procince'] = procince
            item['city'] = city
            item['shopname'] = shopname
            item['shop_id'] = shop_id
            item['shoptype'] = shop_type
            item['mainbrand'] = mainbrand
            item['sell_online'] = sell_online
            item['tel'] = tel
            item['business_hours'] = business_hours
            item['salesregions'] = sales_regions
            item['location'] = location
            item['promotion'] = promotion
            item['url'] = shop_url
            item['status'] = city + shopname + str(shop_id) + location + str(tel)
            # print(item)
            yield item
