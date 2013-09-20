from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from pprint import pprint
from netaporter.tidyhtml import *
from netaporter.items import Product
import time

class IconicSpider(BaseSpider):
    name = "iconic"
    allowed_domains = ["theiconic.com.au"]
    start_urls = (
        'http://www.theiconic.com.au/womens-brands/',
        'http://www.theiconic.com.au/mens-brands/',
        'http://www.theiconic.com.au/kids-brands/'
        )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        brands = ['http://www.theiconic.com.au'+x for x in hxs.select('//a[@class="brands-item"]/@href').extract()]
        for brand in brands:
            yield Request(brand,callback = self.get_product_links)

    def get_product_links(self, response):
        hxs = HtmlXPathSelector(response)
        product_links = [ 'http://www.theiconic.com.au' + x for x in hxs.select('//a[@class="link-item"]/@href').extract()]
        for link in product_links:
            yield Request(link,callback=self.scrap_product)

    def scrap_product(self, response):
        hxs = HtmlXPathSelector(response)
        #Fields
        id_url = re.findall('(\d+)\.html',response.url)[0]
        title = tidy(hxs.select('//*[@id="productpage"]/div[1]/article/section[1]/div[3]/h1/text()').extract()[0])
        label = tidy(hxs.select('//*[@id="productpage"]/div[1]/article/section[1]/div[3]/h1/strong/text()').extract()[0])
        image_urls = [x.replace("gallery","zoom") for x in hxs.select('//*[@id="prdMedia"]/ul//img/@src').extract()]
        description = tidy(strip_tags(hxs.select('//*[@id="productpage"]/div[1]/article/section[1]/div[5]/div').extract()[0]))
        product_id = hxs.select('//*[@id="detail-description"]/div/table//tr[contains(td/text(),"SKU")]/td[2]/text()').extract()[0]
        category = hxs.select('//*[@id="content"]/div[1]/ul/li[2]/a/text()').re('\w+')[0]  
        tags = hxs.select('//*[@id="content"]/div[1]/ul/li[2]/a/@href').re('\w+')
        if 'mens' in tags:
            age_type = 'adult'
            gender = 'male'
        elif 'womens' in tags:
            age_type = 'adult'
            gender = 'female'
        elif 'kids' in tags:
            age_type = 'kids'
            if 'unisex' in tags:
                gender = 'unisex'
            elif 'boys' in tags:
                gender = 'male'
            else:
                gender = 'female'
        elif 'unisex' in tags and 'kids' not in tags:
            age_type = 'adult'
            gender = 'unisex'
        else:
            print tags
        price_discount = None                
        price_currency = 'AUD'
        try:
            price = hxs.select('//span[@class="price"]').re('\d+.\d+')[0]
        except:
            price_discount = float(hxs.select('//span[@class="price-value value"]/span/text()').re('\\d+.\d+')[0])
            price = hxs.select('//span[@class="price-value value"]/span/text()').re('\\d+.\d+')[1]
        color = hxs.select('//*[@id="detail-description"]/div/table//tr[contains(td/text(),"Colour")]/td[2]/text()').extract()[0]
        color_other_products = ['http://www.theiconic.com.au'+x for x in hxs.select('//div[@class="block related-products"]//li/a/@href').extract()]
        sizes_available = hxs.select('//*[@id="product-size-selector"]/ul/li/a[not(@class="unavailable")]/text()').re('[^\s]+')
        sizes_sold_out = hxs.select('//*[@id="product-size-selector"]/ul/li/a[@class="unavailable"]/text()').re('[^\s]+')
        details =hxs.select('//*[@id="detail-description"]/div/table//tr[not(contains(td/text(),"SKU")) and not(contains(td/text(),"Colour"))]').extract()
        if details:
            details = tidy(strip_tags(details[0]))
        else:
            details = None
        item = Product(
            title= title,
            label=label,
            retailer="iconic.com",
            gender="female",
            age_type = age_type,
            category = category,
            image_urls = image_urls,
            sizes_available=sizes_available,
            sizes_sold_out = sizes_sold_out,
            #sizes_coming_soon = sizes_coming_soon,
            #size_and_fit = size_and_fit,
            details = details,
            color_other_products = color_other_products,
            price_currency = price_currency,
            price_discount = price_discount,
            price = float(price),
            description = description,
            id_product = product_id,
            id_url= id_url,
            date_time=time.strftime('%Y-%m-%d %H:%M:%S'),
            url = response.url,
            color = color,
            #extra_info = hxs.select()
            )
        return item


