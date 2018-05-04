# -*- coding: utf-8 -*-
import scrapy


class SinaSpiderSpider(scrapy.Spider):
    name = 'sina_spider'
    allowed_domains = ['sina.com']
    start_urls = ['http://sina.com/']

    def parse(self, response):
        pass
