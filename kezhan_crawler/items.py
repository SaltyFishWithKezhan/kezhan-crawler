# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags


class KezhanCrawlerItem(scrapy.Item):
    pass


class MoocCourseItem(scrapy.Item):
    title = scrapy.Field()
    school = scrapy.Field()
    instructors = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    description = scrapy.Field()
    attend_count = scrapy.Field()
    comment_count = scrapy.Field()
    rating = scrapy.Field()
    is_national = scrapy.Field()
    labels = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            replace into kz_dm.mooc_course(title, school, instructors, create_date, url, url_object_id, front_image_url, front_image_path, description, attend_count, comment_count, rating, is_national, labels)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        params = (
            self["title"], self['school'], self['instructors'], self["create_date"], self["url"],
            self['url_object_id'],
            self['front_image_url'][0], self['front_image_path'], self['description'], self['attend_count'],
            self['comment_count'],
            self['rating'], self['is_national'], self['labels'])
        return insert_sql, params


class NetEaseCourseItem(scrapy.Item):
    title = scrapy.Field()
    school = scrapy.Field()
    for_desc = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    description = scrapy.Field()
    attend_count = scrapy.Field()
    comment_count = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    labels = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            replace into kz_dm.netease_course(title, school, for_desc, create_date, url, url_object_id, front_image_url, front_image_path, description, attend_count, comment_count, rating, price, labels)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        params = (
            self["title"], self['school'], self['for_desc'], self["create_date"], self["url"],
            self['url_object_id'],
            self['front_image_url'][0], self['front_image_path'], self['description'], self['attend_count'],
            self['comment_count'],
            self['rating'], self['price'], self['labels'])
        return insert_sql, params


def replace_splash(value):
    return value.replace("/", "")


def handle_strip(value):
    return value.strip()


def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    return "".join(addr_list)


class LagouJobItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    # 拉勾网职位
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(replace_splash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(replace_splash),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(replace_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor=MapCompose(handle_strip),
    )
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    company_name = scrapy.Field(
        input_processor=MapCompose(handle_strip),
    )
    company_url = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            replace into kz_dm.lagou_job(title, url, url_object_id, salary, job_city, work_years, degree_need,
            job_type, publish_time, job_advantage, job_desc, job_addr, company_url, company_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            self["title"], self["url"], self['url_object_id'], self["salary"], self["job_city"], self["work_years"],
            self["degree_need"],
            self["job_type"], self["publish_time"], self["job_advantage"], self["job_desc"], self["job_addr"],
            self["company_url"], self["company_name"])

        return insert_sql, params


class ImoocFreeItem(scrapy.Item):
    title = scrapy.Field()
    target = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    description = scrapy.Field()
    attend_count = scrapy.Field()
    rating = scrapy.Field()
    labels = scrapy.Field()
    difficulty = scrapy.Field()
    tutor = scrapy.Field()
    pre_request = scrapy.Field()
    time_length = scrapy.Field()
    comment_count = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                replace into kz_dm.imooc_free(title, url, url_object_id, front_image_url, front_image_path, labels, difficulty, attend_count, time_length, rating, tutor, target, pre_request, description, comment_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

        params = (self['title'], self['url'], self['url_object_id'], self['front_image_url'], self['front_image_path'],
                  self['labels'], self['difficulty'], ['attend_count'], self['time_length'], self['rating'], self['tutor'],
                  self['target'], self['pre_request'], self['description'], self['comment_count'])
        return insert_sql, params
