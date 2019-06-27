# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class AdReportPipeline(object):
    def __init__(self):
        self.file = open('D:/Users/yf/Documents/stock.json', 'w')

    def process_item(self, item, spider):
        item['id'],item['like'],item['unlike'] = int(item['id']),int(item['like']),int(item['unlike'])
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
