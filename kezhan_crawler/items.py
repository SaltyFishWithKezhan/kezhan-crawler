# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re


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
    comment_count = scrapy.Field()
    rating = scrapy.Field()
    is_national = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            replace into kz_dm.mooc_course(title, school, instructors, create_date, url, url_object_id, front_image_url, front_image_path, description, comment_count, rating, is_national)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        if self["front_image_url"]:
            params = (
                self["title"], self['school'], self['instructors'], self["create_date"], self["url"],
                self['url_object_id'],
                self['front_image_url'], self['front_image_path'], self['description'], self['comment_count'],
                self['rating'], self['is_national'])
        return insert_sql, params
