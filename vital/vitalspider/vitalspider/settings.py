# Scrapy settings for vitalspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import MySQLdb

BOT_NAME = 'vitalspider'

SPIDER_MODULES = ['vitalspider.spiders']
NEWSPIDER_MODULE = 'vitalspider.spiders'
ITEM_PIPELINES = ['vitalspider.pipelines.VitalspiderPipeline',]
#ITEM_PIPELINES = ['vitalspider.pipelines.VitalsAwardPipeline',]
#,'vitalspider.pipelines.VitalsAwardPipeline'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'vitalspider (+http://www.yourdomain.com)'

conn=db=MySQLdb.connect(host="localhost",user="root",passwd="passme", db="cubator")
cursor=db.cursor()