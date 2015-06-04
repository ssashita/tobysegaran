'''
Created on Mar 1, 2014

@author: ssashita
'''
import logging

startfromcrawling=0
startfromurlsimilarity=1
startfromuserurlhits=2

class configure:
    def __init__(self, dbname):
        self.dbname = dbname
        self.crawlerdepth=2
        self.loglevel=logging.DEBUG
        self.minclusterlength=10
        self.minsimilarityforclustering=0.9
        self.numusers = 20
        self.startfrom=startfromuserurlhits
        self.seed=["http://en.wikipedia.org/wiki/India",
                   "http://en.wikipedia.org/wiki/Native_Americans_in_the_United_States"]
        self.cleanup=False
        self.queries=None
        self.userurlhitscoresweight=2.0
        self.userid=1
        