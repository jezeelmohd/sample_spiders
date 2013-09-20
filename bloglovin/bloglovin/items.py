from scrapy.item import Item, Field

class Blog(Item):
    name = Field()
    followers = Field()
    description = Field()
    url = Field()
    category = Field()
    social_links  = Field()
    email = Field()
    image_urls = Field()
    feed_url = Field()