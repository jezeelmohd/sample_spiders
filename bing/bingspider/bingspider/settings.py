# Scrapy settings for bingspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import MySQLdb
BOT_NAME = 'bingspider'

SPIDER_MODULES = ['bingspider.spiders']
NEWSPIDER_MODULE = 'bingspider.spiders'
ITEM_PIPELINES = ['bingspider.pipelines.BingspiderPipeline',]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bingspider (+http://www.yourdomain.com)'
#conn=db = MySQLdb.connect(host="localhost",user="root",passwd="passme", db="cubator")
#cursor=db.cursor()
DOWNLOAD_DELAY = 0.25

from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('../settings.conf')

dbhost=parser.get('DB', 'hostname')
dbuser=parser.get('DB', 'username')
dbpassword=parser.get('DB', 'password')
dbdb=parser.get('DB', 'dbname')

db=MySQLdb.connect(dbhost,dbuser,dbpassword,dbdb)
cursor=db.cursor(MySQLdb.cursors.DictCursor)