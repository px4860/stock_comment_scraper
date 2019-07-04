import scrapy
import scrapy.downloadermiddlewares.redirect
from stock_comment.items import DmozItem
import json


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    start_urls = [
        "https://finance.yahoo.co.jp/cm/message/1008308/8308/19?offset=1&rv=1"
    ]

    def parse(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_articles_follow_next_page)
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

    def parse_articles_follow_next_page(self, response):
        divs = response.xpath('.//div[@id="cmtlst"]')
        for p in divs.xpath('.//div[@class="comment"]'):
            item = DmozItem()
            item['id'] = p.xpath('./@data-comment').extract()[0]
            # 去除空评论
            try:
                item['comment'] = p.xpath('.//p[@class="comText"]/text()').extract()
            except IndexError:
                continue
            item['datetime'] = p.xpath('.//p[@class="comWriter"]/span/a/text()').extract()[0]
            item['like'] = p.xpath('.//li[@class="positive"]/a/span/text()').extract()[0]
            item['unlike'] = p.xpath('.//li[@class="negative"]/a/span/text()').extract()[0]
            try:
                item['reply'] = p.xpath('.//p[@class="comReplyTo"]/a/@data-parent_comment').extract()[0]
            except IndexError:
                item['reply'] = None
            if p.xpath('.//span[@class="emotionLabel weakest"]'):
                item['tendency'] = 0
            elif p.xpath('.//span[@class="emotionLabel strongest"]'):
                item['tendency'] = 1
            elif p.xpath('.//span[@class="emotionLabel both"]'):
                item['tendency'] = 2
            else:
                item['tendency'] = None
            yield item

        next_page = response.xpath('.//li[@class="next"]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_articles_follow_next_page)