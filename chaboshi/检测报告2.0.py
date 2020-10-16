import time

import pymongo
import requests
from lxml import etree


def jiancebaogao2(url):
    response = requests.get(url)
    html = response.text
    text = etree.HTML(html)
    # 合同协议网页里面获取VIN码
    xieyi_url = 'https://app.chaboshi.cn/' + text.xpath('//iframe[@id="iframe2"]/@src')[0]
    xieyi_response = requests.get(xieyi_url)
    xieyi_html = xieyi_response.text
    xieyi_text = etree.HTML(xieyi_html)
    # 首页图片跳转图片url
    images_url = 'https://app.chaboshi.cn/wap/' + \
                 text.xpath('//img[@class="detectReportImgTop"]/@onclick')[0].split("'")[1]
    images_response = requests.get(images_url)
    images_html = images_response.text
    images_text = etree.HTML(images_html)

    item = {}

    # %% 基本信息

    cheliangmingcheng = text.xpath('//p[@class="detectionCarName"]/text()')[0]
    VIN = xieyi_text.xpath('//ul[@class="insurContract"]/li/input/@value')[0]
    jianceriqi = xieyi_text.xpath('//ul[@class="insurContract"]/li/input/@value')[1]
    jiancejieguo = xieyi_text.xpath('//ul[@class="insurContract"]/li/input/@value')[2]
    baogaobianhao = text.xpath('//p[@class="detectionCarNo"]/text()')[0]
    baogao = baogaobianhao.split('：')[0]
    bianhao = baogaobianhao.split('：')[1]
    jianceshi = text.xpath('//div[@class="detectionScoreTime"]/p/text()')[0]
    jianceshihaoma = text.xpath('//div[@class="detectionScoreTime"]/a/@href')[0]

    jibenxinxi = {'车辆名称': cheliangmingcheng, 'VIN': VIN, '检测日期': jianceriqi, '检测结果': jiancejieguo, baogao: bianhao,
                  '检测人员': jianceshi, '检测人员联系方式': jianceshihaoma}
    print(jibenxinxi)
    item['基本信息'] = jibenxinxi

    # %% 综合评分

    zonghepingfen = text.xpath('//div[@class="detectionBoxNew"]/p/text()')[0]
    zonghepingfen1 = zonghepingfen.split(' ')[0]
    zonghepingfen2 = zonghepingfen.split(' ')[1]
    zonghepingfen3 = zonghepingfen.split(' ')[2]
    jiancejieguo = text.xpath('//div[@class="detectionBoxNew"]/div/label/text()')[0]

    lis = text.xpath('//ul[@class="detectionScoreList"]/li')
    gexiangzongji = {}
    for li in lis:
        leibie = li.xpath('./p/text()')[0]
        try:
            jishu = li.xpath('./div/span/text()')[0]
        except:
            jishu = '0'
        gexiangzongji[leibie] = jishu

    zongshu = text.xpath('//div[@class="detectionCarTxt"]/div/text()')[0]

    zonghefen = {'事故车/ 非泡水/ 非火烧': zonghepingfen1, '重要车况评分': zonghepingfen2, '重要部件评级': zonghepingfen3,
                 '检测结果': jiancejieguo, '各项综合计数': gexiangzongji, '车况综述': zongshu}
    print(zonghefen)
    item['综合评分'] = zonghefen

    # %%  车辆信息

    # 车辆证件信息
    lis = text.xpath('//ul[@class="parameterList"]/li')
    item_zhengjianxinxi = {}
    for i in lis[1:]:
        label = i.xpath('./label/text()')[0]
        span = i.xpath('./span/text()')[0]
        item_zhengjianxinxi[label] = span

    # 实车配置
    item_shichepeizhi = {}
    span = text.xpath('//ul[@class="parameterList parameterListTwo"]/li[2]/span/text()')[0]
    label = text.xpath('//ul[@class="parameterList parameterListTwo"]/li[2]/label/text()')[0].strip()
    item_shichepeizhi[span] = label

    shichejiance = {'车辆&证件信息': item_zhengjianxinxi, '试车配置': item_shichepeizhi}
    print(shichejiance)

    item['实车检测'] = shichejiance

    # %% 各项检测
    item_gexiangjiance = {}
    all_div = text.xpath('//div[@class="detectionTab detectionTab1"]/div')
    for div in all_div[1:-4]:
        jiancemingcheng = div.xpath('./div/div/div/text()')[0]
        zongji = div.xpath('.//label[@class="parameterNo"]/text()')[0]
        lis = div.xpath('.//ul[@class="exterior"]/li')
        item_danxiang = {}
        item_danxiang['总计'] = zongji
        for li in lis:
            span = li.xpath('./span/text()')[0]
            label = li.xpath('./label/text()')[0]
            try:
                biaoshi = li.xpath('./img[@class="exteriorNewImg"]/@src')[0]
                label = '黄色!--' + label
            except:
                label = '正常--' + label
            item_danxiang[span] = label
        item_gexiangjiance[jiancemingcheng] = item_danxiang
    print(item_gexiangjiance)
    item['各项检测'] = item_gexiangjiance

    # %% 车辆图片
    item_tupian = {}
    # 基础图片
    item_jichutupian = {}
    lis = images_text.xpath('//div[@class="detectionTabV2"][1]/ul[@class="detectionTabImg"]/li')
    for li in lis:
        label = li.xpath('./label/text()')[0]
        image_url = li.xpath('./img/@src')[0]
        # print(label,images_url)
        item_jichutupian[label] = image_url
    # 检测照片
    item_jiancezhaopian = {}
    lis = images_text.xpath('//div[@class="detectionTabV2"][2]/ul[@class="detectionTabImg"]/li')
    for li in lis:
        label = li.xpath('./label/text()')[0]
        image_url = li.xpath('./img/@src')[0]
        # print(label,images_url)
        item_jiancezhaopian[label] = image_url
    item_tupian = {'基础图片': item_jichutupian, '检测照片': item_jiancezhaopian}
    item['图片'] = item_tupian

    # %%
    item = str(item).replace("'", '"')
    return item


url_list = ['https://m.chaboshi.cn/wap/findShareDetection?orderno=709c4319f5c543e4a45760721942864b',
            'https://m.chaboshi.cn/wap/findShareDetection?orderno=371274f31db142d3be83caf7d5ee144f',
            'https://m.chaboshi.cn/wap/findShareDetection?orderno=7d4ba984454748448d51b4353e210017',
            'https://m.chaboshi.cn/wap/findShareDetection?orderno=849bb7abb7394d7985a0c5c6d73e695a',
            'https://m.chaboshi.cn/wap/findShareDetection?orderno=2666e18b46a343e48f0a56bdd9b6670d',
            'https://m.chaboshi.cn/wap/findShareDetection?orderno=d58ab6fca707488388f27930b6c0a78f',
            'https://m.chaboshi.cn/wap/findShareDetection?orderno=6795e8c6c7394f209c4e31aac48f95df']

connection = pymongo.MongoClient("192.168.2.149", 27017)
db = connection['chaboshi']
collection = db['report2.0']
for url in url_list:
    item = {}
    meta = jiancebaogao2(url)
    item['url'] = url
    item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    item['meta'] = meta
    collection.insert(dict(item))
