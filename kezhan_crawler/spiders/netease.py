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

from kezhan_crawler.items import NetEaseCourseItem
from kezhan_crawler.utils.common import get_md5


class NeteaseSpider(scrapy.Spider):
    name = 'netease'
    allowed_domains = ['study.163.com']
    start_urls = ['http://study.163.com/courses']

    def __init__(self):
        # disable loading pics
        chrome_opt = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_opt.add_experimental_option('prefs', prefs)
        self.browser = webdriver.Chrome(executable_path="F:\DataScience\Crawler\Tools\chromedriver.exe",
                                        chrome_options=chrome_opt)
        super(NeteaseSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # 当爬虫退出的时候关闭Chrome
        print("NeteaseSpider closed.")
        self.browser.quit()

    def parse(self, response):
        # mooc is a js based website, cannot use default scrapy downloader
        # loop through next pages
        self.browser.get(response.url)

        # acquire all course links thumbnial urls
        courses_links = []
        debug_num = 2
        while debug_num > 0:
            try:
                # acquire course detail infos, passing through prase_detail
                time.sleep(1.5)
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                next_btn = self.browser.find_element_by_css_selector(
                    '.ux-pager_btn.ux-pager_btn__next > a:not(.th-bk-disable-gh)')

                course_nodes = self.browser.find_elements_by_css_selector(".uc-course-list_itm.f-ib")

                for course_node in course_nodes:
                    tmp_urls = {'course_url': course_node.find_element_by_css_selector('a').get_attribute('href'),
                                'front_image_url': course_node.find_element_by_css_selector('img').get_attribute('src'),
                                'title': course_node.find_element_by_css_selector('.uc-ykt-coursecard-wrap_tit').text,
                                'school': course_node.find_element_by_css_selector('.uc-ykt-coursecard-wrap_orgName.f-fs0.f-thide').text,
                                'rating': course_node.find_element_by_css_selector('.uc-starrating_score').text,
                                'attend_count': course_node.find_element_by_css_selector('.m-hot.f-fl').text,
                                'price': course_node.find_element_by_css_selector('.uc-ykt-coursecard-wrap_price.f-pa').text
                                }
                    courses_links.append(tmp_urls)

                debug_num = debug_num - 1
                next_btn.click()
            except:
                break

        import json
        print(len(courses_links))
        with open('netease_course_links.json', 'w') as outfile:
            json.dump(courses_links, outfile)

        # each course
        for course_link in courses_links:
            course_url = parse.urljoin(response.url, course_link['course_url'])

            # going to detail page
            self.browser.get(course_url)
            time.sleep(2)

            course_desc = self.browser.find_elements_by_css_selector('div.cintrocon.j-courseintro')
            if len(course_desc) > 0:
                course_desc = course_desc[0].text
            else:
                course_desc = 'Unknown'

            for_desc = self.browser.find_elements_by_css_selector('p.j-targetuser.cintrocon')
            if len(for_desc) > 0:
                for_desc = for_desc[0].text
            else:
                for_desc = 'Unknown'

            raw_comment_count = self.browser.find_elements_by_css_selector('span.cmt')
            if len(raw_comment_count) > 0:
                comment_count = raw_comment_count[0].text
                re_ret = re.match('.*\((.*)\).*', comment_count)
                if re_ret:
                    comment_count = re_ret.group(1)
                else:
                    comment_count = -1
            else:
                comment_count = -1

            raw_labels = self.browser.find_elements_by_css_selector('.navcrumb-item')
            labels = ''
            for raw_label in raw_labels[1:-1]:
                labels = labels + raw_label.text + ','

            raw_attend_count = course_link['attend_count']
            re_ret = re.match('\((\d*).*\)', raw_attend_count)
            if re_ret:
                attend_count = re_ret.group(1)
            else:
                attend_count = 0

            # load item
            course_item = NetEaseCourseItem()
            course_item['title'] = course_link['title']
            course_item['school'] = course_link['school']
            course_item['for_desc'] = for_desc
            course_item['url'] = course_url
            course_item['url_object_id'] = get_md5(course_url)
            course_item['create_date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            course_item['front_image_url'] = [course_link['front_image_url']]
            course_item['description'] = course_desc
            course_item['attend_count'] = attend_count
            course_item['comment_count'] = comment_count
            course_item['rating'] = course_link['rating']
            course_item['price'] = course_link['price']
            course_item['labels'] = labels

            yield course_item
