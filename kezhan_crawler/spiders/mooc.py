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
        # disable loading pics
        chrome_opt = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_opt.add_experimental_option('prefs', prefs)
        self.browser = webdriver.Chrome(executable_path="F:\DataScience\Crawler\Tools\chromedriver.exe",
                                        chrome_options=chrome_opt)
        super(MoocSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # 当爬虫退出的时候关闭Chrome
        print("MoocSpider closed.")
        self.browser.quit()

    def parse(self, response):
        # mooc is a js based website, cannot use default scrapy downloader
        # loop through next pages
        self.browser.get(response.url)

        # acquire all course links thumbnial urls
        courses_links = []
        debug_num = 23333333333
        while debug_num > 0:
            try:
                # acquire course detail infos, passing through prase_detail
                time.sleep(2)
                next_btn = self.browser.find_element_by_css_selector('.ux-pager_btn.ux-pager_btn__next:not(.z-dis)')
                course_nodes = self.browser.find_elements_by_css_selector(".u-clist.f-bg.f-cb.f-pr.j-href.ga-click")
                for course_node in course_nodes:
                    tmp_urls = [course_node.find_element_by_css_selector('a').get_attribute('href'),
                                course_node.find_element_by_css_selector('img').get_attribute('src')]
                    courses_links.append(tmp_urls)
                next_btn.click()
                debug_num = debug_num - 1
            except:
                break
        print(len(courses_links))
        print(courses_links)

        # each course
        for course_link in courses_links:
            course_url = parse.urljoin(response.url, course_link[0])

            # going to detail page
            self.browser.get(course_url)
            time.sleep(2)

            # parse detail page, break when url errors occure
            raw_course_title = self.browser.find_elements_by_css_selector('.course-title.f-ib.f-vam')
            if (len(raw_course_title) > 0):
                course_title = raw_course_title.text;
            else:
                continue

            course_school = self.browser.find_element_by_css_selector('.m-teachers_school-img.f-ib').get_attribute(
                'data-label')

            raw_course_instructors = self.browser.find_elements_by_css_selector('.u-tchcard.f-cb')
            course_instructor = ''
            for raw_course_instructor in raw_course_instructors:
                course_instructor = course_instructor + ',' + raw_course_instructor.text

            course_desc = self.browser.find_elements_by_css_selector('#j-rectxt2')
            if (len(course_desc) > 0):
                course_desc = course_desc[0].text
            else:
                course_desc = 'Unknown'

            attend_count = self.browser.find_element_by_css_selector(
                '.course-enroll-info_course-enroll_price-enroll_enroll-count')
            re_ret = re.match('.*?(\d+).*', attend_count.text)
            if re_ret:
                attend_count = re_ret.group(1)
            else:
                attend_count = 0

            raw_is_national = self.browser.find_elements_by_css_selector('#j-tag')
            if (len(raw_is_national) > 0):
                is_national = 1
            else:
                is_national = 0

            labels = ''
            raw_labels = self.browser.find_elements_by_css_selector('span.breadcrumb_item')
            for raw_label in raw_labels:
                labels = labels + raw_label.text + ','

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
            course_item['title'] = course_title
            course_item['school'] = course_school
            course_item['instructors'] = course_instructor
            course_item['url'] = course_url
            course_item['url_object_id'] = get_md5(course_url)
            course_item['create_date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            course_item['front_image_url'] = [course_link[1]]
            course_item['description'] = course_desc
            course_item['attend_count'] = attend_count
            course_item['comment_count'] = comment_count
            course_item['rating'] = rating
            course_item['is_national'] = is_national
            course_item['labels'] = labels

            yield course_item
