# Define here the models for your scraped items
#
# See documentation in:
# http:/d/oc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class YelpspiderItem(Item):
    eid = Field()
    URL= Field()
    author = Field()
    review_date = Field()
    review_title = Field()
    review_text = Field()
    rating = Field()
    changed_since_last_crawl = Field()