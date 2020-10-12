# -*- coding: utf-8 -*-
import re
import scrapy
import time
from scrapy.utils.project import get_project_settings
from scrapy.mail import MailSender
import logging
import json
# 老版 已弃用 新版名称为yiche_car
website = 'yiche_newcar'


class CarSpider(scrapy.Spider):
    name = website
    start_urls = ['http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=chexing']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        settings = get_project_settings()
        super(CarSpider, self).__init__(**kwargs)
        self.mailer = MailSender.from_settings(settings)
        self.carnum = 1000000
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'yiche',
        'MONGODB_COLLECTION': 'yiche_newcar',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    # def start_requests(self):
    #     cars=[]
    #     for i in range(1,self.carnum):
    #         print(i)
    #         url="http://car.bitauto.com/xinyatu/m"+str(i)+"/"
    #         car=scrapy.Request(url,callback=self.parse)
    #         cars.append(car)
    #     return cars

    def parse(self, response):
        tree_list = json.loads(
            response.text.replace("JsonpCallBack(", "").replace("}]}})", "}]}}").replace("{", "{\"").replace(":",
                                                                                                             "\":").replace(
                ",", ",\"").replace("\"\"", "\"").replace(",\"{", ",{").replace("https\"", "https"))

        for c in tree_list["char"]:
            if tree_list["char"][c] == 1:
                for f in tree_list["brand"][c]:
                    brandname = f["name"]
                    brandid = f["id"]
                    meta = {
                        "brandname": brandname,
                        "brandid": brandid
                    }
                    url = "http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=chexing&pagetype=masterbrand&objid=%d" % brandid
                    yield scrapy.Request(url=url, meta=meta, callback=self.parse_family)
                    break
            break

    def parse_family(self, response):
        # print(response.text)
        result = (
            response.text.replace('AI:', 'AI-').replace("JsonpCallBack(", "").replace("}]}})", "}]}}").replace(':',
                                                                                                               '":"').replace(
                '{', '{"').replace(',', '","').replace('http":"', '').replace('https":"', '').replace('}"',
                                                                                                      '"}').replace(
                '"{',
                '{').replace(
                '"[', '[').replace(']"', ']').replace('""', '"').replace('}]', '"}]').replace(']"', ']')

        )
        result = re.sub(r'//(.*?).png', '', result)
        tree_list = json.loads(result)
        for c in tree_list["char"]:
            # print(c, tree_list['char'])
            # print(tree_list['char'][c])
            if tree_list["char"][c] == '1':
                for f in tree_list["brand"][c]:
                    if f["id"] == str(response.meta["brandid"]):
                        factoryname = f["name"]
                        print('         ', factoryname, f)
                        for factory in f["child"]:
                            if "child" in factory:
                                factoryname = factory["name"]
                                for fam in factory["child"]:
                                    print(fam, '      这是fam')
                                    familyname = fam["name"]
                                    meta = {
                                        "factoryname": factoryname,
                                        "familyname": familyname,
                                    }
                                    url = "http://car.bitauto.com%s" % fam["url"]
                                    yield scrapy.Request(url=url, meta=dict(meta, **response.meta),
                                                         callback=self.parse_model)
                            else:
                                familyname = factory["name"]
                                meta = {
                                    "factoryname": factoryname,
                                    "familyname": familyname,
                                }
                                url = "http://car.bitauto.com%s" % factory["url"]
                                yield scrapy.Request(url=url, meta=dict(meta, **response.meta),
                                                     callback=self.parse_model)
                        break

    def get_value(self, td, item, name):
        if td.xpath('following-sibling::td[1]/span/text()'):
            item[name] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
        else:
            temp = []
            divs = td.xpath('following-sibling::td[1]/div/div')
            for div in divs:
                option = div.xpath("div/text()[1]").extract_first().strip()
                temp.append(option)
            item[name] = "|".join(temp)
            return

    def parse_model(self, response):
        model_list = response.xpath("//*[contains(@id, 'car_filter_id')]")
        for model in model_list:
            modelid = model.xpath("td[1]/@id").re("\d+")[0]
            meta = {
                "modelid": modelid
            }
            url = response.urljoin(model.xpath("td[1]/a[1]/@href").extract_first())
            yield scrapy.Request(url=url, meta=dict(meta, **response.meta), callback=self.parse_details)

        stop = response.xpath("//*[@id='pop_nosalelist']")
        if stop:
            print("停售&&&&&&&&&&&&&&&&&&&&&&&")
            for a in stop.xpath("a"):
                url = response.urljoin(a.xpath("@href").extract_first())
                print(url)
                yield scrapy.Request(url=url, meta=response.meta, callback=self.parse_model)

    def parse_details(self, response):
        self.counts += 1
        logging.log(msg="down               " + str(self.counts) + "           items", level=logging.INFO)
        # item = YicheItem()
        item = {}
        item['url'] = response.url
        item["chexing_id"] = re.findall(r"http://car.bitauto.com/(.*?)/m(\d*?)/", item["url"])[0][1]
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + time.strftime('%Y-%m', time.localtime())
        # item['datasave'] = response.xpath('//html').extract_first()
        item['brandname'] = response.meta["brandname"]
        item['brandid'] = response.meta["brandid"]
        item['familyname'] = response.meta["familyname"]
        item['familyid'] = response.xpath('//input[@id="hidSerialID"]/@value').extract_first()

        # item['familyid'] = response.xpath('//div[@class="crumbs-txst() \t"]/a[5]/@href').extract_fir
        #     if response.xpath('//div[@class="crumbs-txt"]/a[5]/@href').extract_first() else "-"
        item['factoryname'] = response.meta["factoryname"]
        item['salesdesc'] = response.xpath('//div[@class="crumbs-txt"]/strong/text()').extract_first() \
            if response.xpath('//div[@class="crumbs-txt"]/strong/text()').extract_first() else "-"
        item['makeyear'] = response.xpath('//div[@class="crumbs-txt"]/strong/text()').re(u"(\d{4})款")[0] \
            if response.xpath('//div[@class="crumbs-txt"]/strong/text()').extract_first() else "-"

        tds = response.xpath('//*[contains(@class, "config-section")]/div[3]/table/tbody/tr/td')
        print(tds)
        for td in tds:
            if td.xpath('span/text()').extract_first() == u"厂商指导价：":
                item['guideprice'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip().replace(
                    u"万", "")
            if td.xpath('span/text()').extract_first() == u"商家报价：":
                item['shangjiabaojia'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"北京参考价：":
                item['beijing_price'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"上市日期：":
                item['market_time'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"车型级别：":
                item['level'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"车身型式：":
                item['body'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"动力类型：":
                item['power_type'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"发动机：":
                item['engine'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"最大功率/最大扭矩：	":
                item['maximum_power_torque'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"变速箱类型：":
                item['gear_type'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"0-100km/h加速时间：":
                item['acceleration_time'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"混合工况油耗：":
                item['hybrid_oil_comsuption'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"最高车速：":
                item['max_speed'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"环保标准：":
                item['environmental_standard'] = td.xpath(
                    'following-sibling::td[1]/span/text()').extract_first().strip()
                # item['color'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"保修政策：":
                item['warranty_policy'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()

        try:
            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[2]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"长：":
                    self.get_value(td, item, "length")
                if td.xpath('span/text()').extract_first() == u"宽：":
                    self.get_value(td, item, "width")
                if td.xpath('span/text()').extract_first() == u"高：":
                    self.get_value(td, item, "height")
                if td.xpath('span/text()').extract_first() == u"轴距：":
                    self.get_value(td, item, "wheelbase")
                if td.xpath('span/text()').extract_first() == u"整备质量：":
                    self.get_value(td, item, "curb_weight")
                if td.xpath('span/text()').extract_first() == u"座位数：":
                    self.get_value(td, item, "seats_num")
                if td.xpath('span/text()').extract_first() == u"行李厢容积：":
                    self.get_value(td, item, "luggage_compartment_volume")
                if td.xpath('span/text()').extract_first() == u"油箱容积：":
                    self.get_value(td, item, "tank_volume")
                if td.xpath('span/text()').extract_first() == u"前轮胎规格：":
                    self.get_value(td, item, "front_tire_specification")
                if td.xpath('span/text()').extract_first() == u"后轮胎规格：":
                    self.get_value(td, item, "rear_tire_specification")
                if td.xpath('span/text()').extract_first() == u"备胎：":
                    self.get_value(td, item, "spare_tire")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[4]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"排气量：":
                    self.get_value(td, item, "displacement")
                if td.xpath('span/text()').extract_first() == u"最大功率：":
                    self.get_value(td, item, "maximum_power")
                if td.xpath('span/text()').extract_first() == u"最大马力：":
                    self.get_value(td, item, "maximum_horsepower")
                if td.xpath('span/text()').extract_first() == u"最大功率转速：":
                    self.get_value(td, item, "maximum_power_speed")
                if td.xpath('span/text()').extract_first() == u"最大扭矩：":
                    self.get_value(td, item, "maximum_torque")
                if td.xpath('span/text()').extract_first() == u"最大扭矩转速：":
                    self.get_value(td, item, "maximum_torque_speed")
                if td.xpath('span/text()').extract_first() == u"缸体形式：":
                    self.get_value(td, item, "gangtixingshi")
                if td.xpath('span/text()').extract_first() == u"气缸数：":
                    self.get_value(td, item, "qigangshu")
                if td.xpath('span/text()').extract_first() == u"进气形式：":
                    self.get_value(td, item, "jinqifangshi")
                if td.xpath('span/text()').extract_first() == u"供油方式：":
                    self.get_value(td, item, "oil_supply_mode")
                if td.xpath('span/text()').extract_first() == u"燃油标号：":
                    self.get_value(td, item, "fuel_labeling")
                if td.xpath('span/text()').extract_first() == u"发动机启停：":
                    self.get_value(td, item, "engine_start_stop")
                if td.xpath('span/text()').extract_first() == u"变速箱类型：":
                    self.get_value(td, item, "gear_type2")
                if td.xpath('span/text()').extract_first() == u"挡位个数：":
                    self.get_value(td, item, "gears_number")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[6]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"驱动方式：":
                    self.get_value(td, item, "driving_mode")
                if td.xpath('span/text()').extract_first() == u"后悬架类型：":
                    self.get_value(td, item, "rear_suspension_type")
                if td.xpath('span/text()').extract_first() == u"可调悬架：":
                    self.get_value(td, item, "adjustable_suspension")
                if td.xpath('span/text()').extract_first() == u"前轮制动器类型：":
                    self.get_value(td, item, "front_wheel_brake_type")
                if td.xpath('span/text()').extract_first() == u"后轮制动器类型：":
                    self.get_value(td, item, "rear_wheel_brake_type")
                if td.xpath('span/text()').extract_first() == u"驻车制动类型：":
                    self.get_value(td, item, "parking_brake_type")
                if td.xpath('span/text()').extract_first() == u"车体结构：":
                    self.get_value(td, item, "body_structure")
                if td.xpath('span/text()').extract_first() == u"限滑差速器/差速锁：":
                    self.get_value(td, item, "differential_gear")
                if td.xpath('span/text()').extract_first() == u"前悬架类型：":
                    self.get_value(td, item, "front_suspension_type")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[8]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"防抱死制动(ABS)：":
                    self.get_value(td, item, "abs")
                if td.xpath('span/text()').extract_first() == u"制动力分配(EBD/CBC等)：":
                    self.get_value(td, item, "braking_force_distribution")
                if td.xpath('span/text()').extract_first() == u"制动辅助(BA/EBA等)：":
                    self.get_value(td, item, "brake_assistant")
                if td.xpath('span/text()').extract_first() == u"牵引力控制(ARS/TCS等)：":
                    self.get_value(td, item, "traction_control")
                if td.xpath('span/text()').extract_first() == u"车身稳定控制(ESP/DSC等)：":
                    self.get_value(td, item, "vehicle_body_stability_control")
                if td.xpath('span/text()').extract_first() == u"主驾驶安全气囊：":
                    self.get_value(td, item, "main_driving_safety_airbag")
                if td.xpath('span/text()').extract_first() == u"副驾驶安全气囊：":
                    self.get_value(td, item, "auxiliary_driving_safety_airbag")
                if td.xpath('span/text()').extract_first() == u"前侧气囊：":
                    self.get_value(td, item, "front_air_bag")
                if td.xpath('span/text()').extract_first() == u"后侧气囊：":
                    self.get_value(td, item, "rear_air_bag")
                if td.xpath('span/text()').extract_first() == u"侧安全气帘：":
                    self.get_value(td, item, "side_safety_air_curtain")
                if td.xpath('span/text()').extract_first() == u"膝部气囊：":
                    self.get_value(td, item, "knee_airbag")
                if td.xpath('span/text()').extract_first() == u"胎压监测：":
                    self.get_value(td, item, "tire_pressure_monitoring")
                if td.xpath('span/text()').extract_first() == u"零胎压续行轮胎：":
                    self.get_value(td, item, "run_flats")
                if td.xpath('span/text()').extract_first() == u"后排儿童座椅接口：":
                    self.get_value(td, item, "rear_child_seat_interface")
                if td.xpath('span/text()').extract_first() == u"安全带气囊：":
                    self.get_value(td, item, "seat_belt_airbag")
                if td.xpath('span/text()').extract_first() == u"后排中央气囊：":
                    self.get_value(td, item, "rear_central_airbag")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[10]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"定速巡航：":
                    self.get_value(td, item, "cruise_control")
                if td.xpath('span/text()').extract_first() == u"车道保持：":
                    self.get_value(td, item, "lane_keeping")
                if td.xpath('span/text()').extract_first() == u"并线辅助：":
                    self.get_value(td, item, "parallel_auxiliary")
                if td.xpath('span/text()').extract_first() == u"碰撞报警/主动刹车：":
                    self.get_value(td, item, "collision_alarm")
                if td.xpath('span/text()').extract_first() == u"疲劳提醒：":
                    self.get_value(td, item, "fatigue_reminding")
                if td.xpath('span/text()').extract_first() == u"自动泊车：":
                    self.get_value(td, item, "zidongboche")
                if td.xpath('span/text()').extract_first() == u"遥控泊车：":
                    self.get_value(td, item, "remote_parking")
                if td.xpath('span/text()').extract_first() == u"自动驾驶辅助：":
                    self.get_value(td, item, "automatic_driving_assistance")
                if td.xpath('span/text()').extract_first() == u"自动驻车：":
                    self.get_value(td, item, "zidongzhuche")
                if td.xpath('span/text()').extract_first() == u"上坡辅助：":
                    self.get_value(td, item, "shangpofuzhu")
                if td.xpath('span/text()').extract_first() == u"陡坡缓降：":
                    self.get_value(td, item, "doupohuanjiang")
                if td.xpath('span/text()').extract_first() == u"夜视系统：":
                    self.get_value(td, item, "yeshixitong")
                if td.xpath('span/text()').extract_first() == u"可变齿比转向：":
                    self.get_value(td, item, "kebianchibizhuanxiang")
                if td.xpath('span/text()').extract_first() == u"前倒车雷达：":
                    self.get_value(td, item, "qiandaocheleida")
                if td.xpath('span/text()').extract_first() == u"后倒车雷达：":
                    self.get_value(td, item, "houdaocheleida")
                if td.xpath('span/text()').extract_first() == u"倒车影像：":
                    self.get_value(td, item, "daocheyingxiang")
                if td.xpath('span/text()').extract_first() == u"驾驶模式选择：":
                    self.get_value(td, item, "jiashimoshixuanze")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[12]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"前大灯：":
                    self.get_value(td, item, "qiandadeng")
                if td.xpath('span/text()').extract_first() == u"LED日间行车灯：":
                    self.get_value(td, item, "ledrijianxingchedeng")
                if td.xpath('span/text()').extract_first() == u"自动大灯：":
                    self.get_value(td, item, "zidongdadeng")
                if td.xpath('span/text()').extract_first() == u"前雾灯：":
                    self.get_value(td, item, "qianwudeng")
                if td.xpath('span/text()').extract_first() == u"大灯功能：":
                    self.get_value(td, item, "dadenggongneng")
                if td.xpath('span/text()').extract_first() == u"天窗类型：":
                    self.get_value(td, item, "tianchuangleixing")
                if td.xpath('span/text()').extract_first() == u"前电动车窗：":
                    self.get_value(td, item, "qiandiandongchechuang")
                if td.xpath('span/text()').extract_first() == u"后电动车窗：":
                    self.get_value(td, item, "houdiandongchechuang")
                if td.xpath('span/text()').extract_first() == u"外后视镜电动调节：":
                    self.get_value(td, item, "waihoushijingdiandongtiaojie")
                if td.xpath('span/text()').extract_first() == u"内后视镜自动防眩目：":
                    self.get_value(td, item, "neihoushijingzidongfangxuanmu")
                if td.xpath('span/text()').extract_first() == u"流媒体后视镜：":
                    self.get_value(td, item, "liumeitihoushijing")
                if td.xpath('span/text()').extract_first() == u"外后视镜自动防眩目：":
                    self.get_value(td, item, "waihoushijingzidongfangxuanmu")
                if td.xpath('span/text()').extract_first() == u"隐私玻璃：":
                    self.get_value(td, item, "yinsiboli")
                if td.xpath('span/text()').extract_first() == u"后排侧遮阳帘：":
                    self.get_value(td, item, "houpaicezheyanglian")
                if td.xpath('span/text()').extract_first() == u"后遮阳帘：":
                    self.get_value(td, item, "houzheyanglian")
                if td.xpath('span/text()').extract_first() == u"前雨刷器：":
                    self.get_value(td, item, "qianyushuaqi")
                if td.xpath('span/text()').extract_first() == u"后雨刷器：":
                    self.get_value(td, item, "houyushuaqi")
                if td.xpath('span/text()').extract_first() == u"电吸门：":
                    self.get_value(td, item, "dianximen")
                if td.xpath('span/text()').extract_first() == u"电动侧滑门：":
                    self.get_value(td, item, "diandongcehuamen")
                if td.xpath('span/text()').extract_first() == u"电动行李厢：":
                    self.get_value(td, item, "diandongxinglixiang")
                if td.xpath('span/text()').extract_first() == u"车顶行李架：":
                    self.get_value(td, item, "chedingxinglijia")
                if td.xpath('span/text()').extract_first() == u"中控锁：":
                    self.get_value(td, item, "zhongkongsuo")
                if td.xpath('span/text()').extract_first() == u"智能钥匙：":
                    self.get_value(td, item, "zhinengyaoshi")
                if td.xpath('span/text()').extract_first() == u"远程遥控功能：":
                    self.get_value(td, item, "yuanchengyaokonggongneng")
                if td.xpath('span/text()').extract_first() == u"尾翼/扰流板：":
                    self.get_value(td, item, "weiyi_raoliuban")
                if td.xpath('span/text()').extract_first() == u"运动外观套件：":
                    self.get_value(td, item, "yundongwaiguantaojian")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[14]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"内饰材质：":
                    self.get_value(td, item, "neishicailiao")
                if td.xpath('span/text()').extract_first() == u"车内氛围灯：":
                    self.get_value(td, item, "cheneifenweideng")
                if td.xpath('span/text()').extract_first() == u"遮阳板化妆镜：":
                    self.get_value(td, item, "zheyangbanhuazhuangjing")
                if td.xpath('span/text()').extract_first() == u"方向盘材质：":
                    self.get_value(td, item, "fangxiangpancaizhi")
                if td.xpath('span/text()').extract_first() == u"多功能方向盘：":
                    self.get_value(td, item, "duogongnengfangxiangpan")
                if td.xpath('span/text()').extract_first() == u"方向盘调节：":
                    self.get_value(td, item, "fangxiangpantiaojie")
                if td.xpath('span/text()').extract_first() == u"方向盘加热：":
                    self.get_value(td, item, "fangxiangpanjiare")
                if td.xpath('span/text()').extract_first() == u"方向盘换挡：":
                    self.get_value(td, item, "fangxiangpanhuandang")
                if td.xpath('span/text()').extract_first() == u"前排空调：":
                    self.get_value(td, item, "qianpaikongtiao")
                if td.xpath('span/text()').extract_first() == u"后排空调：":
                    self.get_value(td, item, "houpaikongtiao")
                if td.xpath('span/text()').extract_first() == u"香氛系统：":
                    self.get_value(td, item, "xiangfenxitong")
                if td.xpath('span/text()').extract_first() == u"空气净化：":
                    self.get_value(td, item, "kongqijinghua")
                if td.xpath('span/text()').extract_first() == u"车载冰箱：":
                    self.get_value(td, item, "chezaibingxiang")
                if td.xpath('span/text()').extract_first() == u"主动降噪：":
                    self.get_value(td, item, "zhudongjiangzao")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[16]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"座椅材质：":
                    self.get_value(td, item, "zuoyicaizhi")
                if td.xpath('span/text()').extract_first() == u"运动风格座椅：":
                    self.get_value(td, item, "yundongfenggezuoyi")
                if td.xpath('span/text()').extract_first() == u"主座椅电动调节：":
                    self.get_value(td, item, "zhuzuoyidiandongtiaojie")
                if td.xpath('span/text()').extract_first() == u"副座椅电动调节：":
                    self.get_value(td, item, "fuzuoyidiandongtiaojie")
                if td.xpath('span/text()').extract_first() == u"主座椅调节方式：":
                    self.get_value(td, item, "zhuzuoyitiaojiefangshi")
                if td.xpath('span/text()').extract_first() == u"副座椅调节方式：":
                    self.get_value(td, item, "fuzuoyitiaojiefangshi")
                if td.xpath('span/text()').extract_first() == u"第二排座椅电动调节：":
                    self.get_value(td, item, "dierpaizuoyidiandongtiaojie")
                if td.xpath('span/text()').extract_first() == u"第二排座椅调节方式：":
                    self.get_value(td, item, "dierpaizuoyitiaojiefangshi")
                if td.xpath('span/text()').extract_first() == u"前排座椅功能：":
                    self.get_value(td, item, "qianpaizuoyigongneng")
                if td.xpath('span/text()').extract_first() == u"后排座椅功能：":
                    self.get_value(td, item, "houpaizuoyigongneng")
                if td.xpath('span/text()').extract_first() == u"前排中央扶手：":
                    self.get_value(td, item, "qianpaizhongyangfushou")
                if td.xpath('span/text()').extract_first() == u"后排中央扶手：":
                    self.get_value(td, item, "houpaizhongyangfushou")
                if td.xpath('span/text()').extract_first() == u"第三排座椅：":
                    self.get_value(td, item, "disanpaizuoyi")
                if td.xpath('span/text()').extract_first() == u"座椅放倒方式：":
                    self.get_value(td, item, "zuoyifangdaofangshi")
                if td.xpath('span/text()').extract_first() == u"后排杯架：":
                    self.get_value(td, item, "houpaibeijiang")
                if td.xpath('span/text()').extract_first() == u"后排折叠桌板：":
                    self.get_value(td, item, "houpaizhediezhuoban")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[18]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"中控彩色液晶屏：":
                    self.get_value(td, item, "zhongkongcaiseyejingping")
                if td.xpath('span/text()').extract_first() == u"全液晶仪表盘：":
                    self.get_value(td, item, "quanyejingyibiaopan")
                if td.xpath('span/text()').extract_first() == u"行车电脑显示屏：":
                    self.get_value(td, item, "xingchediannaoxianshiping")
                if td.xpath('span/text()').extract_first() == u"HUD平视显示：":
                    self.get_value(td, item, "hudpingshixianshi")
                if td.xpath('span/text()').extract_first() == u"GPS导航：":
                    self.get_value(td, item, "gpsdaohang")
                if td.xpath('span/text()').extract_first() == u"智能互联定位：":
                    self.get_value(td, item, "zhinenghuliandingwei")
                if td.xpath('span/text()').extract_first() == u"语音控制：":
                    self.get_value(td, item, "yuyinkongzhi")
                if td.xpath('span/text()').extract_first() == u"手机互联(Carplay&Android)：":
                    self.get_value(td, item, "shoujihulian")
                if td.xpath('span/text()').extract_first() == u"手机无线充电：":
                    self.get_value(td, item, "shoujiwuxianchongdian")
                if td.xpath('span/text()').extract_first() == u"手势控制系统：":
                    self.get_value(td, item, "shoushikongzhixitong")
                if td.xpath('span/text()').extract_first() == u"CD/DVD：":
                    self.get_value(td, item, "cd_dvd")
                if td.xpath('span/text()').extract_first() == u"蓝牙/WIFI连接：":
                    self.get_value(td, item, "lanya_wifilianjie")
                if td.xpath('span/text()').extract_first() == u"外接接口：":
                    self.get_value(td, item, "waijiejiekou")
                if td.xpath('span/text()').extract_first() == u"车载行车记录仪：":
                    self.get_value(td, item, "chezaixingchejiluyi")
                if td.xpath('span/text()').extract_first() == u"车载电视：":
                    self.get_value(td, item, "chezaidianshi")
                if td.xpath('span/text()').extract_first() == u"音响品牌：":
                    self.get_value(td, item, "yinxiangpinpai")
                if td.xpath('span/text()').extract_first() == u"扬声器数量：":
                    self.get_value(td, item, "yangshengqishuliang")
                if td.xpath('span/text()').extract_first() == u"后排液晶屏/娱乐系统：":
                    self.get_value(td, item, "houpaiyejingping_yulexitong")
                if td.xpath('span/text()').extract_first() == u"车载220V电源：":
                    self.get_value(td, item, "chezai220vdianyuan")
        except Exception as e:
            pass
            # with open("D:/yiche_newcar.log", "a") as f:
            #     f.write(traceback.format_exc())
            #     f.close()

        print(item)
        # yield item
