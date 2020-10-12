from scrapy.cmdline import execute

import sys
import os

website = 'jzg_price_sh_master'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])