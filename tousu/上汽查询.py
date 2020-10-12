import pandas as pd
import pymongo

dict1 = {"code": 200, "message": "操作成功", "data": {"factory": "上汽大众", "brandList": [{"list": [
    {"modelList": [], "family": "朗逸"}, {"modelList": [], "family": "途安"}, {"modelList": [], "family": "途观"},
    {"modelList": [], "family": "帕萨特"}, {"modelList": [], "family": "途岳"}, {"modelList": [], "family": "朗行"},
    {"modelList": [], "family": "Passat领驭"}, {"modelList": [], "family": "Polo"}, {"modelList": [], "family": "桑塔纳"},
    {"modelList": [], "family": "途观L"}, {"modelList": [], "family": "桑塔纳志俊"}, {"modelList": [], "family": "桑塔纳经典"},
    {"modelList": [], "family": "朗境"}, {"modelList": [], "family": "帕萨特新能源"}, {"modelList": [], "family": "凌渡"},
    {"modelList": [], "family": "途昂X"}, {"modelList": [], "family": "途昂"}, {"modelList": [], "family": "途铠"},
    {"modelList": [], "family": "途观L新能源"}, {"modelList": [], "family": "辉昂"}, {"modelList": [], "family": "桑塔纳·浩纳"},
    {"modelList": [], "family": "新桑塔纳"}, {"modelList": [], "family": "桑塔纳·尚纳"},
    {"modelList": [], "family": "Cross桑塔纳"}], "brand": "大众"}, {"list": [{"modelList": [], "family": "明锐"},
                                                                        {"modelList": [], "family": "Yeti"},
                                                                        {"modelList": [], "family": "晶锐"},
                                                                        {"modelList": [], "family": "昊锐"},
                                                                        {"modelList": [], "family": "柯迪亚克"},
                                                                        {"modelList": [], "family": "昕锐"},
                                                                        {"modelList": [], "family": "昕动"},
                                                                        {"modelList": [], "family": "速派"},
                                                                        {"modelList": [], "family": "柯迪亚克GT"},
                                                                        {"modelList": [], "family": "柯珞克"},
                                                                        {"modelList": [], "family": "柯米克"}],
                                                               "brand": "斯柯达"}]}}

dict2 = {"code": 200, "message": "操作成功", "data": {"factory": "上汽通用", "brandList": [{"list": [
    {"modelList": [], "family": "VELITE 6"}, {"modelList": [], "family": "别克GL6"},
    {"modelList": [], "family": "VELITE 5"}, {"modelList": [], "family": "别克GL8"}, {"modelList": [], "family": "凯越"},
    {"modelList": [], "family": "君威"}, {"modelList": [], "family": "君越"}, {"modelList": [], "family": "英朗"},
    {"modelList": [], "family": "阅朗"}, {"modelList": [], "family": "林荫大道"}, {"modelList": [], "family": "昂科拉GX"},
    {"modelList": [], "family": "威朗"}, {"modelList": [], "family": "昂科威"}, {"modelList": [], "family": "昂科拉"},
    {"modelList": [], "family": "昂科旗"}, {"modelList": [], "family": "荣御"}, {"modelList": [], "family": "微蓝"},
    {"modelList": [], "family": "昂科雷"}], "brand": "别克"}, {"list": [{"modelList": [], "family": "乐风"},
                                                                   {"modelList": [], "family": "科鲁兹"},
                                                                   {"modelList": [], "family": "赛欧"},
                                                                   {"modelList": [], "family": "乐骋"},
                                                                   {"modelList": [], "family": "景程"},
                                                                   {"modelList": [], "family": "科帕奇"},
                                                                   {"modelList": [], "family": "迈锐宝XL"},
                                                                   {"modelList": [], "family": "科鲁泽"},
                                                                   {"modelList": [], "family": "创酷"},
                                                                   {"modelList": [], "family": "爱唯欧"},
                                                                   {"modelList": [], "family": "创界"},
                                                                   {"modelList": [], "family": "沃兰多"},
                                                                   {"modelList": [], "family": "乐风RV"},
                                                                   {"modelList": [], "family": "探界者"},
                                                                   {"modelList": [], "family": "迈锐宝"},
                                                                   {"modelList": [], "family": "科沃兹"}], "brand": "雪佛兰"},
    {"list": [{"modelList": [],
               "family": "凯迪拉克CT6"},
              {"modelList": [],
               "family": "凯迪拉克XT4"},
              {"modelList": [],
               "family": "凯迪拉克XT6"},
              {"modelList": [],
               "family": "SLS赛威"},
              {"modelList": [],
               "family": "凯迪拉克CT5"},
              {"modelList": [],
               "family": "凯迪拉克CTS"},
              {"modelList": [],
               "family": "凯迪拉克XTS"},
              {"modelList": [],
               "family": "凯迪拉克ATS-L"},
              {"modelList": [],
               "family": "凯迪拉克XT5"}],
     "brand": "凯迪拉克"}]}}

