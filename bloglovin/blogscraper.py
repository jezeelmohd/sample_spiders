import json 
import urllib2
from pprint import pprint
urls = open('blogs.json')
count = 0
blog_urls = []
for blog in urls.readlines():
	blog_urls.append(json.loads(blog)['url'])
pprint(blog_urls	)