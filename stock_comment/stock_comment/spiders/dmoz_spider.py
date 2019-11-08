import scrapy
import scrapy.downloadermiddlewares.redirect
from stock_comment.items import DmozItem
import json


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    start_urls = [
        "http://sousuo.gov.cn/column/30562/0.htm"
    ]

    def parse(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_articles_follow_next_page)
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

    def parse_articles_follow_next_page(self, response):
        divs = response.xpath('/html/body/div[2]/div/div[2]/div[2]/ul/li')
        for p in divs:
            # item = DmozItem()
            # item['id'] = p.xpath('./@data-comment').extract()[0]
            # # 去除空评论
            # try:
            #     item['comment'] = p.xpath('.//p[@class="comText"]/text()').extract()
            # except IndexError:
            #     continue
            # item['datetime'] = p.xpath('.//p[@class="comWriter"]/span/a/text()').extract()[0]
            # item['like'] = p.xpath('.//li[@class="positive"]/a/span/text()').extract()[0]
            # item['unlike'] = p.xpath('.//li[@class="negative"]/a/span/text()').extract()[0]
            # try:
            #     item['reply'] = p.xpath('.//p[@class="comReplyTo"]/a/@data-parent_comment').extract()[0]
            # except IndexError:
            #     item['reply'] = None
            # if p.xpath('.//span[@class="emotionLabel weakest"]'):
            #     item['tendency'] = 0
            # elif p.xpath('.//span[@class="emotionLabel strongest"]'):
            #     item['tendency'] = 1
            # elif p.xpath('.//span[@class="emotionLabel both"]'):
            #     item['tendency'] = 2
            # else:
            #     item['tendency'] = None
            # yield item

            next_page = p.xpath('.//h4/a/@href')
            if next_page:
                url = response.urljoin(next_page[0].extract())
                yield scrapy.Request(url, self.article_page)

    def article_page(self, response):
        next_page = response.xpath('/html/body/div[1]/div[2]/div[1]/p/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.detail_page)

    def detail_page(self, response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        item = DmozItem()
        item['title'] = response.xpath('/html/body/div[3]/div[1]/div[2]/h1').extract()
        item['content'] = response.xpath('/html/body/div[3]/div[1]/div[2]/div[2]/p[3]/text()').extract()
        yield item