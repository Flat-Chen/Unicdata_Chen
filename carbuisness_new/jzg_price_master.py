from scrapy.cmdline import execute

import sys
import os

website = 'jzg_price_master'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])