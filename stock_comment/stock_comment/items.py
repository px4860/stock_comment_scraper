# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class DmozItem(scrapy.Item):
    id = scrapy.Field()
    comment = scrapy.Field()
    datetime = scrapy.Field()
    like = scrapy.Field()
    unlike = scrapy.Field()
    reply = scrapy.Field()
    tendency = scrapy.Field()
