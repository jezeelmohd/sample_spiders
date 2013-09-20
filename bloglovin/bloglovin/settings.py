# Scrapy settings for bloglovin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'bloglovin'
COOKIES_ENABLED = True
SPIDER_MODULES = ['bloglovin.spiders']
NEWSPIDER_MODULE = 'bloglovin.spiders'
LOG_LEVEL = 'INFO'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bloglovin (+http://www.yourdomain.com)'
