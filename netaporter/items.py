# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Product(Item):
    id_url = Field()
    id_product = Field()
    url = Field()
    title = Field()
    label = Field()
    retailer = Field()
    category = Field()
    gender = Field()
    image_urls = Field()
    description = Field()
    price = Field()
    price_currency = Field()
    price_discount = Field()
    sizes_available = Field()
    sizes_sold_out = Field()
    sizes_coming_soon = Field()
    color = Field()
    color_other_products = Field()
    extra_info = Field()
    details = Field()
    size_and_fit = Field()
    date_time = Field()
    video_url = Field()
    #remove if not required
    age_type = Field() # Store if Adult/Kid 
    #db based fields
    #status_sold_out = Field()
    #status_restocked = Field()
    #status_discontinued = Field()
