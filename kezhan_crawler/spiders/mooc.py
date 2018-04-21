# -*- coding: utf-8 -*-
import scrapy
# For Spider
from scrapy.http import Request
from urllib import parse
import re

# For Chrome
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import time
from kezhan_crawler.utils.common import get_md5

from kezhan_crawler.items import MoocCourseItem


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
        # # mooc is a js based website, cannot use default scrapy downloader
        # # loop through next pages
        # self.browser.get(response.url)
        # # acquire all course links
        # courses_links = []
        # while True:
        #     try:
        #         # acquire course detail infos, passing through prase_detail
        #         time.sleep(1)
        #         next_btn = self.browser.find_element_by_css_selector('.ux-pager_btn.ux-pager_btn__next:not(.z-dis)')
        #         course_nodes = self.browser.find_elements_by_css_selector(".u-clist.f-bg.f-cb.f-pr.j-href.ga-click")
        #         for course_node in course_nodes:
        #             courses_links.append(course_node.find_element_by_css_selector('a').get_attribute('href'))
        #         next_btn.click()
        #     except:
        #         break
        # print(len(courses_links))
        # print(courses_links)

        for course_link in courses_links:
            course_url = parse.urljoin(response.url, course_link)

            # going to detail page
            self.browser.get(course_url)
            time.sleep(2)

            # parse detail page
            course_desc = self.browser.find_elements_by_css_selector('#j-rectxt2')
            if (len(course_desc) > 0):
                course_desc = course_desc[0].text
            else:
                course_desc = 'Unknown'

            # going to comment page
            comment_btn = self.browser.find_element_by_css_selector('#review-tag-button')
            comment_btn.click()
            time.sleep(2)

            # parse comment page
            raw_comment_count = self.browser.find_elements_by_css_selector('#review-tag-num')
            re_ret = re.match('.*\((\d*)\).*', raw_comment_count[0].text)
            if re_ret:
                comment_count = re_ret.group(1)
            else:
                comment_count = 0

            rating = self.browser.find_elements_by_css_selector(
                '.ux-mooc-comment-course-comment_head_rating-scores > span')
            if (len(rating) > 0):
                rating = rating[0].text
            else:
                rating = -1

            # load item
            course_item = MoocCourseItem()
            course_item['url'] = course_url
            course_item['url_object_id'] = get_md5(course_url)
            course_item['create_date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            # course_item['front_image_url'] = [image_url]
            course_item['description'] = course_desc
            course_item['comment_count'] = comment_count
            course_item['rating'] = rating
            course_item['is_national'] = 0;

            # yield course_item

        next_btn.click()
