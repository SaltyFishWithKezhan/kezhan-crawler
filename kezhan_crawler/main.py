# -*- coding: utf-8 -*-

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#execute(["scrapy", "crawl", "mooc"])
#execute(["scrapy", "crawl", "netease"])
#execute(["scrapy", "crawl", "lagou"])
execute(["scrapy", "crawl", "imooc_free"])
