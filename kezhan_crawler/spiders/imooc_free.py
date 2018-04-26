# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse

from kezhan_crawler.items import ImoocFreeItem
from kezhan_crawler.utils.common import get_md5


class ImoocFreeSpider(scrapy.Spider):
    name = 'imooc_free'
    allowed_domains = ['www.imooc.com']
    start_urls = ['https://www.imooc.com/course/list/']

    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
    }

    def parse(self, response):

        course_nodes = response.css(".course-card-container")
        for course_node in course_nodes:
            image_url = course_node.css('::attr(src)').extract()[0]
            image_url = 'http:' + image_url
            course_url = course_node.css('::attr(href)').extract()[0]
            attend_count = course_node.css('div > div > span:nth-child(2)::text').extract()[0]
            labels = course_node.css('label::text').extract()
            course_label = ''
            for label in labels:
                course_label = label + ','
            yield Request(url=parse.urljoin(response.url, course_url), meta={"front_image_url": [image_url],
                                                                             'attend_count': attend_count,
                                                                             'labels': course_label},
                          callback=self.parse_detail)

        next_url = response.css(
            '#main > div.container > div.course-list > div.page > a:nth-child(10)::attr(href)').extract_first('')
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        course_item = ImoocFreeItem()
        course_item['front_image_url'] = response.meta.get('front_image_url', '')
        course_item['attend_count'] = response.meta.get('attend_count', '')
        course_item['labels'] = response.meta.get('labels')
        course_item['url'] = response.url
        course_item['url_object_id'] = get_md5(response.url)
        course_item['title'] = \
            response.css('#main > div.course-infos > div.w.pr > div.hd.clearfix > h2::text').extract()[0]
        course_item['tutor'] = response.css(
            '#main > div.course-infos > div.w.pr > div.statics.clearfix > div.teacher-info.l > span.tit > a::text').extract()[
            0]
        course_item['rating'] = response.css('#main > div.course-infos > div.w.pr > div.statics.clearfix > div.static-item.l.score-btn > span.meta-value::text').extract()[0]
        course_item['difficulty'] = response.css('#main > div.course-infos > div.w.pr > div.statics.clearfix > div:nth-child(2) > span.meta-value::text').extract()[0]
        course_item['description'] =response.css('#main > div.course-info-main.clearfix.w > div.content-wrap.clearfix > div.content > div.course-description.course-wrap::text').extract()[0]
        course_item['pre_request'] = response.css('#main > div.course-info-main.clearfix.w > div.content-wrap.clearfix > div.aside.r > div.course-wrap.course-aside-info.js-usercard-box > div.course-info-tip > dl.first > dd::text').extract()[0]
        course_item['target'] = response.css('#main > div.course-info-main.clearfix.w > div.content-wrap.clearfix > div.aside.r > div.course-wrap.course-aside-info.js-usercard-box > div.course-info-tip > dl:nth-child(2) > dd::text').extract()[0]
        course_item['time_length'] =response.css('#main > div.course-infos > div.w.pr > div.statics.clearfix > div:nth-child(3) > span.meta-value::text').extract()[0]
        raw_comment_count = response.css('#main > div.course-info-menu > div > ul > li:nth-child(4) > span::text').extract_first('')
        if raw_comment_count:
            comment_count = raw_comment_count
        else:
            comment_count = 0
        course_item['comment_count'] = comment_count
        yield course_item
