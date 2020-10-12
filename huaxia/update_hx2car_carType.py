from scrapy.cmdline import execute

import sys
import os

website = 'update_hx2car_carType'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])
