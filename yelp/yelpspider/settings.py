# Scrapy settings for yelpspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import MySQLdb
BOT_NAME = 'yelpspider'

SPIDER_MODULES = ['yelpspider.spiders']
NEWSPIDER_MODULE = 'yelpspider.spiders'
ITEM_PIPELINES = ['yelpspider.pipelines.YelpspiderPipeline',]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'yelpspider (+http://www.yourdomain.com)'
conn=db=MySQLdb.connect(host="localhost",user="root",passwd="passme", db="cubator")
cursor=db.cursor()