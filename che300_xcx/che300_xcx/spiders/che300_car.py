import json
import time

from che300_xcx.items import Che300CarItem

import scrapy


class Che300CarSpider(scrapy.Spider):
    name = 'che300_car'
    allowed_domains = ['che300.com']

    # start_urls = ['http://che300.com/']
    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(Che300CarSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': "192.168.1.94",
        'MYSQL_USER': "dataUser94",
        'MYSQL_PWD': "94dataUser@2020",
        'MYSQL_PORT': 3306,
        'MYSQL_DB': "che300",
        'MYSQL_TABLE': "che300_car",
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'che300',
        'MONGODB_COLLECTION': 'che300_car',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        # 'DOWNLOAD_TIMEOUT': 5,
        # 'RETRY_ENABLED': False,
        # 'RETRY_TIMES': 1,
    }

    def start_requests(self):
        brand_item = {'奥迪': '1',
                      '阿尔法·罗密欧': '3',
                      '阿斯顿·马丁': '2',
                      'ALPINA': '536',
                      'AUXUN傲旋': '1714',
                      'AC Schnitzer': '4',
                      'ARCFOX': '1721',
                      '爱驰': '1407',
                      '本田': '5',
                      '宝马': '7',
                      '宝骏': '15',
                      '宝沃': '172',
                      '宝龙': '144',
                      '奔驰': '9',
                      '奔腾': '12',
                      '别克': '6',
                      '标致': '10',
                      '比亚迪': '8',
                      '比速': '499',
                      '比德文汽车': '853',
                      '保时捷': '11',
                      '保斐利': '20',
                      '北汽绅宝': '115',
                      '北汽幻速': '156',
                      '北汽威旺': '17',
                      '北汽制造': '14',
                      '北汽新能源': '167',
                      '北汽道达': '573',
                      '北京汽车': '13',
                      '北京清行': '837',
                      '宾利': '16',
                      '巴博斯': '19',
                      '布加迪': '18',
                      '长安': '21',
                      '长安欧尚': '23',
                      '长城': '22',
                      '昌河': '24',
                      '成功': '497',
                      '车驰汽车': '1716',
                      '大众': '25',
                      '大乘汽车': '639',
                      '大运': '1705',
                      '大迪': '142',
                      '东风风行': '26',
                      '东风风光': '170',
                      '东风风神': '30',
                      '东风': '33',
                      '东风小康': '28',
                      '东风风度': '32',
                      '东风瑞泰特': '620',
                      '东南': '27',
                      '道奇': '29',
                      'DS': '31',
                      '电咖': '574',
                      '丰田': '36',
                      '福特': '35',
                      '福田': '39',
                      '福田乘用车': '545',
                      '福迪': '40',
                      '福汽启腾': '162',
                      '菲亚特': '37',
                      '菲斯克': '42',
                      '法拉利': '38',
                      '富奇': '147',
                      '枫叶汽车': '1704',
                      '飞碟': '543',
                      '飞驰商务车': '41',
                      '广汽传祺': '44',
                      '广汽新能源': '636',
                      '广汽吉奥': '45',
                      '观致': '46',
                      'GMC': '47',
                      '国机智骏': '1075',
                      '国金': '586',
                      '光冈': '48',
                      '高合汽车': '1772',
                      '哈弗': '50',
                      '哈飞': '56',
                      '海马': '51',
                      '海马商用车': '54',
                      '海格': '57',
                      '红旗': '53',
                      '红星汽车': '618',
                      '华泰': '52',
                      '华泰新能源': '173',
                      '华颂': '160',
                      '华普': '146',
                      '华骐': '560',
                      '汉腾': '495',
                      '汉龙汽车': '1300',
                      '黄海': '55',
                      '悍马': '145',
                      '汇众': '59',
                      'HYCAN合创': '1703',
                      '恒天': '58',
                      '航天凌河': '2094',
                      'IMSA英飒': '1766',
                      '吉利': '143',
                      '吉利帝豪': '63',
                      '吉利全球鹰': '62',
                      '吉利英伦': '65',
                      '江淮': '60',
                      '江铃': '66',
                      '江铃集团新能源': '542',
                      '江南': '68',
                      'Jeep': '61',
                      '捷豹': '64',
                      '捷途汽车': '634',
                      '捷达': '852',
                      '金杯': '67',
                      '金龙联合': '69',
                      '金旅客车': '71',
                      '金冠': '657',
                      '九龙': '70',
                      '君马汽车': '572',
                      '几何汽车': '825',
                      '钧天': '752',
                      '巨威': '817',
                      '凯迪拉克': '73',
                      '凯翼': '157',
                      '凯佰赫': '678',
                      '凯马': '819',
                      '克莱斯勒': '74',
                      '开瑞': '75',
                      '卡威': '158',
                      '卡升': '562',
                      '卡尔森': '77',
                      '康迪全球鹰': '546',
                      'KTM': '552',
                      '科尼赛克': '76',
                      '雷克萨斯': '80',
                      '雷诺': '84',
                      '雷丁': '640',
                      '路虎': '79',
                      '路特斯': '90',
                      '铃木': '78',
                      '猎豹': '85',
                      '林肯': '87',
                      '陆风': '83',
                      '陆地方舟': '619',
                      '领克': '561',
                      '领途汽车': '682',
                      '力帆': '81',
                      '理念': '89',
                      '理想': '815',
                      '劳斯莱斯': '86',
                      '兰博基尼': '82',
                      '莲花': '88',
                      '拉达LADA': '588',
                      'LITE': '587',
                      'Lorinser': '661',
                      '凌宝汽车': '1718',
                      '罗夫哈特': '712',
                      '零跑汽车': '750',
                      '马自达': '92',
                      '名爵': '93',
                      'MINI': '94',
                      '玛莎拉蒂': '96',
                      '迈凯伦': '97',
                      '迈巴赫': '95',
                      '迈莎锐': '820',
                      '迈迈': '1298',
                      '迈迪汽车': '641',
                      '摩根': '98',
                      '明君汽车': '558',
                      '美亚': '99',
                      '纳智捷': '100',
                      '哪吒汽车': '713',
                      'NEVS国能汽车': '836',
                      '讴歌': '101',
                      '欧宝': '102',
                      '欧尚汽车': '637',
                      '欧拉': '635',
                      '欧朗': '103',
                      'Pgo': '679',
                      'Polestar': '716',
                      '帕加尼': '503',
                      '起亚': '104',
                      '奇瑞': '105',
                      '启辰': '106',
                      '庆铃': '107',
                      '前途汽车': '632',
                      '乔治·巴顿': '624',
                      '日产': '108',
                      '荣威': '109',
                      '瑞麒': '110',
                      '瑞驰新能源': '631',
                      '如虎': '570',
                      '斯柯达': '112',
                      '斯巴鲁': '113',
                      '斯威': '498',
                      '斯达泰克': '644',
                      '三菱': '111',
                      '上汽MAXUS': '34',
                      'Smart': '116',
                      'SERES赛力斯': '1689',
                      '双龙': '114',
                      '双环': '117',
                      '思铭': '169',
                      '思皓': '1301',
                      '陕汽通家': '501',
                      '世爵': '118',
                      '萨博': '149',
                      '赛麟': '500',
                      '速达汽车': '1715',
                      '特斯拉': '120',
                      '腾势': '166',
                      '天美汽车': '1768',
                      '天际汽车': '816',
                      '天马': '150',
                      '泰赫雅特': '119',
                      '五菱': '121',
                      '五十铃': '163',
                      '沃尔沃': '122',
                      'WEY': '544',
                      '蔚来': '571',
                      '威马汽车': '617',
                      '威麟': '123',
                      '威兹曼': '124',
                      '潍柴汽车': '1076',
                      '万丰': '652',
                      '瓦滋汽车': '616',
                      '现代': '125',
                      '雪佛兰': '126',
                      '雪铁龙': '127',
                      '夏利': '155',
                      '小鹏汽车': '717',
                      '星途': '751',
                      '新特汽车': '638',
                      '西雅特': '128',
                      '新凯': '130',
                      '新大地': '151',
                      '新雅途': '148',
                      '鑫源': '564',
                      '英菲尼迪': '132',
                      '英致': '159',
                      '一汽': '131',
                      '一汽红塔': '615',
                      '依维柯': '135',
                      '野马': '133',
                      '云度新能源': '565',
                      '永源': '134',
                      '云雀': '568',
                      '御捷新能源': '547',
                      '扬州亚星客车': '136',
                      '裕路': '563',
                      '远程汽车': '838',
                      '银隆新能源': '824',
                      '众泰': '138',
                      '中华': '137',
                      '中兴': '139',
                      '中欧': '140',
                      '中客华北': '152',
                      '中顺': '154',
                      '知豆': '168',
                      '之诺': '569'}
        for brand in brand_item.keys():
            brand_id = brand_item[brand]
            url = f'https://ssl-meta.che300.com/meta/series/series_brand{brand_id}.json'
            yield scrapy.Request(url=url, meta={'info': (brand, brand_id)})

    def parse(self, response):
        brand, brand_id = response.meta.get('info')
        family_data = json.loads(response.text)
        for i in family_data:
            family_name = i['series_name']
            family_id = i['series_id']
            url = f'https://ssl-meta.che300.com/meta/model/model_series{family_id}.json'
            yield scrapy.Request(url=url, meta={'info': (brand, brand_id, family_name, family_id)},
                                 callback=self.parse_vehicle)

    def parse_vehicle(self, response):
        item = Che300CarItem()
        brand, brand_id, family_name, family_id = response.meta.get('info')
        vehicle_data = json.loads(response.text)
        for i in vehicle_data:
            vehicle_name = i['model_name']
            vehicle_id = i['model_id']
            price = i['model_price']
            vehicle_year = i['model_year']
            min_reg_year = i['min_reg_year']
            max_reg_year = i['max_reg_year']
            # print(brand, brand_id, family_name, family_id, vehicle_name, vehicle_id, price, vehicle_year, min_reg_year,
            #       max_reg_year)
            item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['brand'] = brand
            item['brand_id'] = brand_id
            item['family_name'] = family_name
            item['family_id'] = family_id
            item['vehicle_name'] = vehicle_name
            item['vehicle_id'] = vehicle_id
            item['price'] = price
            item['vehicle_year'] = vehicle_year
            item['min_reg_year'] = min_reg_year
            item['max_reg_year'] = max_reg_year
            item['status'] = str(brand_id) + '-' + str(family_id) + '-' + str(vehicle_id) + '-' + str(
                min_reg_year) + '-' + str(max_reg_year)
            yield item
