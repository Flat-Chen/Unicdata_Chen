import re
import time

import scrapy


class PcautoDealerSpider(scrapy.Spider):
    name = 'pcauto_dealer'
    allowed_domains = ['pcauto.com.cn']

    # start_urls = ['http://pcauto.com.cn/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(PcautoDealerSpider, self).__init__(**kwargs)
        self.counts = 0
        self.province_item = {'北京': 'c2',
                              '上海': 'c3',
                              '重庆': 'c77',
                              '天津': 'p20',
                              '安徽': 'p28',
                              '福建': 'p3',
                              '甘肃': 'p25',
                              '贵州': 'p26',
                              '广东': 'p5',
                              '广西': 'p23',
                              '河南': 'p22',
                              '黑龙江': 'p15',
                              '湖南': 'p10',
                              '海南': 'p18',
                              '湖北': 'p4',
                              '河北': 'p11',
                              '吉林': 'p24',
                              '江苏': 'p1',
                              '江西': 'p16',
                              '辽宁': 'p2',
                              '内蒙古': 'p27',
                              '宁夏': 'p30',
                              '青海': 'p31',
                              '山东': 'p13',
                              '四川': 'p12',
                              '山西': 'p21',
                              '陕西': 'p8',
                              '新疆': 'p17',
                              '西藏': 'p29',
                              '云南': 'p9',
                              '浙江': 'p19'}
        # self.brand_item = {'AC Schnitzer': 'nb693',
        #                    'APEX': 'nb8083',
        #                    '艾康尼克': 'nb7261',
        #                    '爱驰': 'nb7541',
        #                    'ALPINA': 'nb7230',
        #                    'ARCFOX极狐': 'nb7342',
        #                    '阿尔法·罗密欧': 'nb60',
        #                    '阿斯顿·马丁': 'nb62',
        #                    '奥迪': 'nb1',
        #                    '北汽制造': 'nb122',
        #                    '奔腾': 'nb306',
        #                    '北汽威旺': 'nb643',
        #                    '巴博斯': 'nb723',
        #                    '北汽幻速': 'nb898',
        #                    '宝骏': 'nb582',
        #                    '北京': 'nb593',
        #                    '比亚迪': 'nb107',
        #                    'BEIJING汽车': 'nb814',
        #                    '北汽新能源': 'nb950',
        #                    '北京清行': 'nb7602',
        #                    '比德文汽车': 'nb7912',
        #                    '宝腾': 'nb7922',
        #                    '宝沃': 'nb1126',
        #                    '比速汽车': 'nb7190',
        #                    '北汽道达': 'nb7311',
        #                    '标致': 'nb41',
        #                    '保时捷': 'nb44',
        #                    '宾利': 'nb45',
        #                    '布加迪': 'nb63',
        #                    '本田': 'nb3',
        #                    '奔驰': 'nb4',
        #                    '别克': 'nb7',
        #                    '宝马': 'nb20',
        #                    '长安汽车': 'nb124',
        #                    '长安欧尚': 'nb613',
        #                    '长城': 'nb110',
        #                    '成功': 'nb990',
        #                    '长安跨越': 'nb7692',
        #                    '长安凯程': 'nb7301',
        #                    '长江EV': 'nb7321',
        #                    '昌河': 'nb75',
        #                    '大迪': 'nb235',
        #                    '东风启辰': 'nb633',
        #                    'DS': 'nb754',
        #                    '东风风神': 'nb581',
        #                    '东风': 'nb111',
        #                    '东风小康': 'nb856',
        #                    '东风风行': 'nb949',
        #                    '大乘汽车': 'nb7691',
        #                    '东风富康': 'nb7741',
        #                    '东风风度': 'nb877',
        #                    '东风风光': 'nb1139',
        #                    '东风风诺': 'nb1190',
        #                    '电咖': 'nb7401',
        #                    '东风瑞泰特': 'nb7562',
        #                    '道奇': 'nb72',
        #                    '大众': 'nb2',
        #                    '东南': 'nb16',
        #                    '福迪': 'nb116',
        #                    '福汽启腾': 'nb878',
        #                    '法拉利': 'nb61',
        #                    '福田': 'nb103',
        #                    '枫叶汽车': 'nb8113',
        #                    '丰田': 'nb10',
        #                    '菲亚特': 'nb18',
        #                    '福特': 'nb21',
        #                    '广汽吉奥': 'nb195',
        #                    'GMC': 'nb265',
        #                    '光冈': 'nb567',
        #                    '广汽传祺': 'nb571',
        #                    '广汽蔚来': 'nb7901',
        #                    '观致': 'nb824',
        #                    '广汽集团': 'nb7711',
        #                    '格罗夫': 'nb7841',
        #                    '国金汽车': 'nb7351',
        #                    '广汽新能源': 'nb7471',
        #                    '黄海': 'nb133',
        #                    '红旗': 'nb396',
        #                    '海马郑州': 'nb583',
        #                    '华泰': 'nb115',
        #                    '哈弗': 'nb845',
        #                    '恒天': 'nb855',
        #                    '海格': 'nb876',
        #                    '华颂': 'nb1001',
        #                    '红星': 'nb7621',
        #                    '华泰新能源': 'nb1149',
        #                    '汉腾': 'nb1180',
        #                    '海马新能源': 'nb7291',
        #                    '华骐': 'nb7331',
        #                    '悍马': 'nb59',
        #                    '华普': 'nb81',
        #                    '哈飞': 'nb82',
        #                    '海马': 'nb8',
        #                    '金龙汽车': 'nb355',
        #                    '九龙': 'nb568',
        #                    '钧天汽车': 'nb7781',
        #                    '捷达': 'nb7791',
        #                    '几何汽车': 'nb7861',
        #                    '捷尼赛思': 'nb7952',
        #                    '捷途': 'nb7501',
        #                    '江铃集团新能源': 'nb7260',
        #                    '君马汽车': 'nb7322',
        #                    '吉利汽车': 'nb13',
        #                    '金旅': 'nb114',
        #                    '江淮': 'nb78',
        #                    '金杯': 'nb83',
        #                    '江铃': 'nb101',
        #                    '捷豹': 'nb26',
        #                    'Jeep': 'nb38',
        #                    '科尼赛克': 'nb570',
        #                    '卡升': 'nb704',
        #                    '开瑞': 'nb578',
        #                    '凯翼': 'nb970',
        #                    '卡威汽车': 'nb1012',
        #                    '凯马': 'nb1075',
        #                    '康迪': 'nb1095',
        #                    'KTM': 'nb888',
        #                    '凯迪拉克': 'nb70',
        #                    '克莱斯勒': 'nb39',
        #                    '力帆': 'nb305',
        #                    '陆风': 'nb569',
        #                    '理念': 'nb604',
        #                    '路特斯': 'nb653',
        #                    'Lorinser': 'nb663',
        #                    '雷丁': 'nb1022',
        #                    'LITE': 'nb7611',
        #                    '领途': 'nb7701',
        #                    '理想汽车': 'nb7721',
        #                    '陆地方舟': 'nb939',
        #                    '领志': 'nb1011',
        #                    '领克': 'nb7220',
        #                    '雷诺': 'nb40',
        #                    '莲花': 'nb46',
        #                    '劳斯莱斯': 'nb47',
        #                    '猎豹汽车': 'nb58',
        #                    '兰博基尼': 'nb64',
        #                    '林肯': 'nb66',
        #                    '铃木': 'nb73',
        #                    '路虎': 'nb29',
        #                    '雷克萨斯': 'nb30',
        #                    'MINI': 'nb205',
        #                    '玛莎拉蒂': 'nb316',
        #                    'MG名爵': 'nb345',
        #                    '迈巴赫': 'nb387',
        #                    '迈凯伦': 'nb715',
        #                    '迈莎锐': 'nb8003',
        #                    '明君华凯': 'nb1106',
        #                    '摩根': 'nb908',
        #                    '马自达': 'nb17',
        #                    '纳智捷': 'nb623',
        #                    '哪吒汽车': 'nb7651',
        #                    'NEVS国能汽车': 'nb7731',
        #                    '南京金龙': 'nb1053',
        #                    '讴歌': 'nb140',
        #                    '欧朗': 'nb703',
        #                    '欧睿': 'nb1116',
        #                    '欧拉': 'nb7553',
        #                    '欧宝': 'nb22',
        #                    '帕加尼': 'nb573',
        #                    'Polestar极星': 'nb7381',
        #                    '庆铃汽车': 'nb121',
        #                    '前途': 'nb1074',
        #                    '骐铃汽车': 'nb1136',
        #                    '乔治·巴顿': 'nb7581',
        #                    '奇瑞': 'nb57',
        #                    '起亚': 'nb12',
        #                    '荣威': 'nb365',
        #                    '瑞麒': 'nb580',
        #                    '容大智造': 'nb7631',
        #                    '日产': 'nb15',
        #                    'R汽车': 'nb8223',
        #                    '世爵': 'nb546',
        #                    'smart': 'nb603',
        #                    '上汽大通MAXUS': 'nb673',
        #                    '思铭': 'nb733',
        #                    '双环': 'nb119',
        #                    '斯达泰克': 'nb1137',
        #                    'SWM斯威汽车': 'nb7200',
        #                    '思皓': 'nb7552',
        #                    '赛麟': 'nb980',
        #                    '斯巴鲁': 'nb49',
        #                    '双龙': 'nb53',
        #                    '斯柯达': 'nb69',
        #                    '萨博': 'nb23',
        #                    '三菱': 'nb32',
        #                    '腾势': 'nb743',
        #                    '特斯拉': 'nb774',
        #                    '泰卡特': 'nb969',
        #                    '天际': 'nb7661',
        #                    '威兹曼': 'nb753',
        #                    '威麟': 'nb579',
        #                    '五菱': 'nb118',
        #                    '威马汽车': 'nb7441',
        #                    '五十铃': 'nb918',
        #                    'WEY': 'nb7240',
        #                    '蔚来': 'nb7250',
        #                    '沃尔沃': 'nb24',
        #                    '雪佛兰': 'nb225',
        #                    '星途': 'nb7751',
        #                    '新宝骏': 'nb7963',
        #                    '新凯': 'nb7461',
        #                    '小鹏汽车': 'nb7210',
        #                    '星驰': 'nb7361',
        #                    '雪铁龙': 'nb6',
        #                    '现代': 'nb34',
        #                    '依维柯': 'nb132',
        #                    '永源': 'nb275',
        #                    '野马汽车': 'nb516',
        #                    '云度新能源': 'nb7271',
        #                    '云雀汽车': 'nb7491',
        #                    '裕路': 'nb7371',
        #                    '驭胜': 'nb7511',
        #                    '一汽': 'nb9',
        #                    '英菲尼迪': 'nb28',
        #                    '中兴': 'nb125',
        #                    '众泰': 'nb307',
        #                    '中欧': 'nb506',
        #                    '中华': 'nb104',
        #                    '之诺': 'nb866',
        #                    '知豆': 'nb929'}

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': "192.168.1.94",
        'MYSQL_USER': "dataUser94",
        'MYSQL_PWD': "94dataUser@2020",
        'MYSQL_PORT': 3306,
        'MYSQL_DB': "network",
        'MYSQL_TABLE': "pcauto_dealer",
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'shop_name',
        'MONGODB_COLLECTION': 'pcauto_dealer',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOAD_TIMEOUT': 5,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 15,
        # 'COOKIES_ENABLED': True,
        # 'REDIS_URL': 'redis://192.168.1.241:6379/14',
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'dealer.middlewares.DealerProxyMiddleware': 400,
        #     'dealer.middlewares.DealerUserAgentMiddleware': 100,
        # },
        # 'ITEM_PIPELINES': {
        'dealer.pipelines.DealerPipeline': 300,
        #     'dealer.pipelines.RenameTable': 299
        # },
    }

    def start_requests(self):
        for province in self.province_item.keys():
            province_id = self.province_item[province]
            url = f'https://price.pcauto.com.cn/shangjia/{province_id}/'
            yield scrapy.Request(url=url, meta={'info': (province, province_id)})

    def parse(self, response):
        province, province_id = response.meta.get('info')
        lis = response.xpath('//li[@class="liFc"]')
        for li in lis:
            shop_url = li.xpath('.//div[@class="divYSd"]/p[1]/a/@href').extract_first()
            city = li.xpath('.//span[@class="smoke"]/text()').extract_first()
            shopname = li.xpath('.//div[@class="divYSd"]/p[1]/a/@title').extract_first()
            mainbrand = li.xpath('.//p[@class="tel"][2]/span[2]/text()').extract_first()
            yield scrapy.Request(url=response.urljoin(shop_url), callback=self.shop_parse,
                                 meta={'info': (province, city, shopname, mainbrand)})
        next_url = response.xpath('//div[@class="pcauto_page"]/a[@class="next"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse,
                                 meta={'info': (province, province_id)})

    def shop_parse(self, response):
        item = {}
        province, city, shopname, mainbrand = response.meta.get('info')
        shoptype = response.xpath('//i[@class="tag tag-blue"]/text()').extract_first()
        if shoptype is None:
            shoptype = response.xpath('//p[@class="tit"]/i/text()').extract_first()
        tel = response.xpath('//div[@class="otlisttl otlisttlyh"]/i/text()').extract_first()
        try:
            location = re.findall(r'，地址：(.*?)"/>', response.text)[0]
        except:
            location = response.xpath('//div[@class="modeali"]/text()').extract_first()
        if location is None:
            location = response.xpath('//p[@class="address"]/@title').extract_first()
        # print(province, city, shopname, mainbrand, shoptype, tel, location)
        item['grantime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['province'] = province
        item['city'] = city
        item['shopname'] = shopname
        item['shoptype'] = shoptype
        item['mainbrand'] = mainbrand
        item['tel'] = tel
        item['location'] = location
        item['url'] = response.url
        yield item
