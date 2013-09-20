from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from netaporter.items import Product
from pprint import pprint
import time    
from scrapy.http import FormRequest
from netaporter.tidyhtml import *

class StylemilkSpider(BaseSpider):
    name = "stylemilk"
    allowed_domains = ["stylemilkshop.com"]
    start_urls = (
        'http://www.stylemilkshop.com/collections/womens',
        'http://www.stylemilkshop.com/collections/kids'
        )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        links = [ 'http://www.stylemilkshop.com' + x for x in hxs.select('//div[@class="product-name"]/a/@href').extract()]
        for link in links:
            r = Request(link,callback=self.scrap_product)
            if response.url == 'http://www.stylemilkshop.com/collections/kids':
                r.meta['age_type'] = 'kids'
            else:
                r.meta['age_type'] = 'adult'
            yield r

        next = hxs.select('//div[@class="pagination"]/span[@class="next"]/a/@href').extract()
        if next:
            yield Request('http://www.stylemilkshop.com'+ next[0],callback=self.parse)

    def scrap_product(self,response):
        hxs = HtmlXPathSelector(response)
        url = response.url
        id_url = re.findall('http://www.stylemilkshop.com/products/([\w.-]+)',url)[0]
        title =  hxs.select('//div[@class="intro"]/h1/text()').extract()[0]
        label = hxs.select('//*[@id="price-container"]/h3[2]/span/a/text()').extract()[0]
        description = hxs.select('//div[@id="product-description"]').extract()[0]
        price = hxs.select('//span[@class="amount"]/text()').re('\d+.\d+')[0]
        #whole = tidy(strip_tags(hxs.select('//*[@id="product-page"]').extract()[0]))
        sizes_available = hxs.select('//*[@id="id_container"]/select/option[not(contains(text(),"Sold out"))]/text()').extract()
        sizes_available = [re.findall('(^.+)-',x)[0] for x in sizes_available]
        sizes_sold_out = hxs.select('//*[@id="id_container"]/select/option[contains(text(),"Sold out")]/text()').extract()
        sizes_sold_out =[re.findall('(^.+)-',x)[0] for x in sizes_sold_out]
        image_urls = [x.replace("_small","_full") for x in hxs.select('//div[@class="product-images"]//img/@src').extract()]
        image_urls = [x.replace("_large","_full") for x in image_urls]
        image_urls = [x.split("?")[0] for x in image_urls]
        #possibe_id = re.findall('.+/sites/457/products/(\d+)',image_urls[0])
        price_currency = 'AUD'
        if description:
            description = tidy(strip_tags(description))
        item = Product(
            title= title,
            label=label,
            retailer="stylemilkshop.com",
            gender="female",
            age_type = response.meta['age_type'],
            #category = category,
            image_urls = image_urls,
            sizes_available=sizes_available,
            sizes_sold_out = sizes_sold_out,
            #sizes_coming_soon = sizes_coming_soon,
            #size_and_fit = size_and_fit,
            #details = details,
            #color_other_products = color_other_products,
            price_currency = price_currency,
            #price_discount = price_discount,
            price = float(price),
            description = description,
            #id_product = product_id,
            id_url= id_url,
            date_time=time.strftime('%Y-%m-%d %H:%M:%S'),
            url = response.url,
            #color = color,
            #extra_info = hxs.select()
            )
        pprint(item)
        return item
        