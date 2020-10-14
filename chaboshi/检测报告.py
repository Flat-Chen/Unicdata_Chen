# %%
import time
import pymongo
import requests
from lxml import etree


def baogao_json(url):
    response = requests.get(url)
    html = response.text
    text = etree.HTML(html)
    # print(html)
    # print(text)
    item = {}
    # %% 车辆信息

    车辆名称 = text.xpath('//div[@class="detectionCarTopRTit detectionCarTopRTitImg"]/label/text()')[0]
    VIN = ''.join(text.xpath('//div[@class="detectionCarTopRTit detectionCarTopRTitImg"]/text()')).strip().split('：')[
        -1]
    评级 = text.xpath('//div[@class="detectionCarTopRTit detectionCarTopRTitImg"]/img/@src')[0].split('.')[-2][-1]

    # print(车辆名称,VIN,评级)
    item_cheliangxinxi = {'车辆名称': 车辆名称, 'VIN': VIN, '评级': 评级}

    item['车辆信息'] = item_cheliangxinxi

    # %% 基本信息

    item_jibenxinxi = {}
    div_jiben = text.xpath('//div[@class="customCol1"]/ul[@class="detectionCarInfo"]/li')
    for i in div_jiben:
        label = i.xpath('./label/text()')[0]
        span = i.xpath('./span/text()')[0]
        item_jibenxinxi[label] = span
        # print(label,span)
    # print(item_jibenxinxi)

    item['基本信息'] = item_jibenxinxi

    # %% 检测项目
    # 加！--为红色感叹号的标
    item_jiancexiangmu = {}
    div_jiance = text.xpath('//table[@class="detectionItems"]//td')
    for i in div_jiance:
        p1 = ''.join(i.xpath('./p/text()')).strip()
        div = i.xpath('./div/text()')[0]
        try:
            logo = i.xpath('./p/span/@class')[0]
            div = '!--' + div
        except:
            pass
        item_jiancexiangmu[p1] = div
    # print(item_jiancexiangmu)

    item['检测项目'] = item_jiancexiangmu

    # %% 车辆综述
    zongshu = text.xpath('//div[@class="detectionCarTxt"]/text()')[0].replace(' ', '').replace('\n', '')
    # print(zongshu)
    item_cheliangzongshu = {'车辆综述': zongshu}
    # print(item_cheliangzongshu)

    item['车辆综述'] = item_cheliangzongshu

    # %% 检测信息-车身结构
    item_jiancexinxi = {}
    item_cheshenjiegou = {}
    info_cheshenjiegou = text.xpath('//div[@class="reportInfo"][1]/label/text()')[0]
    # print(info_cheshenjiegou)
    item_cheshenjiegou['车身结构'] = info_cheshenjiegou

    meta = {}
    tds = text.xpath('//table[@class="reportInfoTab"][1]//td')
    for td in tds:
        label = td.xpath('./label/text()')[0]
        try:
            span = '黄色-' + td.xpath('./span/text()')[0]
        except:
            span = '绿色-正常'
        meta[label] = span
    item_cheshenjiegou['meta'] = meta
    # print(item_cheshenjiegou)

    item_jiancexinxi['车身结构'] = item_cheshenjiegou

    # %% 检测信息-动力系统
    item_donglixitong = {}
    info_donglixitong = text.xpath('//div[@class="reportInfo"][2]/label/text()')[0]
    # print(info_donglixitong)
    item_donglixitong['动力系统'] = info_donglixitong

    meta = {}
    tds = text.xpath('//table[@class="reportInfoTab"][2]//td')
    for td in tds:
        label = td.xpath('./label/text()')[0]
        try:
            span = '黄色-' + td.xpath('./span/text()')[0]
        except:
            span = '绿色-正常'
        meta[label] = span
    item_donglixitong['meta'] = meta
    # print(item_donglixitong)

    item_jiancexinxi['动力系统'] = item_donglixitong

    # %% 检测系统-外观内饰
    item_waiguanneishi = {}
    info_waiguanneishi = text.xpath('//div[@class="reportInfo"][3]/label/text()')[0]
    # print(info_waiguanneishi)
    item_waiguanneishi['外观内饰'] = info_waiguanneishi

    meta = {}
    tds = text.xpath('//table[@class="reportInfoTab"][3]//td')
    for td in tds:
        label = td.xpath('./label/text()')[0]
        try:
            span = '黄色-' + td.xpath('./span/text()')[0]
        except:
            span = '绿色-正常'
        meta[label] = span
    item_waiguanneishi['meta'] = meta
    # print(item_waiguanneishi)

    item_jiancexinxi['外观内饰'] = item_waiguanneishi

    # %% 检测系统-安全系统
    item_anquanxitong = {}
    info_anquanxitong = text.xpath('//div[@class="reportInfo"][4]/label/text()')[0]
    # print(info_anquanxitong)
    item_anquanxitong['安全系统'] = info_anquanxitong

    meta = {}
    tds = text.xpath('//table[@class="reportInfoTab"][4]//td')
    for td in tds:
        label = td.xpath('./label/text()')[0]
        try:
            span = '黄色-' + td.xpath('./span/text()')[0]
        except:
            span = '绿色-正常'
        meta[label] = span
    item_anquanxitong['meta'] = meta
    # print(item_anquanxitong)

    item_jiancexinxi['安全系统'] = item_anquanxitong

    # %% 检测系统-车身底盘
    item_cheshendipan = {}
    info_cheshendipan = text.xpath('//div[@class="reportInfo"][5]/label/text()')[0]
    # print(info_cheshendipan)
    item_cheshendipan['车身底盘'] = info_cheshendipan

    meta = {}
    tds = text.xpath('//table[@class="reportInfoTab"][5]//td')
    for td in tds:
        label = td.xpath('./label/text()')[0]
        try:
            span = '黄色-' + td.xpath('./span/text()')[0]
        except:
            span = '绿色-正常'
        meta[label] = span
    item_cheshendipan['meta'] = meta
    # print(item_cheshendipan)

    item_jiancexinxi['车身底盘'] = item_cheshendipan

    # %% 检测系统-电气系统
    item_dianqixitong = {}
    info_dianqixitong = text.xpath('//div[@class="reportInfo"][6]/label/text()')[0]
    # print(info_dianqixitong)
    item_dianqixitong['电气系统'] = info_dianqixitong

    meta = {}
    tds = text.xpath('//table[@class="reportInfoTab"][6]//td')
    for td in tds:
        label = td.xpath('./label/text()')[0]
        try:
            span = '黄色-' + td.xpath('./span/text()')[0]
        except:
            span = '绿色-正常'
        meta[label] = span
    item_dianqixitong['meta'] = meta
    # print(item_dianqixitong)

    item_jiancexinxi['电气系统'] = item_dianqixitong

    item['监测信息'] = item_jiancexinxi

    # %%
    item = str(item).replace("'", '"')
    return item


url_list = ['http://m.chaboshi.cn/web/pcInsuranceReport?orderno=c2391b1f75da4beda80c288eff3b5706',
            'http://m.chaboshi.cn/web/pcInsuranceReport?orderno=9a09f2d144cf40db96800bb7c00ff03a']

connection = pymongo.MongoClient("192.168.2.149", 27017)
db = connection['chaboshi']
collection = db['report']
for url in url_list:
    item = {}
    meta = baogao_json(url)
    item['url'] = url
    item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    item['meta'] = meta
    collection.insert(dict(item))
