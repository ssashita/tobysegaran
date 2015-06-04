'''
Created on Feb 10, 2014

@author: ssashita
'''
from urlsimilarity import urlsimilarity

from pysqlite2 import dbapi2 as sqlite

def dbcleanup(dbname):
    con = sqlite.connect(dbname)
    if con != None:
        con.execute('drop table if exists urlsimilarity')
        con.commit()
        con.close()
        
if __name__ == '__main__':
    dbname = 'crawled.db'
    dbcleanup(dbname)
    urlsimilarityobj = urlsimilarity(dbname)
    urlsimilarityobj.createtables()
    urlsimilarityobj.fillsimilaritymatrix()
    con = sqlite.connect(dbname)
    data = con.execute('select rowid,url from urllist')
    f=open('urlword.dump','w')
    f.write('First the urls.........................\n')   
    for row in data:
        f.write(repr(row)+'\n')
#     f.write('And now the words.........................\n')
#     data = con.execute('select rowid,word from wordlist')
#     for row in data:
#         f.write(repr(row)+'\n')
#     f.write('And now the url info from wordlocation.........................\n')
#     data = con.execute('select distinct urlid from wordlocation')
#     for row in data:
#         f.write(repr(row)+'\n')
#     f.write('And now the word info from wordlocation.........................\n')
#     data = con.execute('select distinct wordid from wordlocation')
#     for row in data:
#         f.write(repr(row)+'\n')
#     f.close()
#     con.close()

#    urlsimilarityobj.geturlwordcount()