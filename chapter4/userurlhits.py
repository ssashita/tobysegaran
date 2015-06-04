'''
Created on Feb 9, 2014

@author: ssashita
'''
from searchengine import searcher
from pysqlite2 import dbapi2 as sqlite

class userurlhits:
#Store url hits per user

    def __init__(self, dbname):
        #self.searcher = searcher(dbname)
        self.con=sqlite.connect(dbname)
        #self.con = self.searcher.con    
    
    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()
    
    def createtables(self):
        self.con.execute('create table user(userinfo)')
        self.con.execute('create table userurlhits(userid,urlid,hits integer)')
        self.con.execute('create index userurlhitsidx on userurlhits(userid)')
        self.con.commit()
        
    def filltables(self,numusers=20):
        for i in range(numusers):
            self.con.execute('insert into user(userinfo) values(%d)'%(i))
        self.con.commit()
        #Calculate url similarity matrix
 

        