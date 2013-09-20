from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from netaporter.items import Product
from pprint import pprint
import time    
from scrapy.http import FormRequest
from netaporter.tidyhtml import *

class ProductSpider(BaseSpider):
    name = 'product'
    allowed_domains = ['net-a-porter.com']
    FormRequest(
        url="http://www.net-a-porter.com/apac/changecountry.nap?overlay=true",
        formdata={'language': 'en', 'country': 'AU','channel':'APAC'}
    )
    start_urls = ['http://www.net-a-porter.com/Shop/AZDesigners']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//*[@id="atoz-page-container"]/div[@class="designer_list_col"]/ul/li[not(@class="top-letter")]/a/@href').extract()
        links[:] = ['http://net-a-porter.com' + x for x in links]
        for link in links:
            yield Request(link,callback=self.follow_designer_link)

    def follow_designer_link(self,response):
        hxs = HtmlXPathSelector(response)
        product_links = hxs.select('//div[@class="product-details"]/div/a/@href').extract()
        if product_links:
            product_links[:] = ['http://net-a-porter.com' + x for x in product_links]
            for link in product_links:
                yield Request(link,callback=self.follow_product_link)
        else:
            print "No products for this guy"+str(response.url)

    def follow_product_link(self,response):
        hxs = HtmlXPathSelector(response)
        title = tidy(hxs.select('//*[@id="product-details"]/h2/text()').extract()[0])
        i_urls = hxs.select('//*[@id="thumbnails-container"]/img/@src').extract()
        i_urls[:] = [x.replace("_xs","_xl") for x in i_urls]
        description = hxs.select('//div[contains(@class,"tabBody1")]/p/span').extract()
        currency = hxs.select('//*[@id="welcome"]/li[2]/div/span/text()').extract()
        product_id = int(hxs.select('//span[@class="product-code"][1]/text()').re('\d+')[0])
        price = float(tidy_num(hxs.select('//*[@id="price"]/text()').extract()[0])[1:].replace(",", ""))
        sizes_available=hxs.select('//*[@id="choose-your-size"]/select/option[not(contains(@value,"so_")) and not(@value="-1") and not(contains(text(),"Coming soon"))]/text()').extract()
        sizes_coming_soon = hxs.select('//*[@id="choose-your-size"]/select/option[contains(text(),"Coming soon")]/text()').extract()
        sizes_sold_out = hxs.select('//*[@id="choose-your-size"]/select/option[contains(@value,"so_")]/text()').extract()
        sizes_available[:] = [tidy(size) for size in sizes_available]
        sizes_coming_soon[:] = [tidy(size).replace(" - Coming soon","") for size in sizes_coming_soon]
        sizes_sold_out[:] = [tidy(size).replace(" - sold out","") for size in sizes_sold_out]
        size_and_fit = tidy(strip_tags(hxs.select('//div[contains(@class,"tabBody3")]/span/ul').extract()[0]))
        details = tidy(strip_tags(hxs.select('//div[contains(@class,"tabBody2")]/p/span/ul').extract()[0]))
        other_color_links = ['http://net-a-porter.com'+x for x in hxs.select('//*[@id="alternative-colors"]/a/@href').extract()]
        if description:
            description = tidy(strip_tags(description[0]))
        if currency:
            currency=tidy(currency[0])[:3]
        item = Product(
            title= title,
            label=hxs.select('//*[@id="product-details"]/h1/a/text()').extract()[0],
            retailer="net-a-porter.com",
            gender="female",
            category = hxs.select('/html/head/script[contains(text(),"subsection1")]').re(r'subsection1.+"(\w+)')[0],
            image_urls = i_urls,
            sizes_available=sizes_available,
            sizes_sold_out = sizes_sold_out,
            sizes_coming_soon = sizes_coming_soon,
            size_and_fit = size_and_fit,
            details = details,
            color_other_products = other_color_links,
            price_currency = currency,
            price = price,
            description = description,
            id_product = product_id,
            id_url= product_id,
            date_time=time.strftime('%Y-%m-%d %H:%M:%S'),
            url = response.url,
            age_type = 'adult',
            #extra_info = hxs.select()
            )
        return item

        