# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class WellnesspiderItem(Item):
    eid = Field()
    URL= Field()
    author = Field()
    review_date = Field()
    review_title = Field()
    review_text = Field()
    rating = Field()
    #award_title=Field()
    changed_since_last_crawl = Field()