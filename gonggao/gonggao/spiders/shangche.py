# -*- coding: utf-8 -*-
import re
import time

import scrapy


class ShangcheSpider(scrapy.Spider):
    name = 'shangche'
    allowed_domains = ['cn537.com']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(ShangcheSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        # 'MYSQL_SERVER': '192.168.1.94',
        # 'MYSQL_DB': 'chexiu',
        # 'MYSQL_TABLE': 'chexiu',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'gonggao',
        'MONGODB_COLLECTION': 'shangche',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        for i in range(1, 1000):
            url = f'https://www.cn357.com/cvi.php?m=cvNotice&search=n&lot={i}'
            yield scrapy.Request(url=url)

    def parse(self, response):
        if '暂无搜索结果' in response.text:
            pass
        else:
            urls = response.xpath('//ul[@class="searchList uiLinkList"]/li/h3/a/@href').getall()
            for url in urls:
                yield scrapy.Request(url=response.urljoin(url), callback=self.second_parse, dont_filter=True)
            try:
                # 看是否存在下一页
                next_url = response.xpath('//a[@class="nextprev"]/@href').getall()[-1]
                text = response.xpath('//a[@class="nextprev"]/text()').getall()[-1]
                if '下一页' in text:
                    yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse, dont_filter=True)
            except:
                pass

    def second_parse(self, response):
        change_record = response.xpath('//span[@class="itemCur"]/a/text()').extract_first()
        name = response.xpath('//div[@class="gMain"]/h1[@class="itemH1"]//text()').extract_first().strip()
        announcement_model = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[2]/td[2]//text()').extract_first()
        batch = response.xpath('//table[@class="listTable itemTable uiLinkList"]/tr[2]/td[4]//text()').extract_first()
        brand = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[3]/td[2]//text()').extract_first()
        type = response.xpath('//table[@class="listTable itemTable uiLinkList"]/tr[3]/td[4]//text()').extract_first()
        rated_quality = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[4]/td[2]//text()').extract_first()
        car_quality = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[4]/td[4]//text()').extract_first()
        readiness_quality = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[5]/td[2]//text()').extract_first()
        fuel_type = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[5]/td[4]//text()').extract_first()
        emissions_standards = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[6]/td[2]//text()').extract_first()
        axis = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[6]/td[4]//text()').extract_first()
        wheelbase = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[7]/td[2]//text()').extract_first()
        axle_load = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[7]/td[4]//text()').extract_first()
        spring_sheet = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[8]/td[2]//text()').extract_first()
        tires = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[8]/td[4]//text()').extract_first()
        tire_specifications = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[9]/td[2]//text()').extract_first()
        departure_angle = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[9]/td[4]//text()').extract_first()
        overhang = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[10]/td[2]//text()').extract_first()
        front_track = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[10]/td[4]//text()').extract_first()
        rear_track = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[11]/td[2]//text()').extract_first()
        identification = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[11]/td[4]//text()').extract_first()
        vehicle_length = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[12]/td[2]//text()').extract_first()
        vehicle_width = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[12]/td[4]//text()').extract_first()
        vehicle_height = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[13]/td[2]//text()').extract_first()
        cargo_length = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[13]/td[4]//text()').extract_first()
        cargo_width = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[14]/td[2]//text()').extract_first()
        cargo_height = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[14]/td[4]//text()').extract_first()
        maximum_speed = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[15]/td[2]//text()').extract_first()
        rated_capacity = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[15]/td[4]//text()').extract_first()
        cab_ride = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[16]/td[2]//text()').extract_first()
        steering_type = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[16]/td[4]//text()').extract_first()
        totalmass_trailer_quality = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[17]/td[2]//text()').extract_first()
        load_weight_use_factor = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[17]/td[4]//text()').extract_first()
        maximum_loading_mass_saddle_trailer = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[18]/td[2]//text()').extract_first()
        company = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[18]/td[4]//text()').extract_first()
        company_address = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[19]/td[2]//text()').extract_first()
        phone = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[19]/td[4]//text()').extract_first()
        fax = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[20]/td[2]//text()').extract_first()
        postal = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[20]/td[4]//text()').extract_first()
        chassis_1 = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[21]/td[2]//text()').extract_first()
        chassis_2 = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[21]/td[4]//text()').extract_first()
        chassis_3 = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[22]/td[2]//text()').extract_first()
        chassis_4 = response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[22]/td[4]//text()').extract_first()
        engine_model = ','.join(response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[23]/td/table/tr[2]/td[1]//text()').getall())
        engine_anufacturer = ','.join(response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[23]/td/table/tr[2]/td[2]//text()').getall())
        engine_trademark = ','.join(response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[23]/td/table/tr[2]/td[3]//text()').getall())
        engine_displacement = ','.join(response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[23]/td/table/tr[2]/td[4]//text()').getall())
        engine_power = ','.join(response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[23]/td/table/tr[2]/td[5]//text()').getall())
        remark = ''.join(response.xpath(
            '//table[@class="listTable itemTable uiLinkList"]/tr[24]/td[2]//text()').getall()).replace('\n', '') \
            .replace('\r', '').replace(' ', '')
        try:
            identification = re.sub(r'.,', ',', identification)
        except:
            pass
        # print(change_record, name, announcement_model, batch, brand, type, rated_quality, car_quality,
        #       readiness_quality, fuel_type, emissions_standards, axis, wheelbase, axle_load, spring_sheet, tires,
        #       tire_specifications, departure_angle, overhang, front_track, rear_track, identification, vehicle_length,
        #       vehicle_width, vehicle_height, cargo_length, cargo_width, cargo_height, maximum_speed, rated_capacity,
        #       cab_ride, steering_type, totalmass_trailer_quality, load_weight_use_factor,
        #       maximum_loading_mass_saddle_trailer, company, company_address, phone, fax, postal, chassis_1, chassis_2,
        #       chassis_3, chassis_4, engine_model, engine_anufacturer, engine_trademark, engine_displacement,
        #       engine_power, remark, response.url)

        item = {}
        item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['change_record'] = change_record
        item['name'] = name
        item['announcement_model'] = announcement_model
        item['batch'] = batch
        item['brand'] = brand
        item['type'] = type
        item['rated_quality'] = rated_quality
        item['car_quality'] = car_quality
        item['readiness_quality'] = readiness_quality
        item['fuel_type'] = fuel_type
        item['emissions_standards'] = emissions_standards
        item['axis'] = axis
        item['wheelbase'] = wheelbase
        item['axle_load'] = axle_load
        item['spring_sheet'] = spring_sheet
        item['tires'] = tires
        item['tire_specifications'] = tire_specifications
        item['departure_angle'] = departure_angle
        item['overhang'] = overhang
        item['front_track'] = front_track
        item['rear_track'] = rear_track
        item['identification'] = identification
        item['vehicle_length'] = vehicle_length
        item['vehicle_width'] = vehicle_width
        item['vehicle_height'] = vehicle_height
        item['cargo_length'] = cargo_length
        item['cargo_width'] = cargo_width
        item['cargo_height'] = cargo_height
        item['maximum_speed'] = maximum_speed
        item['rated_capacity'] = rated_capacity
        item['cab_ride'] = cab_ride
        item['steering_type'] = steering_type
        item['totalmass_trailer_quality'] = totalmass_trailer_quality
        item['load_weight_use_factor'] = load_weight_use_factor
        item['maximum_loading_mass_saddle_trailer'] = maximum_loading_mass_saddle_trailer
        item['company'] = company
        item['company_address'] = company_address
        item['phone'] = phone
        item['fax'] = fax
        item['postal'] = postal
        item['chassis_1'] = chassis_1
        item['chassis_2'] = chassis_2
        item['chassis_3'] = chassis_3
        item['chassis_4'] = chassis_4
        item['engine_model'] = engine_model
        item['engine_anufacturer'] = engine_anufacturer
        item['engine_trademark'] = engine_trademark
        item['engine_displacement'] = engine_displacement
        item['engine_power'] = engine_power
        item['remark'] = remark
        item['url'] = response.url
        item['status'] = response.url + batch + announcement_model + change_record
        yield item
