import time
from tqdm import tqdm
import pymongo
from pandas import DataFrame

city_list = ['安阳', '鞍山', '安庆', '安康', '阿坝', '阿拉善', '阿克苏', '阿勒泰', '安顺', '澳门', '阿拉尔', '阿里', '北京', '蚌埠', '保定',
             '本溪', '包头', '亳州', '滨州', '白城', '百色', '白山', '白银', '宝鸡', '保山', '巴彦淖尔', '巴中', '北海', '毕节', '博尔塔拉',
             '巴音郭楞', '重庆', '成都', '长春', '长沙', '承德', '常州', '滁州', '沧州', '常德', '昌吉', '长治', '朝阳', '潮州', '郴州',
             '楚雄', '赤峰', '池州', '崇左', '昌都', '大连', '东莞', '德州', '丹东', '大理', '大庆', '大同', '达州', '德宏', '德阳',
             '定西', '迪庆', '东营', '东方', '儋州', '定安', '大兴安岭', '鄂州', '鄂尔多斯', '恩施', '福州', '阜阳', '佛山', '抚州', '防城港',
             '抚顺', '阜新', '广州', '贵阳', '桂林', '赣州', '广元', '甘孜', '广安', '贵港', '固原', '甘南', '果洛', '杭州', '合肥',
             '哈尔滨', '海口', '衡阳', '邯郸', '呼和浩特', '黄冈', '黄石', '湖州', '衡水', '呼伦贝尔', '黄山', '海北', '海西', '哈密', '汉中',
             '鹤壁', '河池', '鹤岗', '黑河', '和田', '河源', '菏泽', '贺州', '红河', '淮安', '淮北', '怀化', '淮南', '惠州', '葫芦岛',
             '海东', '海南', '黄南', '吉林', '济南', '九江', '揭阳', '酒泉', '嘉兴', '荆州', '锦州', '佳木斯', '吉安', '江门', '焦作',
             '嘉峪关', '金昌', '晋城', '景德镇', '荆门', '金华', '济宁', '晋中', '鸡西', '济源', '昆明', '开封', '喀什', '克拉玛依',
             '克孜勒苏', '兰州', '廊坊', '六安', '乐山', '来宾', '柳州', '聊城', '莱芜', '拉萨', '洛阳', '凉山', '连云港', '辽阳', '辽源',
             '丽江', '临沧', '临汾', '临夏', '临沂', '林芝', '丽水', '六盘水', '陇南', '龙岩', '娄底', '漯河', '泸州', '吕梁', '绵阳',
             '马鞍山', '茂名', '眉山', '梅州', '牡丹江', '南京', '南昌', '南宁', '宁波', '南通', '南充', '南平', '南阳', '内江', '宁德',
             '那曲', '怒江', '莆田', '濮阳', '盘锦', '攀枝花', '平顶山', '平凉', '萍乡', '普洱', '青岛', '秦皇岛', '泉州', '衢州', '曲靖',
             '黔东南', '黔南', '黔西南', '庆阳', '清远', '钦州', '齐齐哈尔', '七台河', '琼海', '潜江', '日照', '日喀则', '上海', '深圳',
             '沈阳', '石家庄', '三门峡', '三明', '三亚', '商洛', '商丘', '苏州', '汕头', '汕尾', '十堰', '遂宁', '上饶', '绍兴', '邵阳',
             '双鸭山', '朔州', '四平', '松原', '绥化', '随州', '宿迁', '宿州', '石嘴山', '韶关', '神农架', '石河子', '山南', '天津', '太原',
             '唐山', '台州', '塔城', '泰安', '铁岭', '泰州', '天水', '铜川', '通化', '通辽', '铜陵', '铜仁', '吐鲁番', '天门', '台湾',
             '图木舒克', '武汉', '温州', '无锡', '乌鲁木齐', '芜湖', '潍坊', '威海', '渭南', '文山', '乌海', '乌兰察布', '武威', '吴忠',
             '梧州', '万宁', '五指山', '文昌', '五家渠', '西安', '厦门', '湘潭', '徐州', '许昌', '信阳', '西宁', '咸阳', '宣城', '新乡',
             '湘西', '襄阳', '咸宁', '孝感', '锡林郭勒', '兴安', '邢台', '新余', '忻州', '西双版纳', '香港', '仙桃', '扬州', '银川', '宜昌',
             '岳阳', '榆林', '烟台', '雅安', '延安', '延边', '盐城', '阳江', '阳泉', '宜宾', '伊春', '宜春', '伊犁', '营口', '鹰潭',
             '益阳', '永州', '玉林', '运城', '云浮', '玉溪', '玉树', '珠海', '肇庆', '张家口', '中山', '淄博', '驻马店', '枣庄', '张家界',
             '张掖', '漳州', '湛江', '昭通', '郑州', '镇江', '中卫', '周口', '舟山', '株洲', '自贡', '资阳', '遵义']

# %%

connection = pymongo.MongoClient('192.168.1.94', 27017)
db = connection["newcar"]
collection = db["dongchedi_car"]
model_data = collection.find({}, {"car_id": 1, "_id": 0})
car_msg_list = list(model_data)
connection.close()
car_msg_df = DataFrame(car_msg_list)
car_msg_df_new = car_msg_df.drop_duplicates('car_id')
print(len(car_msg_df_new))
print(len(city_list))
print(len(car_msg_df_new)*len(city_list))
# %%

connection149 = pymongo.MongoClient('192.168.2.149', 27017)
db149 = connection149["newcar_price"]
collection149 = db149["dongchedi_url"]
url_lsit = []
for index, rows in tqdm(car_msg_df_new.iterrows()):
    car_id = rows['car_id']
    for city in city_list:
        item = {}
        url = f'https://www.dongchedi.com/motor/dealer/m/v1/get_dealers_car_info/?car_id={car_id}&city_name={city}&sort_type=1'
        # url = 'https://www.dongchedi.com/motor/dealer/m/v1/get_dealers_car_info/?car_id=50398&city_name=%E5%8C%97%E4%BA%AC&sort_type=1'
        item['push_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['url'] = url
        item['car_id'] = str(car_id)
        item['city'] = city
        url_lsit.append(item)
try:
    collection149.insert_many(url_lsit)
except Exception as e:
    print('没插进去', e)
