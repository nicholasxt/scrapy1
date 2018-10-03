# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql
from twisted.enterprise import adbapi


class Scrapy1Pipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 爬取速度可能大于数据库存储的速度,异步操作
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handler_error, item, spider)

    def do_insert(self, cursor, item):
        sql, params = item.get_insert_sql()
        cursor.execute(sql, params)

    def handler_error(self, failure, item, spider):
        print('--------------database operation exception!!-----------------')
        print(failure)
