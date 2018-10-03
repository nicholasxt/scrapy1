# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    type = scrapy.Field()
    number = scrapy.Field()
    location = scrapy.Field()
    time = scrapy.Field()

    def get_insert_sql(self):
        sql = "insert into tencentJob(name,link,type,number,location,time) values(%s,%s,%s,%s,%s,%s)"
        params = (self['name'], self['link'], self['type'], self['number'], self['location'], self['time'])
        return sql,params


