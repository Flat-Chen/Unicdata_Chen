from scrapy.cmdline import execute

import sys
import os

website = 'che300_21price_sh'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])
