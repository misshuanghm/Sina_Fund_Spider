# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

from sina_fund_spider.items import FundBasicItem


class SinaFundSpiderPipeline(object):
    # 初始化连接数据库，
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd='777888', db='fund_test', charset='utf8')

    def process_item(self, item, spider):
        cursor = self.conn.cursor()
        if isinstance(item, FundBasicItem):
            sql = '''CREATE TABLE IF NOT EXISTS fund_basic  
                     (
                          fund_code VARCHAR (30) NOT NULL,
                          fund_name VARCHAR (20) NOT NULL,
                          net_worth VARCHAR(30) NOT NULL,
                          accumulated_net_worth VARCHAR (20) NOT NULL ,
                          previous_net_worth VARCHAR (20) NOT NULL ,
                          rise_and_fall VARCHAR (20) NOT NULL DEFAULT '无',
                          growth_rate VARCHAR (20) NOT NULL DEFAULT '无',
                          subscription_status VARCHAR (20) NOT NULL DEFAULT '无',
                          net_worth_date VARCHAR (20) NOT NULL ,
                          PRIMARY KEY (fund_code)
                     );'''
            cursor.execute(sql)
            for i in range(0, len(item['fund_code'])):
                sql = "REPLACE INTO fund_basic" + " \
                       VALUES \
                            ('" + item['fund_code'][i] + "',\
                            '" + item['fund_name'][i] + "',\
                            '" + item['net_worth'][i] + "',\
                            '" + item['accumulated_net_worth'][i] + "',\
                            '" + item['previous_net_worth'][i] + "',\
                            '" + item['rise_and_fall'][i] + "',\
                            '" + item['growth_rate'][i] + "',\
                            '" + item['subscription_status'][i] + "',\
                            '" + item['net_worth_date'][i] + "'\
                            )"
                self.conn.query(sql)
                self.conn.autocommit(True)
        else:
            pass
        return item

    def close_spider(self, spider):
        self.conn.close()
