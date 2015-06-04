'''
Created on Feb 16, 2014

@author: ssashita
'''

import searchengine
if __name__ == '__main__':
    crawler=searchengine.crawler('crawled.db')
    crawler.calculatepagerank()
    cur=crawler.con.execute('select * from pagerank,urllist where pagerank.urlid=urllist.rowid order by score desc')
    for i in range(100): print cur.next()
    