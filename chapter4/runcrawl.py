'''
Created on Feb 10, 2014

@author: ssashita
'''
import searchengine
from pysqlite2 import dbapi2 as sqlite

def dbcleanup(dbname):
    con = sqlite.connect(dbname)
    if con != None:
        con.execute('drop table if exists urllist')
        con.execute('drop table if exists wordlist')
        con.execute('drop table if exists wordlocation')
        con.execute('drop table if exists link')
        con.execute('drop table if exists linkwords')
        con.commit()
        con.close()
        
if __name__ == '__main__':
    pagelist=['http://lxml.de/parsing.html', 'http://kiwitobes.com']

    dbcleanup('crawled.db')
    crawler=searchengine.crawler('crawled.db')
    crawler.createindextables()
    crawler.crawl(pagelist)