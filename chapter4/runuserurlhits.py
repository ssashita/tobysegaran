'''
Created on Feb 15, 2014

@author: ssashita
'''
import sys
from pysqlite2 import dbapi2 as sqlite
from userurlhits import userurlhits
from urlsimilarity import urlsimilarity
from random import randint
import logging

def dbcleanup(dbname):
    con = sqlite.connect(dbname)
    if con != None:
        con.execute('drop table if exists user')
        con.execute('drop table if exists userurlhits')
        con.commit()
        con.close()
        
def getuseridcountfromdbase(dbname):
    con = sqlite.connect(dbname)
    numusers=0
    if con != None:
        result = con.execute('select count(*) from user').fetchone()
        if result != None:
            numusers = result[0]
    con.close()
    return numusers
        
def  createuserurlhitsfromsimilarurls(dbname, minclusterlength=10,minsimilarity=0.9,loglevel=logging.DEBUG):
    ll=0
    dbcleanup(dbname)
    userhits=userurlhits(dbname)
    userhits.createtables()
    urlsim=urlsimilarity(dbname,loglevel)
    clusters=urlsim.createurlsimilaritysets(minsimilarity=minsimilarity)
    #choose only those sets with at least 10 urls
    bigclusters=[c for c in clusters if len(c) >= minclusterlength]
    ll=len(bigclusters)
    if ll == 0:
        print 'No big enough clusters to create user with focused url type preference\n'
    else:
        userhits.filltables(numusers=ll)
        con=sqlite.connect(dbname)
        useridlist=con.execute('select rowid from user')
        count=-1
        for _userid in useridlist:
            count +=1
            userid=_userid[0]
            cluster=bigclusters[count]
            lenc=len(cluster)
            clusterlist = list(cluster)
            dicturlcounts={}            
            for i in range(1000):
                j=randint(0,lenc-1)
                if dicturlcounts.has_key(clusterlist[j]):
                    dicturlcounts[clusterlist[j]] += 1
                else:
                    dicturlcounts[clusterlist[j]]=1
            for urlid in dicturlcounts:
                con.execute('insert into userurlhits(userid,urlid,hits) values(%d,%d,%d)'%
                            (userid,urlid,dicturlcounts[urlid]))
        con.commit()
        con.close()
        return ll

              
if __name__ == '__main__':
    dbname='crawled.db'
    dbcleanup(dbname)
    createuserurlhitsfromsimilarurls(dbname,logging.DEBUG)
            
