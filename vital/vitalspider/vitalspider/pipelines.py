# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request
from vitalspider.settings import *

class VitalspiderPipeline(object):

	def process_item(self, item, spider): 

		eid=item['eid']
		URL=item['URL']
		author=str(item['author'])
		rating=str(item['rating'])

		review_title=str(item['review_title'])
		review_date=str(item['review_date'])
		review_text=str(item['review_text'])

		cursor.execute("INSERT INTO vitalsresults (eid, URL, author, review_title, review_date, review_text, rating) VALUES (%s, %s, %s, %s, %s, %s, %s)",(eid, URL, author, review_title, review_date, review_text,rating))
		db.commit()
