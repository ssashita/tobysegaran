'''
Created on Feb 20, 2014

@author: ssashita
'''
import unittest
from searchengine import crawler,searcher
from urlsimilarity import urlsimilarity
from runcrawl import dbcleanup as dbcleanup_runcrawl
from runurlsimilarity import dbcleanup as dbcleanup_runurlsimilarity
from runuserurlhits import dbcleanup as dbcleanup_runuserurlhits
from runuserurlhits import createuserurlhitsfromsimilarurls, getuseridcountfromdbase
import cconfigurator

def dbcleanup(dbname):
    dbcleanup_runcrawl(dbname)
    dbcleanup_runurlsimilarity(dbname)
    dbcleanup_runuserurlhits(dbname)

iconfig=0
config=cconfigurator.configure("testquery.db")

def setupcommon(config):
    if config.startfrom <= cconfigurator.startfromcrawling:
        dbcleanup(config.dbname)
#           seed=["http://en.wikipedia.org/wiki/India",
#               "http://en.wikipedia.org/wiki/Native_Americans_in_the_United_States"]
        seed=config.seed
        #seed = ["http://en.wikipedia.org/wiki/Memory", "http://en.wikipedia.org/wiki/Computer_memory"]     
        crawled=crawler(config.dbname)
        crawled.createindextables()
        crawled.crawl(seed, depth=config.crawlerdepth)
        crawled.calculatepagerank()
        cur=crawler.con.execute('select * from pagerank,urllist where pagerank.urlid=urllist.rowid order by score desc')
    
    if config.startfrom <= cconfigurator.startfromurlsimilarity:
        urlsimilarityobj = urlsimilarity(config.dbname)
        urlsimilarityobj.createtables()
        urlsimilarityobj.fillsimilaritymatrix()
    if config.startfrom <= cconfigurator.startfromuserurlhits:
        config.numusers= createuserurlhitsfromsimilarurls(config.dbname, minclusterlength=config.minclusterlength,
                                                          minsimilarity=config.minsimilarityforclustering, loglevel=config.loglevel)
        config.numusers = getuseridcountfromdbase(config.dbname)
                
class Test(unittest.TestCase):
    #DO NOT define an __init__    
    def setUp(self):        
        self.config = config
        self.dbname = self.config.dbname
        #setupcommon(config)     
           
        if self.config.startfromcrawling:
            dbcleanup(self.dbname)
#           seed=["http://en.wikipedia.org/wiki/India",
#               "http://en.wikipedia.org/wiki/Native_Americans_in_the_United_States"]
            seed=self.config.seed
        #seed = ["http://en.wikipedia.org/wiki/Memory", "http://en.wikipedia.org/wiki/Computer_memory"]     
            crawled=crawler(self.dbname)
            crawled.createindextables()
            crawled.crawl(seed, depth=self.config.crawlerdepth)
            crawled.calculatepagerank()
            cur=crawler.con.execute('select * from pagerank,urllist where pagerank.urlid=urllist.rowid order by score desc')
        else:
            if self.config.startfromurlsimilarity:
                urlsimilarityobj = urlsimilarity(self.dbname)
                urlsimilarityobj.createtables()
                urlsimilarityobj.fillsimilaritymatrix()
            else:
                if self.config.startfromuserurlhits:
                    self.numusers= createuserurlhitsfromsimilarurls(self.dbname, minclusterlength=self.config.minclusterlength,
                                                                    minsimilarity=self.config.minsimilarityforclustering, loglevel=self.config.loglevel)
                    self.numusers = getuseridcountfromdbase(self.dbname)
        
    def tearDown(self ):
        if self.config.cleanup:
            dbcleanup(self.dbname)

    def testQueryIndian(self):
        wordids=[]
        rows=[]
        if self.config.queries == None or len(self.config.queries) <= 0:
            queries=['memory', 'mental', 'mind', 'storage', 'magnetic', 'cache', 'psychological', 'semiconductor', 'transistor', 'random access', 'data storage']
        else:
            queries = self.config.queries
        s=searcher(self.dbname)
        if self.numusers >= 1:
            for q in queries:
                for userid in [x+1 for x in range(self.numusers)]:
                    wordids,rows = s.query(q, userid)

if __name__ == "__main__":
    import sys;sys.argv = ['', 'test0.testQueryIndian']
    test0=Test()
    unittest.main()
    
 