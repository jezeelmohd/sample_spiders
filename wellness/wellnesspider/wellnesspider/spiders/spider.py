from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.shell import inspect_response
from scrapy.http import Request
from wellnesspider.items import *
from wellnesspider.settings import *
from datetime import date,timedelta
from dateutil import parser
import re

class LoginSpider(BaseSpider):
    page_incr=0    
    rank=0
    end_flag=0

    name = 'wellness'
    start_urls = ['http://www.wellness.com']

    def __init__(self,source="http://www.wellness.com/reviews/2171328/stanley-chmiel-md-ent-otolaryngologist",eid="0"):
        self.start_urls = [source]
        self.URL=source
        self.eid=eid

    def parse(self, response):

        hxs = HtmlXPathSelector(response)
        reviews=hxs.select("//div[@id='reviews']/div")
        total_rating=hxs.select("//span[@class='reviewCount']/p/span[@class='rating']/span/span/@title").extract()
        total_rating=total_rating[0]
        total_reviews=hxs.select("//span[@class='reviewCount']/p/span[@class='count']/text()").extract()
        total_reviews=total_reviews[0]

        cursor.execute("INSERT INTO wellnessparent (eid, URL, num_reviews, rating) VALUES (%s, %s, %s, %s)",(self.eid,self.URL, total_reviews,total_rating))
        db.commit()
        print '##########',cursor.lastrowid

        def date_format(rdate):
            today=date.today()
            if 'day' in rdate:
                rdate=rdate[7:]
                days=re.findall(r'\d+',rdate)
                days=days[0]
                days=-int(days)
                tod=today+timedelta(days=days)
                return tod
            if 'week' in rdate:
                rdate=rdate[7:]
                days=re.findall(r'\d+',rdate)
                days=days[0]
                days=-int(days)
                tod=today+timedelta(weeks=days)
                return tod
            else:
                dt = parser.parse(rdate)
                return dt

        for rev in reviews:

            rating=rev.select("span[@class='rating']/span/@title").extract()
            rating=rating[0]

            author=rev.select("div[@class='reviewer vcard']/div/span[@class='review_name fn']/text()").extract()
            if author:
                author=author[0]
            else:
                author='Null'

            review_date=rev.select("span[@class='review_date']/span/text()").extract()
            review_date=review_date[0]
            review_date=date_format(review_date)

            review_text=rev.select("div[@class='review_text description']/div")
            if review_text:
                text=' '
                for reve in review_text:
                    revt=reve.select("text()").extract()
                    revt=revt[0]
                    text=text+revt
                review_text=text
            else:
                review_text=rev.select("div[@class='review_text description']/text()").extract()
                review_text=review_text[0]
                review_text=review_text.encode('ascii','ignore')

            prop=WellnesspiderItem(
                eid=self.eid,
                URL=self.URL,
                rating=rating,
                author=author,
                review_text=review_text,
                review_date=review_date
                )
            yield prop