from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from pprint import pprint
import time
from scrapy.shell import inspect_response
from netaporter.tidyhtml import *
from netaporter.items import Product
import re
from scrapy import log

class LiveClothingSpider(BaseSpider):
	name="liveclo"
	allowed_domains = ["www.liveclothing.com.au"]
	start_urls = ['http://www.liveclothing.com.au/MENS.aspx?s4&p=1&ipp=10000&f=_v4-pv1-nMENS-t35-c0_&o=Default']
	linkadd='http://www.liveclothing.com.au/'

	def parse(self,response):
		hxs=HtmlXPathSelector(response)
		product_links=hxs.select('//*[@id="pProductListing"]/div[2]/ul/li/strong/a/@href').extract()
		category=response.url[31:].split('.aspx')[0]
		for pro in product_links:
			product_link=self.linkadd+pro
			req=Request(product_link,callback=self.scrap_product)
			req.meta['category']=category
			yield Request(product_link,callback=self.scrap_product)
	"""
	def parse_category(self, response):
		hxs = HtmlXPathSelector(response)
		brands = hxs.select('//*[@id="prodlist"]/table/tr[1]//@href').extract()
		if brands:
			for brand in brands:
				brand=self.linkadd+brand
				req=Request(brand,callback = self.scrap_product)
				yield req
	"""

	def scrap_product(self,response):
		hxs=HtmlXPathSelector(response)
		currency='AUD'		
		def strclean(text):
			text=text[0]
			text=str(strip_tags(text).encode('ascii','ignore'))
			text=str.strip(text)
			return text
		#try:
		if True:
			#product_id=response.url.split('/0/')[-1].strip('.htm')
			label=hxs.select('//*[@id="plProductInfo"]/div[3]/h1/text()').extract()
			title=hxs.select('//*[@id="plProductInfo"]/div[3]/h1/div/text()').extract()
			if label:
				label=strclean(label)
			if title:
				title=strclean(title)

			category=response.meta['category']
			"""
			if category:
				category=category[0]
			else:
				category=None
			"""
			sub_category=hxs.select('//*[@id="plProductInfo"]/div[3]/ul/li/a/@title').extract()
			if sub_category:
				sub_category=sub_category[1]
			else:
				sub_category=None

			discount_price=None
			price=None
			price=hxs.select('//*[@id="htmlPrice"]/text()').extract()[0]
			prn=re.compile(r'\d+.\d+')
			if price:
				price=prn.findall(price[0])
				price=float(price[0])
			else:
				price=None
			discount_price=hxs.select('//*[@id="stPriceSpecial"]/text()').extract()
			if discount_price:
				discount_price=prn.findall(discount_price[0])
				discount_price=float(discount_price[0])
			else:
				discount_price=None
			"""
			desc=hxs.select('//*[@id="description"]/p/span/text()').extract()
			if desc:
				desc=''.join(desc)
			else:
				desccase=hxs.select('//*[@id="description"]//text()').extract()
				if desccase:
					desc=' '.join(desccase)
				else:
					desc=''
			"""
			style_code=hxs.select('//*[@id="lblCode"]/text()').extract()
			if style_code:
				style_code=style_code[0]
			else:
				style_code=None

			fabric=hxs.select('//*[@id="lblFabric"]/text()').extract()
			if fabric:
				fabric=fabric[0]
			else:
				fabric=None
			"""
			descspc=hxs.select('//*[@id="accordion"]/div[1]/text()').extract()
			if descspc:
				descspc=','.join(descspc)
				desc=desc+'\n'+descspc
			"""
			colour=hxs.select('//*[@id="htmlColours"]/div/div/div/text()').extract()


			sizes=hxs.select('//*[@id="htmlSizes"]/div//a/text()').extract()
			sizes_sold_out=[]
			sizes_available=[]
			if sizes:
				#sizes=[size.split() for size in sizes]
				for size in sizes:
					if "sold-out" in size:
						sizes_sold_out.append(size.strip('(sold-out)'))
					else:
						sizes_available.append(size)
			else:
				sizes=None
			main_image=hxs.select('//*[@id="imgImage1URL"]/@src').extract()
			if main_image:
				main_image=main_image[0]
			images=hxs.select('//*[@id="plImages"]/ul/li/a/@href').extract()
			if images:
				img_links=images

		items = Product(
			title= title,
			label=label,
			#retailer="frockaholics.com",
			#gender='Female',
			category = category,
			sub_category=sub_category,
			image_urls = img_links,
			main_image_url=main_image,
			sizes_available=sizes_available,
			sizes_sold_out = sizes_sold_out,
			#sizes_coming_soon = sizes_coming_soon,
			#size_and_fit = size_and_fit,
			#color_other_products = colour,
			#price_currency = currency,
			price = now_price,
			price_discount=discount_price,
			#description = desc,
			#id_product = product_id,
			id_url= product_id,
			#date_time=time.strftime('%Y-%m-%d %H:%M:%S'),
			url = response.url,
			#age_type = 'adult',
			#extra_info = hxs.select()
			)
		yield items