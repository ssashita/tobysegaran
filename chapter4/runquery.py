'''
Created on Feb 16, 2014

@author: ssashita
A query is to be given as 
 python runquery.py 1 functional programming
 {1 is the userid, and the rest are the query words} 
'''

from searchengine import searcher
import sys
import cconfigurator

if __name__ == '__main__':
    config = cconfigurator.configure('crawled.db')
    listargs=[]
    if len(sys.argv) > 2:
        for arg in sys.argv[2:]:
            listargs.append(arg)
        s=searcher('crawled.db')
        s.query(' '.join([str(x) for x in listargs]),sys.argv[1])
    else:
        print("At least 3 args required. Second one is the userid and rest are the query words")