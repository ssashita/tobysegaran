'''
Created on Feb 9, 2014

@author: ssashita
'''
#from searchengine import searcher
from pysqlite2 import dbapi2 as sqlite
from recommendations import  topMatches
#from logging import getLogger,Logger
import logging



def belongsto(urlid1, urlid2, clusterarray,dicturlsim=None):
    #count =0
    cluster=None
    for cluster in clusterarray:
        if urlid1 in cluster or (dicturlsim != None) and cluster.issubset(dicturlsim[urlid1]):
            if urlid2 in cluster or (dicturlsim != None) and cluster.issubset(dicturlsim[urlid2]):
                return cluster            
    return None

class urlsimilarity:

    def __init__(self, dbname,loglevel=logging.DEBUG):
        self.con=sqlite.connect(dbname)
        self.log = logging.Logger("recommendation.urlsimilarity", level=loglevel)
        fh = logging.FileHandler('urlsimilarity.log')
        #fh.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.log.addHandler(fh)
    
    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()
    
    def createtables(self):
        self.con.execute('create table urlsimilarity(urlid1,urlid2,similarity real)')
        self.con.execute('create index urlsimilarityidx on urlsimilarity(urlid1)')
        self.dbcommit()

 
    def geturlwordcount(self):
            
        wordinfolst = self.con.execute('select  wordid, count(*) from wordLocation group by wordid')
        dictObj = {}
        #dumpfile = open("dump.dump","w")
        for wordinfo in wordinfolst:
            els=self.con.execute('select urlid, count(*) from wordlocation where wordid = %s group by urlid order by urlid'% (wordinfo[0]))
            #dumpfile.write(repr(els) + '\n')
            self.log.debug(repr(els) + '\n')
            for el in els:
                url = el[0]
                if url not in dictObj:
                    dictObj[url] = {}
                dictObj[url][wordinfo[0]] = el[1]

        for el in dictObj:
            #sumVal =0.0
            den =1.0*max([1.0]+[x for x in dictObj[el].values()])
            #for wordid in dictObj[el]:
                #sumVal += dictObj[el][wordid]
            #if sumVal == 0.0: sumVal=1.0
            
            #dumpfile.write(str(el) + ":\n")
            self.log.debug(str(el) + ":\n")
            for wordid in dictObj[el]:
                dictObj[el][wordid] /= den
                dictObj[el][wordid] *= 100.0
            #dumpfile.write(repr(dictObj[el]) + "\n")
            self.log.debug((repr(dictObj[el]) + "\n"))
        #dumpfile.close()      
        return dictObj
                
    def fillsimilaritymatrix(self):
        dictObj = self.geturlwordcount()
        #dumpfile = open("urlsim.dump","w")
        for url in self.con.execute('select distinct urlid from wordlocation order by urlid'):
            urllist=topMatches(dictObj,url[0],n=50) 
            print(repr(url[0]) + ":\n" + repr(urllist))         
            self.log.debug(repr(url[0]) + ":\n" + repr(urllist))     
            for u in urllist:
                self.con.execute('insert into urlsimilarity(urlid1,urlid2,similarity) values(%s,%s,%f)'%(url[0],u[1],u[0]))
                #dumpfile.write(repr(url[0]) + "," + repr(u[1]) + ',' + repr(u[0]) + '\n')
                self.log.debug(repr(url[0]) + "," + repr(u[1]) + ',' + repr(u[0]) + '\n')                
        self.dbcommit()
        #dumpfile.close()
   
    def formsimilaritydictionary(self, results ):
        dicturlsim={}
        for result in results:
            if result[0] not in dicturlsim:                
                dicturlsim[result[0]] = set([result[1]])
            else:
                dicturlsim[result[0]].add(result[1])
        return dicturlsim
                
    def createurlsimilaritysets(self, minsimilarity=0.9):
        results=self.con.execute('select urlid1,urlid2 from urlsimilarity where similarity > (%f) order by urlid1'%(minsimilarity)).fetchall()
        dicturlsim = self.formsimilaritydictionary(results)
        
        clusters=[]
            
        for result in results:
            cluster = belongsto(result[0], result[1], clusters, dicturlsim)
            if cluster == None:
                clusters.append(set([ result[0], result[1] ]))
            else:
                cluster.add(result[0])
                cluster.add(result[1])
        self.log.debug("Clusters are :\n")
        for cluster in clusters:
            self.log.debug("cluster\n")
            self.log.debug(repr(cluster))
                
        return clusters                   
      

        
