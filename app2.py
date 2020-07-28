# -*- coding: utf-8 -*-
import scrapy
from dingdian.items import ChapterItem,BookItem

class E1wNetSpider(scrapy.Spider):
    name = 'app2'
    # allowed_domains = ['e1w.net']

    def start_requests(self):
        for type in range(1,11):
            urls = 'https://www.e1w.net/list/'+str(type)+'_1.html'
            yield scrapy.Request(urls,self.first)

    def first(self, response):
        max_page = response.xpath('//a[@class="last"]/text()').extract_first()
        print(max_page)
        print(response.url.split('_')[0])
        for page in range(1,int(max_page)+1):
            urls = response.url.split('_')[0]+'_'+str(page)+'.html'
            yield scrapy.Request(urls,self.second)

    def second(self,response):
        hrefs = response.xpath('//*[@id="content"]/dd[1]/table//tr/td[1]/a/@href').extract()
        for href in hrefs:
            book_num = href.split('/')[-1].split('.')[0]
            book_urls = 'https://www.e1w.net/read/'+str(book_num)+'/index.html'
            yield scrapy.Request(book_urls,self.third)

    def third(self,response):
        book_name = response.xpath('//*[@id="a_main"]/div[2]/dl/dd[1]/h1/text()').extract_first()
        author = response.xpath('//*[@id="a_main"]/div[2]/dl/dd[2]/h3/text()').extract_first()
        item = BookItem()
        item['book_name'] = book_name
        item['author'] = author
        chapter_urls = response.xpath('//*[@id="at"]//tr/td/a/@href').extract()
        yield item
        for urls in chapter_urls:
            chapter_href= response.url.split('index')[0] + urls
            yield scrapy.Request(chapter_href,self.forth,meta={'book_name':book_name})

    def forth(self,response):
        item = ChapterItem()
        book_name = response.meta['book_name']
        chapter_title = response.xpath('//*[@id="amain"]/dl/dd[1]/h1/text()').extract_first()
        chapter_contents=''.join(response.xpath('//*[@id="contents"]//text()').extract())
        item['book_name'] = book_name
        item['chapter_name'] = chapter_title
        item['chapter_contents'] = chapter_contents
        yield item






