# Scrapy settings for wellnesspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import MySQLdb
BOT_NAME = 'wellnesspider'

SPIDER_MODULES = ['wellnesspider.spiders']
NEWSPIDER_MODULE = 'wellnesspider.spiders'
ITEM_PIPELINES = ['wellnesspider.pipelines.WellnesspiderPipeline',]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'yelpspider (+http://www.yourdomain.com)'
conn=db=MySQLdb.connect(host="localhost",user="root",passwd="passme", db="cubator")
cursor=db.cursor()