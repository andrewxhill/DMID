import sys
import simplejson
import urllib
import codecs
import time
import sys

NYTKEY = 'e3f29a79d8b6448d8c90fe59a75dc53b:16:62728759'




class NYTArticles():
    def __init__(self, query,fields=['date','title']):
        self.fields = fields
        self.query = query
        self.errors = []
        
    def getJSON(self, page):
        url = 'http://api.nytimes.com/svc/search/v1/article'
        params = urllib.urlencode({'query': query,
                 'api-key': NYTKEY,
                 'fields': ','.join(self.fields)})
        f = urllib.urlopen("%s?%s" % (url,params))
        return f.read().decode('utf-8')
        
    def parseStream(self):
        first = self.getJSON(0)
        log = open(self.query.strip('"').replace(' ','_')+'.csv',"w+")
        log.write(','.join(self.fields) + "\n")
        data = simplejson.loads(first)
        res = data['results']
        sys.stdout.write(".")
        sys.stdout.flush() 
        for r in res:
            date = r['date'][:4]+'-'+r['date'][4:6]+'-'+r['date'][6:8]
            log.write("%s\t%s\n" % (date,repr(r['title'])))
        len = data['total']
        i = 0
        while i < len:
            try:
                time.sleep(0.5)
                res = simplejson.loads(self.getJSON(i))['results']
                sys.stdout.write(".")
                sys.stdout.flush() 
                for r in res:
                    log.write("%s\t%s\n" % (r['date'][:4]+'-'+r['date'][4:6]+'-'+r['date'][6:8],repr(r['title'])))
            except:
                self.errors.append("page %s skipped" % i)
            i+=1
        for e in self.errors:
            print e
        
if __name__ == "__main__":
    try:
        query = sys.argv[1]
    except:
        print "nyt2csv.py {your_query}"
    query = '"%s"' % query.strip() if len(query.strip().split(" "))>1 else query.strip()
    NYTArticles(query = query).parseStream()
    try:
        NYTArticles(query = query).parseStream()
    except:
        print 'failed'
