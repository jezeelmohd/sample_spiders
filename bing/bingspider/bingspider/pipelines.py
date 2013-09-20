# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request
from bingspider.settings import *

class BingspiderPipeline(object):
    def process_item(self, item, spider):
        titl=item['Title']
        lnk=item['URL']
        summ=item['Summary']
        desc=item['Description']
        rank=item['Rank']
        keyword = item['Keyword']
        source = item['Source']
        eid = item['eid']
        desttable=item['desttable']
        rating=item['rating']
        desttext=item['Desttext']

#        sqlkey = "SELECT Keyword, URL FROM searchresults where eid = %s" % (eid)
#        cursor.execute(sqlkey)
#        sqlkey=cursor.fetchall()
        
#        if (keyword,lnk) in sqlkey:
#            cursor.execute ("UPDATE searchresults SET Title=%s, URL=%s, Summary=%s, Description=%s, Keyword=%s, Rank=%s, Source=%s, eid=%s WHERE Keyword=%s AND Rank=%s",(titl, lnk, summ, desc, keyword, rank, source, eid, keyword, rank))
#            db.commit()
#        else:
        tsql = "INSERT INTO %s" % (desttable)
        cursor.execute(tsql+" (Title, URL, Summary, Description, Keyword, Rank, Source, eid,text_rating,Destinationtext) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s)" , (titl, lnk, summ, desc, keyword, rank, source, eid,rating,desttext))
        db.commit()

        cursor.execute("UPDATE scraper_queue set lastrun = now(), itemsscraped = %s where eid = %s",(rank, eid))
        db.commit()
