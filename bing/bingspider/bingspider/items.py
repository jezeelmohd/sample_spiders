# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class BingspiderItem(Item):
    URL= Field()
    Title = Field()
    Summary = Field()
    Description = Field()
    Rank = Field()
    Keyword = Field()
    Source = Field()
    eid = Field()
    rating=Field()
    Desttext=Field()
    desttable=Field()