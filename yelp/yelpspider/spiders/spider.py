from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.shell import inspect_response
from scrapy.http import Request
from time import sleep
from yelpspider.items import *
import re


class LoginSpider(BaseSpider):
    page_incr=0   
    rank=0
    end_flag=0
    count=1

    name = 'yelpspider'
    start_urls = ['http://www.yelp.com']

    def __init__(self,source="http://www.yelp.com/biz/union-street-dermatology-san-francisco-3",eid="0"):
        self.source = source
        self.start_urls = [source]
        self.URL=source
        self.eid=eid

    def parse(self, response):

        return Request(url=self.URL,callback=self.parse2)

    def parse2(self,response):

        hxs = HtmlXPathSelector(response)
        reviews=hxs.select("//div[@id='reviews-other']/ul/li")

        if not reviews:
            self.end_flag=1
        else:
            print "$$$$$$$$$$$$$$$",reviews

        for rev in reviews:
            rating=rev.select("div/div[2]/div[1]/div/div/i/@title").extract()
            rating=rating[0]
            rating=rating.strip('star rating')

            author=rev.select("div/div[1]/div/ul[2]/li/a/text()").extract()
            if author:
                author=author[0]
            else:
                author='Null'

            review_title=rev.select("div[@class='rating']/span[@class='summary']/text()").extract()
            if review_title:
                review_title=review_title[0]
            else:
                review_title='Null'

            review_date=rev.select("div/div[2]/div[1]/span[1]/text()").extract()
            review_date=review_date[0]

            review_text=rev.select("div/div[2]/p/text()").extract()
            review_text=review_text[0]
            review_text=review_text.encode('ascii','ignore')

            prop=YelpspiderItem(
                eid=self.eid,
                URL=self.URL,
                rating=rating,
                author=author,
                review_text=review_text,
                review_date=review_date
                )
            yield prop
            self.count+=1
            print self.count
            print prop
        self.page_incr += 40
        if self.end_flag==0:
            yield Request(url=self.source+"?start="+str(self.page_incr),callback=self.parse2)