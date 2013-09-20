from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.shell import inspect_response
from scrapy.http import Request
from time import sleep
import re
import urllib2
from HTMLParser import HTMLParser
from bingspider.items import *
from bingspider.settings import *
import logging
from scrapy.log import ScrapyFileLogObserver
from scrapy import log

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

class LoginSpider(BaseSpider):
    page_incr=11    
    rank=0
    end_flag=0
    name = 'bspider'
    start_urls = ["https://www.bing.com"]
    handle_httpstatus_list = [503]
    


    def __init__(self,keyword="dr mona bhan",source="http://www.bing.com",total=6,eid=0,desttable="bingresults"):
        self.source = source
        self.keyword = keyword
        self.totalresults = int(total)
        self.eid = int(eid)
        self.start_urls = [source]
        self.desttable = desttable
        """
        logfile = open('/logs/gspider.log', 'a')
        log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
        log_observer.start()
        """
    def parse(self, response):
        print self.keyword,type(self.totalresults),self.source
        sleep(10)
        return Request(url=self.source+"/search?q="+self.keyword,callback=self.parse2)
    
    def parse2(self, response):
        #sleep(10)
        if response.status == 503:
            sleep(7200)
        def strip_tags(html):
            s = MLStripper()
            s.feed(html)
            s=s.get_data()
            return s 

        hxs = HtmlXPathSelector(response)
        #total bing results are in this object
        results = hxs.select("//div[@id='results']/ul/li")

        for res in results:
            p = re.compile(r'<.*?>')

            title = res.select("div/div/div[1]/h3/a").extract()
            if title:
                title=title[0]
                title=title.encode('ascii','ignore')
                title=strip_tags(title)
            else:
                title='null'
            url=res.select("div/div/div[1]/h3/a/@href").extract()
            if url:
                url=url[0]
            else:
                continue
            #url=url[url.find('?q=')+3:url.find('&amp')]
            #Destination text area
            
            #This flag either turns grabbing destination text on of off
            bGetDest=0
            self.desttext=""

            if bGetDest:
                if url:
                    exclude_desttext=['.pdf','.xls','.doc','.docx']
                    flag=1
                    for chk in exclude_desttext:
                        if chk in url.lower():
                            flag=0
                            break  
                    if flag==1:
                        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                                'Accept-Encoding': 'none',
                                'Accept-Language': 'en-US,en;q=0.8',
                                'Connection': 'keep-alive'}                
                            
                        try:
                            req = urllib2.Request(url, headers=hdr)
                            response = urllib2.urlopen(req)

                            self.page_source = response.read()
                            self.desttext=strip_tags(self.page_source)
                                #self.desttext=self.desttext.encode('ascii','ignore')
                        except:
                            self.desttext="Not available"
                    else:
                        self.desttext="Other format"
            # end destination text
            
            #summary getting
            summary = res.select("div/div/p").extract()
            if summary:
                summary=summary[0]
                """
                q=re.compile(r'<.*?>')
                summary=q.sub("",summary)
                summary=str(summary.encode('ascii','ignore'))
                """
                summary=str(summary.encode('ascii','ignore'))
                summary=str(strip_tags(summary))
            #description getting
            description = res.select("div/div/ul/li/a").extract()
            if description:
                dtext=''
                for e in description:
                    txt=strip_tags(e)
                    dtext=dtext+txt+','
                description=str(dtext)
            else:
                description=''
            #description=",".join(description)
            #print description
            #rate_text = res.select("div/div/div/div[@class='f slp'/span/text()").extract()
            
            rate_text = res.select("div/div/ul/li/span/@title").extract()
            if rate_text:
                rate_text=rate_text[0].encode('ascii','ignore')

                #log.msg("** AK RATING IS: "+rate_text, level=log.INFO)
                if 'Rating:' in rate_text:
                    rate_text=rate_text[7:]
                else:
                    rate_text=''
            else:
                rate_text=''
            
            #check if no of results needed reached?
            if self.rank>=self.totalresults:
                print "Result reached its limit:",self.rank
                self.end_flag=1
                break
            self.rank+=1

            prop = BingspiderItem(
                Title = title,
                URL = url,
                Summary = summary,
                Description = description,
                Rank=self.rank,
                Keyword = self.keyword.lower(),
                Source = self.source,
                eid = self.eid,
                rating =rate_text,
                Desttext=self.desttext,
                desttable=self.desttable
            )
            yield prop
           
        #recurse the function to change the page if no of results is not reached
        
        if self.end_flag==0:
            yield Request(url=self.source+"/search?q="+self.keyword+"&first="+str(self.page_incr),
                callback=self.parse2)
            self.page_incr += 10

