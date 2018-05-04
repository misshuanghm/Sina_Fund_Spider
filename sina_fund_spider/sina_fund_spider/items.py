# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaFundSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 从首页获取的基金信息
class FundBasicItem(scrapy.Item):
    fund_code = scrapy.Field()
    fund_name = scrapy.Field()
    net_worth = scrapy.Field()
    accumulated_net_worth = scrapy.Field()
    previous_net_worth = scrapy.Field()
    rise_and_fall = scrapy.Field()
    growth_rate = scrapy.Field()
    subscription_status = scrapy.Field()
    net_worth_date = scrapy.Field()
