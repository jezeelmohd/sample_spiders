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

def resolve_munged_email(whole):
    reg = re.search(r'(([\w-]+)@([\w-]+)([.])([\w]+[\w.]+))|(([\w-]+)@([\w-]+)([.])([\w]+[\w.]+)(.invalid))|(([\w-]+)<i>@<i>([\w-]+)<i>([.])</i>([\w.-]+))|(([\w-]+)(\(at\))([\w-]+)([.])([\w]+[\w.]+))|(([\\w\\s]+)\\s@\\s([\\w\\s]+)\\s([.])\\s([\\w\\s]+[\\w.]+))|(([\w-]+)([.])([\w-]+)@([\w]+[\w.]+))|(([\w-]+)(\sat\s)([\w-]+)(\sdot\s)([\w].+))|(([\w-]+)(\sat\s)([\w-]+)(\(dot\)([\w].+)))',whole)
    if reg:
        email = reg.group()
        if 'png' not in email.lower() and 'jpg' not in email.lower() and 'gif' not in email.lower():
            if reg.re == re.compile('(([\w-]+)([.])([\w-]+)@([\w]+[\w.]+))'):
                #email format : moc.elpmaxe@eno-on
                #so reverse it
                print 'reverse'
                email = email[::-1]
            
            if reg.re == re.compile('(([\w-]+)<i>@<i>([\w-]+)<i>([.])</i>([\w.-]+))'):
                #email format:no-one<i>@</i>example<i>.</i>com
                #so strip the tags out
                print 'italics'
                email = strip_tags(email)
            
            if reg.re == re.compile('(([\w\s]+)\s@\s([\w\s]+)\s([.])\s([\w\s]+[\w.]+))'):
                print 'spaces'
                #email format: n o - o n e @ e x a m p l e . c o m
                #so strip spaces
                email = "".join(email.split())
            
            if ' at ' in email or '(at)' in email:
                print 'atreplace'
                #email format:no-one at example (dot) com
                email = email.replace(' at ','@')
                email = email.replace('(at)','@')

            if ' dot ' in email or '(dot)' in email:
                print 'dotreplACE'
                email = email.replace('(dot)','.')
                email = email.replace(' dot ','.')

            if 'NOSPAM' not in email and '.invalid' in email:
                #email format:no-one@elpmaxe.com.invalid  
                'no-one@elpmaxe.com.invalid', 'no-one', 'elpmaxe', '.', 'com', '.invalid'  
                #so reverse only domain name and remove invalide
                print resolve_munged_email
                address,name,domain,dot,com,invalid = re.findall('(([\w-]+)@([\w-]+)([.])([\w]+[\w.]+)(.invalid))',email)[0]
                domain = domain[::-1]
                email = name+'@'+domain+'.'+com

            if 'REMOVEME' in email:
                print 'REMOVEME'
                #email format:no-one@exampleREMOVEME.com
                email = email.replace('REMOVEME','')

            if 'NOSPAM' in email and '.invalid' in email:
                print 'NOSPAM'
                #email format:no-one@exampleNOSPAM.com.invalid
                email = email.replace('NOSPAM','')

            if '.invalid' in email:
                print 'invalid'
                email = email.replace('.invalid','')
            
            if '<i>' in email:
                email = strip_tags(email)
            return email
    else:
        return None