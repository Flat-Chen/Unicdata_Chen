import re
import time

import scrapy


class XcarDealerSpider(scrapy.Spider):
    name = 'xcar_dealer'
    allowed_domains = ['xcar.com.cn']

    # start_urls = ['http://xcar.com.cn/']
    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(XcarDealerSpider, self).__init__(**kwargs)
        self.counts = 0
        self.brand_item = {'奥迪': '1',
                           '阿尔法·罗密欧': '78',
                           '阿斯顿·马丁': '56',
                           'ARCFOX极狐': '251',
                           '北汽昌河': '28',
                           '北汽制造': '123',
                           '宝骏': '109',
                           '标致': '5',
                           '比亚迪': '27',
                           '奔腾': '105',
                           '北京': '88',
                           '宝马': '2',
                           '本田': '17',
                           '保时捷': '52',
                           '奔驰': '3',
                           'BEIJING汽车': '135',
                           '别克': '13',
                           '宝沃': '202',
                           '比速汽车': '221',
                           '北汽幻速': '179',
                           '宾利': '57',
                           '北汽新能源': '184',
                           '长安凯程': '245',
                           '长城': '30',
                           '长安欧尚': '130',
                           '长安汽车': '29',
                           '东风': '33',
                           '东风风行': '131',
                           '大众': '4',
                           '东风风神': '90',
                           '东南': '34',
                           '东风启辰': '114',
                           '东风风光': '212',
                           '东风小康': '127',
                           'DS': '124',
                           '大乘汽车': '280',
                           '福田': '76',
                           '福特': '10',
                           '福迪': '116',
                           '丰田': '18',
                           '福汽启腾': '178',
                           '法拉利': '59',
                           '广汽传祺': '103',
                           '广汽埃安': '256',
                           '观致': '119',
                           'GMC': '104',
                           '广汽蔚来': '312',
                           '黄海': '91',
                           '汉腾': '218',
                           '哈弗': '139',
                           '海马': '38',
                           '红旗': '106',
                           '华泰新能源': '219',
                           '华骐': '141',
                           '捷途': '260',
                           '金杯': '39',
                           '江淮': '44',
                           '江铃': '79',
                           '吉利': '26',
                           '金龙': '169',
                           'Jeep': '77',
                           '江铃集团新能源': '238',
                           '捷豹': '60',
                           '几何汽车': '302',
                           '捷达': '323',
                           '九龙': '171',
                           '钧天汽车': '291',
                           '开瑞': '99',
                           '凯迪拉克': '69',
                           '凯翼': '185',
                           '卡威': '183',
                           '克莱斯勒': '12',
                           '雷克萨斯': '71',
                           '猎豹汽车': '31',
                           '雷诺': '63',
                           '路虎': '65',
                           '林肯': '70',
                           '力帆': '40',
                           '领克': '226',
                           '铃木': '19',
                           '陆风': '45',
                           '劳斯莱斯': '62',
                           '兰博基尼': '61',
                           '理念': '112',
                           '零跑汽车': '254',
                           'LITE': '274',
                           '理想汽车': '255',
                           'MINI': '54',
                           '名爵': '15',
                           '马自达': '14',
                           '玛莎拉蒂': '66',
                           '迈凯伦': '126',
                           '哪吒汽车': '246',
                           '纳智捷': '113',
                           '讴歌': '72',
                           '欧拉汽车': '270',
                           '奇瑞': '25',
                           '起亚': '22',
                           '乔治·巴顿': '272',
                           '前途': '217',
                           '日产': '20',
                           '荣威': '46',
                           '上汽大通MAXUS': '134',
                           'SWM斯威汽车': '220',
                           '斯柯达': '7',
                           '三菱': '21',
                           'smart': '83',
                           '双龙': '75',
                           '斯巴鲁': '73',
                           '思皓': '269',
                           '思铭': '120',
                           '腾势汽车': '122',
                           '特斯拉': '142',
                           '五十铃': '145',
                           '潍柴汽车': '182',
                           '五菱': '82',
                           '沃尔沃': '9',
                           '威马汽车': '242',
                           '蔚来': '227',
                           'WEY': '229',
                           '新宝骏': '313',
                           '小鹏汽车': '223',
                           '现代': '23',
                           '雪佛兰': '16',
                           '星途': '288',
                           '雪铁龙': '8',
                           '依维柯': '81',
                           '一汽': '50',
                           '野马汽车': '115',
                           '英菲尼迪': '74',
                           '云度': '235',
                           '中兴汽车': '93',
                           '中华': '41',
                           '众泰': '51',
                           '知豆': '201'}

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': "192.168.1.94",
        'MYSQL_USER': "dataUser94",
        'MYSQL_PWD': "94dataUser@2020",
        'MYSQL_PORT': 3306,
        'MYSQL_DB': "network",
        'MYSQL_TABLE': "xcar_dealer",
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_PORT': 27017,
        'MONGODB_DB': 'shop_name',
        'MONGODB_COLLECTION': 'xcar_dealer',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        # 'DOWNLOAD_TIMEOUT': 5,
        # 'RETRY_ENABLED': False,
        'RETRY_TIMES': 50,
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
        province_item = {'安徽省': '24',
                         '澳门特别行政区': '51',
                         '北京市': '1',
                         '重庆市': '4',
                         '福建省': '33',
                         '贵州省': '19',
                         '广东省': '30',
                         '广西省': '31',
                         '甘肃省': '12',
                         '湖北省': '21',
                         '黑龙江省': '5',
                         '湖南省': '20',
                         '河南省': '22',
                         '海南省': '34',
                         '河北省': '8',
                         '海外': '99',
                         '吉林省': '7',
                         '江西省': '32',
                         '江苏省': '25',
                         '辽宁省': '6',
                         '内蒙古': '9',
                         '宁夏省': '13',
                         '青海省': '16',
                         '四川省': '17',
                         '陕西省': '10',
                         '上海市': '2',
                         '山东省': '23',
                         '山西省': '11',
                         '台湾省': '52',
                         '天津市': '3',
                         '西藏省': '15',
                         '香港特别行政区': '50',
                         '新疆省': '14',
                         '云南省': '18',
                         '浙江省': '26'}
        for province in province_item.keys():
            province_id = province_item[province]
            url = f'https://dealer.xcar.com.cn/dealerdp_index.php?r=dealers/Ajax/selectCity&province_id={province_id}&pbid=0'
            yield scrapy.Request(url=url, meta={'info': (province, province_id)})

    def parse(self, response):
        province, province_id = response.meta.get('info')
        # print(response.text)
        citys = re.findall(r'<li id="(.*?)" class="">', response.text)
        city_item = {}
        for i in citys:
            city_item[i.split('" name="')[1]] = i.split('" name="')[0]
        # print(city_item)
        for city in city_item.keys():
            city_id = city_item[city]
            for brand in self.brand_item.keys():
                brand_id = self.brand_item[brand]
                url = f'https://dealer.xcar.com.cn/{city_id}/{brand_id}.htm'
                yield scrapy.Request(url=url, meta={'info': (province, province_id, city, city_id, brand, brand_id)},
                                     callback=self.parse_dealer)

    def parse_dealer(self, response):
        item = {}
        province, province_id, city, city_id, brand, brand_id = response.meta.get('info')
        # 翻页
        next_url = response.xpath('//a[@class="page_down"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),
                                 meta={'info': (province, province_id, city, city_id, brand, brand_id)},
                                 callback=self.parse_dealer)

        # 4S店
        lis1 = response.xpath('//div[@id="dlists_4s_isfee"]/ul[@class="dlists_list"]/li')
        for li in lis1:
            item['grantime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['province'] = province
            item['city'] = city
            item['shopname'] = li.xpath('./dl/dt/a/@title').extract_first()
            item['tel'] = ''.join(li.xpath('.//dd[@class="phone"]/em/b//text()').getall()).replace('同意用户协议查看电话', '') \
                .replace('查看用户协议', '').replace('\n', '').replace('\t', '').replace(' ', '').replace('>', '')
            item['shoptype'] = '4S'
            item['mainbrand'] = brand
            item['location'] = li.xpath('.//dd[@class="site"]/span[2]/@title').extract_first()
            item['salesregions'] = li.xpath('.//dd[@class="promotion"]/a/@title').extract_first()
            item['url'] = response.urljoin(li.xpath('./dl/dt/a/@href').extract_first())
            item['status'] = item['shopname'] + '-' + item['location'] + '-' + item['tel'] + '-' + item[
                'shoptype'] + '-' + item['mainbrand']
            yield item
        # 综合店
        lis2 = response.xpath('//div[@id="dlists_zh"]/ul[@class="dlists_list"]/li')
        for li in lis2:
            item['grantime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['province'] = province
            item['city'] = city
            item['shopname'] = li.xpath('./dl/dt/a/@title').extract_first()
            item['tel'] = ''.join(li.xpath('.//dd[@class="phone"]/em/b//text()').getall()).replace('同意用户协议查看电话', '') \
                .replace('查看用户协议', '').replace('\n', '').replace('\t', '').replace(' ', '').replace('>', '')
            item['shoptype'] = '综合店'
            item['mainbrand'] = brand
            item['location'] = li.xpath('.//dd[@class="site"]/span[2]/@title').extract_first()
            item['salesregions'] = li.xpath('.//dd[@class="promotion"]/a/@title').extract_first()
            item['url'] = response.urljoin(li.xpath('./dl/dt/a/@href').extract_first())
            item['status'] = item['shopname'] + '-' + item['location'] + '-' + item['tel'] + '-' + item[
                'shoptype'] + '-' + item['mainbrand']
            yield item
