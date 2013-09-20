####### COUPLE OF SHARED FUNCTIONS TO TIDY HTMLS ###############
from HTMLParser import HTMLParser
import re

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    s=s.get_data()
    return s 

def tidy(s):
    return " ".join(x.strip() for x in s.split())
    #return "".join(s.strip())

def tidy_num(s):
    return "".join(s.split())