# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from sqlalchemy import create_engine
from sqlalchemy import Column, MetaData, Table
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker

class YlpPipeline(object):
	def __init__(self):
		engine = create_engine("mysql://root:passme@localhost/a", echo=True)
		metadata = MetaData()
    def process_item(self, item, spider):
	