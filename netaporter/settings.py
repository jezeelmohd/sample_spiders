# Scrapy settings for netaporter project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'netaporter'
COOKIES_ENABLED = True
#ITEM_PIPELINES = ['netaporter.pipelines.DuplicatesPipeline']
SPIDER_MODULES = ['netaporter.spiders']
NEWSPIDER_MODULE = 'netaporter.spiders'
LOG_LEVEL = 'INFO'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'netaporter (+http://www.yourdomain.com)'
IMAGES_STORE = '/home/manu/dev/netaporter/images'
