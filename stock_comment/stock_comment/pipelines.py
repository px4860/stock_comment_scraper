# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exporters import CsvItemExporter
from stock_comment.items import DmozItem
import ast
import csv


# 生成json文件
class AdReportPipeline(object):
    def __init__(self):
        self.file = open('D:/Users/yf/Documents/stock.json', 'w')

    def process_item(self, item, spider):
        item['id'],item['like'],item['unlike'] = int(item['id']),int(item['like']),int(item['unlike'])
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


# 照爷版生成csv文件
class CSVPipeline(object):
    def __init__(self):
        self.f = open("D:/Users/yf/Documents/stock.csv", "a", newline="")
        self.fieldnames = ["id", "comment", "datetime", "like", "unlike", "reply", "tendency"]
        self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item

    def close(self, spider):
        self.f.close()


# 这里定义导出器并且修改序列化规则
class CSVExporter(CsvItemExporter):

    def serialize_field(self, field, name, value):
        if name == 'comment':
            temp = ''
            for row in value:
                temp += row
            return temp.replace('\n','')
        serializer = field.get('serializer', self._join_if_needed)
        return serializer(value)


# 定义导出输出
class CSVExportPipeline(object):
    def __init__(self):
        self.file = open('D:/Users/yf/Documents/stock.csv', 'wb')
        self.exporter = CSVExporter(self.file)

    def spider_opened(self, spider):
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item