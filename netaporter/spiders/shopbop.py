from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from netaporter.items import Product
from pprint import pprint
import time    
from scrapy.http import FormRequest
from netaporter.tidyhtml import *
import json

class ShopbopSpider(BaseSpider):
    name = "shopbop"
    allowed_domains = ["shopbop.com"]
    start_urls = ["http://www.shopbop.com/actions/designerindex/viewAlphabeticalDesigners.action"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        brands = ['http://www.shopbop.com'+x for x in hxs.select('//a[@class="designerLink "]/@href').extract() ]
        for brand in brands:
            yield Request(brand+"?all",callback=self.parse_brand)

    def parse_brand(self, response):
        hxs = HtmlXPathSelector(response)
        links = [ 'http://www.shopbop.com'+re.findall('(^.+)\?+.',x)[0] for x in hxs.select('//a[@class="productDetailLink"]/@href').extract() ]
        for link in links:
           yield Request(link,callback=self.parse_product)
           
    def parse_product(self,response):
        hxs = HtmlXPathSelector(response)
        #for grabbing colors and size information 
        url_id = re.findall('(\d+).htm',response.url)[0]
        c_vars = hxs.select('//script[contains(text(),"productDetail")]/text()').extract()[0]
        c_vars = c_vars.replace('var productDetail = ','')
        c_vars = c_vars.replace(';\r\n',"")
        c_vars = json.loads(c_vars)
        title =  tidy(hxs.select('//div[@id="productTitle"]/text()').extract()[0])
        label = tidy(hxs.select('//a[@id="brandName"]/text()').extract()[0])
        price = hxs.select('//meta[@itemprop="price"]/@content').re('\d+.\d+')
        price = float(price[0].replace(',',''))
        try:
            price_discount = float(hxs.select('//div[@class="priceBlock"]/span[@class="salePrice"]').re('\$(\d+.\d+)')[0].replace(',',''))
        except:
            price_discount = None
        price_currency = hxs.select('//meta[@itemprop="currency"]/@content').extract()[0]
        description = hxs.select('//div[@id="longDescriptionContainer"]/text()').extract()
        size_and_fit =hxs.select('//div[@id="modelSizeFitDescription"]').extract()
        try:
            description = tidy(" ".join(description))
        except:
            description = ''
        try:
            size_and_fit = tidy(strip_tags(size_and_fit[0]))
        except:
            size_and_fit = ''
        product_id = hxs.select('//*[@id="productCode"]/@data-product-code').extract()[0]
        all_sizes_keys = [c_vars['sizes'][x]['sizeCode'] for x in c_vars['sizes'].keys()]
        all_sizes_vals = c_vars['sizes'].keys()
        size_dict = dict(zip(all_sizes_keys,all_sizes_vals))
        sl = label.split()
        cl = hxs.select('//*[@id="breadcrumbs"]/a/text()').extract()[0].split()
        category = " ".join(list(set(cl)-set(sl)))
        for c in c_vars['colors'].keys():
            color = c_vars['colors'][c]
            url = response.url + "?colorId=" + c
            color_other_products = ["%s?colorId=%s"%(response.url,x) for x in list(set(c_vars['colors'].keys())-set(list(c)))]
            image_urls = [color['images'][i]['main'] for i in color['images'].keys()]
            sizes_available = [size_dict[x] for x in color['sizes']]
            sizes_sold_out = list(set(all_sizes_vals) - set(sizes_available))
            video = ''
            if color['video']['hasVideo']:
                video = color['video']['mp4']
            if not sizes_available:
                sizes_available = hxs.select('//*[@id="sizeContainer"]/div[@id="sizes"]/span/@data-selectedsize').extract()
                sizes_sold_out = list(set(all_sizes_vals) - set(sizes_available))
            item = Product(
                title= title,
                label=label,
                retailer="shopbop.com",
                gender="female",
                age_type = "adult",
                category = category.lower(),
                image_urls = image_urls,
                sizes_available=sizes_available,
                sizes_sold_out = sizes_sold_out,
                #sizes_coming_soon = sizes_coming_soon,
                size_and_fit = size_and_fit,
                #details = details,
                color_other_products = color_other_products,
                price_currency = price_currency,
                price_discount = price_discount,
                price = price,
                description = description,
                id_product = product_id,
                id_url= url_id,
                date_time=time.strftime('%Y-%m-%d %H:%M:%S'),
                url = url,
                color = color['colorName'],
                video_url = video
                #extra_info = hxs.select()
            )
            return item


