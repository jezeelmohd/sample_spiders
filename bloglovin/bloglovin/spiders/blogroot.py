from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from pprint import pprint
import time    
from scrapy.http import FormRequest
from bloglovin.items import Blog
from bloglovin.tidyhtml import *
import json
import re

social_urls = [
'https://twitter.com/',
 'http://lookbook.nu/',
 'https://www.facebook.com/','https://facebook.com/'
 'http://pinterest.com/',
 'http://instagram.com/',
 'http://youtube.com',
 'https://vimeo.com/',
 'https://google.com.au/',
 'https://myspace.com/'
]

class BlogrootSpider(BaseSpider):
    name = "blogroot"
    #allowed_domains = ["bloglovin.com"]
    start_urls = (
        'http://www.bloglovin.com/',
        )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        categories = hxs.select('//ul[@class="nav"]/li[@class="dropdown category-dropdown"][2]/ul//a[@data-func="Category"]')
        categories = categories
        for cat in categories:
            if cat.select('@data-cat').extract()[0] == '0':
                continue
            link = 'http://www.bloglovin.com' + re.findall('([/\w+]+./\d+)',cat.select('@href').extract()[0])[0]
            req = Request(link,callback=self.parse_category)
            req.meta['category'] = cat.select('text()').extract()[0]
            yield req


    def parse_category(self,response):
        hxs = HtmlXPathSelector(response)
        try:
            url,page,cat = re.findall('(http://www.bloglovin.com/en/blogs/)(\d+)/(\d+)',response.url)[0]
        except:
            url,cat = re.findall('(http://www.bloglovin.com/en/blogs/)(\d+)',response.url)[0]    
            page=0    
        blogs = hxs.select('//div[@class="blog"]/div[@class="content"]')
        for blog in blogs:
            link = "http://bloglovin.com"+blog.select('a/@href').extract()[0]
            blg_url = blog.select('a/h2/span[2]/@data-url').extract()[0]
            req = Request(link,callback=self.parse_blog)
            req.meta['category'] =response.meta['category'] 
            req.meta['url'] = blg_url
            yield req
        if not hxs.select('//*[@class="alert alert-blank"]'):
            req = Request(url+str(int(page)+1)+"/"+cat,callback=self.parse_category)
            req.meta['category'] =response.meta['category']    
            yield req

    def parse_blog(self,response):
        hxs = HtmlXPathSelector(response)
        name = hxs.select('//h1[@class="gl-profile-title"]/text()').extract()   
        followers = long("".join(hxs.select('//*[@id="content"]/div[2]/div/ul/li[2]/a/strong/text()').re('\d+')))
        desc = hxs.select('//*[@id="content"]/div[1]/div[1]/div[3]/text()').extract()
        if desc:
            desc = desc[0]
        else:
            desc = ''
        if name:
            name = name[0]
        else:
            name = ''
        url = response.meta['url']
        item = Blog(
            name = name,
            followers = followers,
            description = desc,
            url = url,
            category = response.meta['category']
        )
        r = Request(url,self.parse_blog_site)
        r.meta['item'] = item
        yield r

    def parse_blog_site(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//a/@href').extract()
        clean_links = []
        for link in links:
            if len(link)>1:
                if link[-1] != '/':
                    link += '/'
            link.lower()
            if '%' not in link and '?' not in link:
                clean_links.append(link)
        found_social_links = []
        for link in list(set(clean_links)):
             #if 'twitter' in re.findall('//([\w+]+)',link) and '%' not in link:
             for social in social_urls:
                if social in link:
                    found_social_links.append(link)
        whole = response.body
        email = resolve_munged_email(whole)
        #NEXT GO FETCH RSS FEED LINK
        feed = hxs.select('//link[@type="application/rss+xml"]/@href').extract()
        if feed:
            feed = feed[0]
            if feed[0] == '/':
                feed = response.url + feed;
        else:
            feed = None
        item = response.meta['item']
        item['feed_url'] = feed
        item['email']= email
        item['social_links']= found_social_links
        pprint(item)
        return item
