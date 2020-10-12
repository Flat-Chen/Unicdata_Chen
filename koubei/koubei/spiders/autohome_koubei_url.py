import scrapy


class AutohomeKoubeiUrlSpider(scrapy.Spider):
    name = 'autohome_koubei_url'
    allowed_domains = ['autohome.com.cn']
    car_list = [
        '途观L新能源', "探岳GTE插电混动", "唐新能源", "宋Pro新能源", "荣威RX5新能源", "宝马X1新能源",
        "帕萨特新能源", "迈腾", "雷凌双擎E+", "汉", "雅阁", "凯美瑞",
    ]
    start_urls = ["https://k.autohome.com.cn/4746/",
                  "https://k.autohome.com.cn/5061/",
                  "https://k.autohome.com.cn/3430/",
                  "https://k.autohome.com.cn/5279/",
                  "https://k.autohome.com.cn/4240/",
                  "https://k.autohome.com.cn/4356/",
                  "https://k.autohome.com.cn/4904/",
                  "https://k.autohome.com.cn/496/",
                  "https://k.autohome.com.cn/4837/",
                  "https://k.autohome.com.cn/5499/",
                  "https://k.autohome.com.cn/78/",
                  "https://k.autohome.com.cn/110/"]

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeKoubeiUrlSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'residual_value',
        'MYSQL_TABLE': 'autohome_gz',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'dasouche',
        'MONGODB_COLLECTION': 'dasouche_url',
        'CrawlCar_Num': 8000000,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'COOKIES_ENABLED': True,
        'ITEM_PIPELINES': {
            'koubei.pipelines.MasterPipeline': 300,
        }
    }

    def parse(self, response):
        item = {}
        next_page_url = response.xpath("//div[@class='page']/a[contains(text(),'下一页')]/@href").extract_first()
        print("-" * 20, next_page_url, "-" * 20)
        if next_page_url == None:
            return
        else:
            yield response.follow(url=next_page_url, callback=self.parse)
        # 解析时间
        koubei_list = response.xpath("//div[@class='mouthcon']")
        for koubei in koubei_list:
            url = "https:" + koubei.xpath('.//a[contains(text(),"查看全部内容")]/@href').extract_first()
            item['url'] = url
            yield item
