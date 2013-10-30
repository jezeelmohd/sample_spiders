from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.shell import inspect_response
from scrapy.http import Request
from time import sleep
from vitalspider.items import *
from vitalspider.settings import *
import re

#from selenium import webdriver

class LoginSpider(BaseSpider):
    page_incr=0    
    rank=0
    end_flag=0

    name = 'vtlspider'
    start_urls = ['https://www.vitals.com']

    def __init__(self,source="http://www.vitals.com/doctors/Dr_Gregory_Yanish/reviews",eid="0"):
        self.start_urls = [source]
        self.URL=source
        self.eid=eid

    def parse(self, response):

        hxs = HtmlXPathSelector(response)
        #inspect_response(response)
        
        awards=hxs.select("//ul[@class='awards']/li")
        for award in awards:
            award_title=award.select("div/@data-title").extract()
            award_title=award_title[0]
            print "%%%%%%%%%%%%%%%%%%%"
            print self.eid,self.URL,award_title
            cursor.execute("INSERT INTO awards (eid, URL,award_title) VALUES (%s, %s, %s)",(self.eid, self.URL, award_title))
            db.commit()     
        reviews=hxs.select("//div[@id='reviewspane']/div")
        for rev in reviews:

            rating=rev.select("div[@class='rating']/span[1]/ul/li/text()").extract()
            rating=rating[0][9:]

            author=rev.select("div[@class='header']/span[@class='reviewer']/text()").extract()
            if author:
                author=author[0]
                author=author[3:]
            else:
                author='Null'
            review_title=rev.select("div[@class='rating']/span[@class='summary']/text()").extract()
            if review_title:
                review_title=review_title[0]
            else:
                review_title='Null'


            review_date=rev.select("div[@class='header']/span[@class='date c_date dtreviewed']/span").extract()
            dat=review_date[0]
            review_date=dat[dat.find('title="')+7:dat.find('">')]

            review_text=rev.select("p[@class='description']/text()").extract()
            review_text=review_text[0]

            prop=VitalspiderItem(
                eid=self.eid,
                URL=self.URL,
                rating=rating,
                author=author,
                review_title=review_title,
                review_text=review_text,
                review_date=review_date
                )
            #print prop
            yield prop