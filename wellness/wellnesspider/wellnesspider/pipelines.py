# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from wellnesspider.settings import *
class WellnesspiderPipeline(object):
	def process_item(self, item, spider):
		eid=item['eid']
		URL=item['URL']
		author=str(item['author'])
		rating=str(item['rating'])
		review_date=str(item['review_date'])
		review_text=str(item['review_text'])

		cursor.execute("SELECT max(id) from wellnessparent")
		lastid=cursor.fetchone()
		lastid=str(lastid[0])

		cursor.execute("INSERT INTO wellnessresults (id,eid, author, review_date, review_text, rating) VALUES (%s, %s, %s, %s, %s, %s)",(lastid,eid, author, review_date, review_text,rating))
		db.commit()
