# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from ylp.items import YelpspiderItem


class LoginSpider(CrawlSpider):
    name = 'ylp'
    
    count=0
    #rules = (Rule(SgmlLinkExtractor(restrict_xpaths='//div[@id="paginationControls"]'),follow=True,callback='parse2'),)    
    
    def __init__(self):
        self.start_urls = ['http://www.yelp.com/biz/vail-c-reese-md-and-felicia-hall-md-san-francisco']
        self.rules = (Rule(SgmlLinkExtractor(restrict_xpaths='//div[@id="paginationControls"]'),follow=True,callback='parse2'),)       
        #super(LoginSpider, self).__init__()
        super(LoginSpider,self).__init__()

    def parse2(self,response):
        hxs = HtmlXPathSelector(response)
        reviews=hxs.select("//div[@id='reviews-other']/ul/li")
        for rev in reviews:
            rating=rev.select("div/div[2]/div[1]/div/div/i/@title").extract()
            rating=rating[0]

            self.count+=1
            author=rev.select("div/div[1]/div/ul[2]/li/a/text()").extract()
            if author:
                author=author[0]
            else:
                author='Null'
            print "%%%%%%%%%%%",self.count


            review_date=rev.select("div/div[2]/div[1]/span[1]/text()").extract()
            review_date=review_date[0]

            review_text=rev.select("div/div[2]/p/text()").extract()
            review_text=review_text[0]
            review_text=review_text.encode('ascii','ignore')
            
            prop=YelpspiderItem(
                rating=rating,
                author=author,
                review_text=review_text,
                review_date=review_date
                )
            print prop