dict3 = {"code": 200, "message": "操作成功", "data": {"factory": "上汽乘用车", "brandList": [{"list": [
    {"modelList": [], "family": "荣威550"}, {"modelList": [], "family": "荣威RX5"}, {"modelList": [], "family": "荣威e550"},
    {"modelList": [], "family": "荣威e50"}, {"modelList": [], "family": "荣威W5"},
    {"modelList": [], "family": "荣威MARVEL X"}, {"modelList": [], "family": "荣威RX5 MAX"},
    {"modelList": [], "family": "荣威RX5新能源"}, {"modelList": [], "family": "荣威950"}, {"modelList": [], "family": "荣威i6"},
    {"modelList": [], "family": "荣威RX8"}, {"modelList": [], "family": "荣威360"}, {"modelList": [], "family": "荣威RX3"},
    {"modelList": [], "family": "荣威350"}, {"modelList": [], "family": "荣威750"}, {"modelList": [], "family": "Vision-R"},
    {"modelList": [], "family": "荣威MAX"}, {"modelList": [], "family": "荣威ei6"}, {"modelList": [], "family": "荣威i5"},
    {"modelList": [], "family": "荣威Ei5"}, {"modelList": [], "family": "荣威e950"}], "brand": "荣威"}, {"list": [
    {"modelList": [], "family": "名爵5"}, {"modelList": [], "family": "名爵6"}, {"modelList": [], "family": "锐腾"},
    {"modelList": [], "family": "名爵7"}, {"modelList": [], "family": "名爵EZS纯电动"}, {"modelList": [], "family": "名爵3"},
    {"modelList": [], "family": "锐行"}, {"modelList": [], "family": "名爵TF"}, {"modelList": [], "family": "名爵3SW"},
    {"modelList": [], "family": "名爵6新能源"}, {"modelList": [], "family": "名爵HS"}, {"modelList": [], "family": "名爵iGS"},
    {"modelList": [], "family": "MG&nbspZS"}], "brand": "名爵"}]}}

dict4 = {"code": 200, "message": "操作成功", "data": {"factory": "上汽通用五菱", "brandList": [{"list": [
    {"modelList": [], "family": "宝骏510"}, {"modelList": [], "family": "宝骏610"}, {"modelList": [], "family": "宝骏E200"},
    {"modelList": [], "family": "宝骏310W"}, {"modelList": [], "family": "新宝骏RS-5"}, {"modelList": [], "family": "宝骏310"},
    {"modelList": [], "family": "宝骏530"}, {"modelList": [], "family": "新宝骏RC-6"}, {"modelList": [], "family": "宝骏730"},
    {"modelList": [], "family": "宝骏360"}, {"modelList": [], "family": "宝骏630"}, {"modelList": [], "family": "宝骏E100"},
    {"modelList": [], "family": "宝骏560"}, {"modelList": [], "family": "新宝骏RM-5"}], "brand": "宝骏"}, {"list": [
    {"modelList": [], "family": "PN货车"}, {"modelList": [], "family": "五菱荣光V"}, {"modelList": [], "family": "五菱之光小卡"},
    {"modelList": [], "family": "五菱荣光小卡"}, {"modelList": [], "family": "五菱荣光"}, {"modelList": [], "family": "五菱征程"},
    {"modelList": [], "family": "五菱宏光"}, {"modelList": [], "family": "五菱之光"}, {"modelList": [], "family": "五菱宏光V"},
    {"modelList": [], "family": "五菱宏光S3"}, {"modelList": [], "family": "五菱荣光新卡"}], "brand": "五菱汽车"}]}}

