# -*- coding: utf-8 -*-
import scrapy
# For Spider
from scrapy.http import Request
from urllib import parse

# For Chrome
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import time


class MoocSpider(scrapy.Spider):
    name = 'mooc'
    allowed_domains = ['www.icourse163.org']
    start_urls = ['https://www.icourse163.org/category/all']

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path="F:\DataScience\Crawler\Tools\chromedriver.exe")
        super(MoocSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # 当爬虫退出的时候关闭Chrome
        print("MoocSpider closed.")
        self.browser.quit()

    def parse(self, response):
        # mooc is a js based website, cannot use default scrapy downloader
        # loop through next pages
        while True:
            try:
                # acquire course detail infos, passing through prase_detail
                self.browser.get(response.url)
                next_btn = self.browser.find_element_by_css_selector('.ux-pager_btn.ux-pager_btn__next > a')
                course_nodes = self.browser.find_elements_by_css_selector(".u-clist.f-bg.f-cb.f-pr.j-href.ga-click")
                for course_node in course_nodes:
                    # acquire 
                    image_url = course_node.find_element_by_css_selector('img').get_attribute('src')
                    post_url = course_node.find_element_by_css_selector('a').get_attribute('href')
                    yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                                  callback=self.parse_detail)
                next_btn.click()
            except:
                break
        # next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        # if next_url:
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        print(response.url)
        pass