dict5 = {"code": 200, "message": "操作成功", "data": {"factory": "上汽大通", "brandList": [{"list": [
    {"modelList": [], "family": "上汽大通G10"}, {"modelList": [], "family": "上汽大通D60"},
    {"modelList": [], "family": "大通EV80"}, {"modelList": [], "family": "上汽大通V80"},
    {"modelList": [], "family": "上汽MAXUS T70"}, {"modelList": [], "family": "上汽大通D90"},
    {"modelList": [], "family": "上汽大通T60"}, {"modelList": [], "family": "上汽大通G20"},
    {"modelList": [], "family": "上汽大通EG10"}, {"modelList": [], "family": "上汽大通G50"},
    {"modelList": [], "family": "上汽大通EG50"}], "brand": "上汽大通"}]}}

dict6 = {"code": 200, "message": "操作成功", "data": {"factory": "南京依维柯", "brandList": [{"list": [
    {"modelList": [], "family": "快运王"}, {"modelList": [], "family": "跃进经典"},
    {"modelList": [], "family": "依维柯Daily(欧胜)"}, {"modelList": [], "family": "依维柯"},
    {"modelList": [], "family": "依维柯得意"}, {"modelList": [], "family": "依维柯Power Daily"},
    {"modelList": [], "family": "跃进"}, {"modelList": [], "family": "红岩金刚"}, {"modelList": [], "family": "都灵"},
    {"modelList": [], "family": "依维柯Ouba"}, {"modelList": [], "family": "超越"}, {"modelList": [], "family": "跃进轻卡"},
    {"modelList": [], "family": "跃进货车"}, {"modelList": [], "family": "红岩牌"}], "brand": "依维柯"}]}}

list_all = [dict1, dict2, dict3, dict4, dict5, dict6]

dataSource_list = ['315汽车网', '车质网', '汽车消费网', '汽车投诉网']

brand_item = dict()
for i in list_all:
    factory = i['data']['factory']
    brands = i['data']['brandList']

    for brand in brands:
        brandname = brand['brand']
        family_serch = ''
        for family in brand['list']:
            familyname = family['family']
            str_find_insert = str({"series": {'$regex': f'{familyname}'}})
            family_serch = family_serch + str_find_insert + ','
        item_family = dict()
        item_family[brandname] = family_serch
        # print(item_family)
        brand_item.update(item_family)
        break
    break

# 连接数据库
str1 = [{'series': {'$regex': '朗逸'}}, {'series': {'$regex': '途安'}},{'series': {'$regex': '途观'}}, {'series': {'$regex': '帕萨特'}},{'series': {'$regex': '途岳'}}, {'series': {'$regex': '朗行'}},{'series': {'$regex': 'Passat领驭'}}, {'series': {'$regex': 'Polo'}},{'series': {'$regex': '桑塔纳'}}, {'series': {'$regex': '途观L'}},{'series': {'$regex': '桑塔纳志俊'}}, {'series': {'$regex': '桑塔纳经典'}},{'series': {'$regex': '朗境'}}, {'series': {'$regex': '帕萨特新能源'}},{'series': {'$regex': '凌渡'}}, {'series': {'$regex': '途昂X'}},{'series': {'$regex': '途昂'}}, {'series': {'$regex': '途铠'}},{'series': {'$regex': '途观L新能源'}}, {'series': {'$regex': '辉昂'}},{'series': {'$regex': '桑塔纳·浩纳'}}, {'series': {'$regex': '新桑塔纳'}},{'series': {'$regex': '桑塔纳·尚纳'}}, {'series': {'$regex': 'Cross桑塔纳'}}]


client = pymongo.MongoClient('192.168.2.149', 27017)
db = client['tousu']
collection = db['quanwang_tousu']
brand = collection.find({'$and': [{'$and': [{'tousu_date': {'$lte': '2020-08-31'}},{'tousu_date': {'$gte': '2020-08-01'}}, {'dataSource': '车质网'}]}, {
                                      '$or': str1}]})
df = pd.DataFrame(list(brand))
print(len(df))
# 数据库查询
# for dataSource in dataSource_list:
#     for key, value in brand_item.items():
#         serch = {"$and": [{"$and": [{"tousu_date": {"$lte": "2020-08-31"}}, {"tousu_date": {"$gte": "2020-08-01"}},
#                                     {"dataSource": dataSource}]}, {"$or": [value[:-1]]}]}
#         # print(key,value)
#         print(serch)
#         find_brand = collection.find(serch)
#         df = pd.DataFrame(list(find_brand))
#         print(dataSource, key, len(df))
#
li = {'series': {'$regex': '新桑塔纳'}}
