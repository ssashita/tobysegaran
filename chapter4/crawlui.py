'''
Created on Mar 15, 2014

@author: ssashita
'''
from searchengine import crawler,searcher
from urlsimilarity import urlsimilarity
from runcrawl import dbcleanup as dbcleanup_runcrawl
from runurlsimilarity import dbcleanup as dbcleanup_runurlsimilarity
from runuserurlhits import dbcleanup as dbcleanup_runuserurlhits
from runuserurlhits import createuserurlhitsfromsimilarurls, getuseridcountfromdbase
import cconfigurator
from Tkinter import *
import Tkinter
import tkMessageBox
import logging
#from ttk import Frame

def dbcleanup(dbname):
    dbcleanup_runcrawl(dbname)
    dbcleanup_runurlsimilarity(dbname)
    dbcleanup_runuserurlhits(dbname)

config=cconfigurator.configure("test")

URLPREFIX="http://"
def createconfig(ev):
    global config
    config = cconfigurator.configure(dbnamevar.get())
    tkMessageBox.showinfo("Configue", config.dbname)


def setstage():
    global config
    config.startfrom = stage.get()
    tkMessageBox.showinfo("Stage", config.startfrom)

def addSeed():
    global seedlist, seedentrylist, seedlist
    seedlist.append(StringVar())
    numseeds = len(seedlist)-1
    seedlist[numseeds].set(URLPREFIX)
    seedentrylist.append(Tkinter.Entry(frseed,textvariable=seedlist[numseeds]))
    seedentrylist[numseeds].pack()

def getseedurls():
    urls=[]
    for s in seedlist:
        if s.get().strip().startswith(URLPREFIX) and s.get().strip() != URLPREFIX:
            urls.append(s.get())
    return urls

def fillconfig():
    global config
    try :
        setstage()
        config.dbname= dbnamevar.get()
        config.seed=getseedurls()
        config.crawlerdepth = crawlerdepth.get()
        config.loglevel=loglevel.get()
        config.minclusterlength = int(minclusterlength.get())
        config.minsimilarityforclustering = float(minsimilarityforclustering.get())
        config.numusers = numusers.get()
        config.startfrom = stage.get()
        config.userurlhitscoresweight = float(userurlhitscoresweight.get())
    except:
        print "Error:", sys.exc_info()
        tkMessageBox.showerror("Input Error", sys.exc_info())
        raise
    createdbase(config)
    
def createdbase(config):
    if config.startfrom <= cconfigurator.startfromcrawling:
        dbcleanup_runcrawl(config.dbname)
        seed=config.seed
        crawled=crawler(config.dbname)
        crawled.createindextables()
        crawled.crawl(seed, depth=config.crawlerdepth)
        crawled.calculatepagerank()
        crawled.con.execute('select * from pagerank,urllist where pagerank.urlid=urllist.rowid order by score desc')
    
    if config.startfrom <= cconfigurator.startfromurlsimilarity:
        dbcleanup_runurlsimilarity(config.dbname)
        urlsimilarityobj = urlsimilarity(config.dbname)
        urlsimilarityobj.createtables()
        urlsimilarityobj.fillsimilaritymatrix()
    if config.startfrom <= cconfigurator.startfromuserurlhits:
        dbcleanup_runuserurlhits(config.dbname)
        config.numusers= createuserurlhitsfromsimilarurls(config.dbname, minclusterlength=config.minclusterlength,
                                                          minsimilarity=config.minsimilarityforclustering, loglevel=config.loglevel)
        config.numusers = getuseridcountfromdbase(config.dbname)
                    
    
    
appname = """Crawl UI"""

if __name__ == '__main__':
    root = Tk("400x200+200+200")
    root.title(appname)
    frtop = Frame(root, relief=RAISED, borderwidth=1)
    frtop.pack()
    frseed= Frame(root, relief=RAISED, borderwidth=1)
    frseed.pack()
    frbottom = Frame(root, relief=RAISED, borderwidth=1)
    frbottom.pack()
    frtoptitle = StringVar()
    frtoptitle.set("CONFIGURE PARAMETERS")
    Label(frtop,textvariable=frtoptitle, height=4).pack(side=TOP)    
    

    
    frseedtitle=StringVar()
    frseedtitle.set("CONFIGURE SEED URLS")
    Label(frseed,textvariable=frseedtitle, height=4).pack(fill=BOTH,side=TOP)
    
    seedentrylist=[]
    seedlist=[StringVar(), StringVar()]
    seedlist[0].set(URLPREFIX)
    seedlist[1].set(URLPREFIX)
    seedentrylist.append(Tkinter.Entry(frseed,textvariable=seedlist[0]))
    seedentrylist.append(Tkinter.Entry(frseed,textvariable=seedlist[1]))
    Button(frseed,text="Add",bg="yellow",fg="red", relief=SOLID,command=addSeed).pack()
    
    for s in seedentrylist: s.pack()
    
    frtopdbname = Frame(frtop, relief=RAISED, borderwidth=1)
    frtopdbname.pack()
    Label(frtopdbname,text="DB name").pack(side=LEFT)
    dbnamevar = StringVar()
    dbnamevar.set("test")
    dbnameentry= Tkinter.Entry(frtopdbname,textvariable=dbnamevar)
    dbnameentry.bind('<Return>', createconfig)
    dbnameentry.pack(side=LEFT)
    
    frtopstage = Frame(frtop, relief=RAISED, borderwidth=1)
    frtopstage.pack()
    stage=IntVar()
    Radiobutton(frtopstage,text="startfromuserurlhits",value=cconfigurator.startfromuserurlhits,variable=stage, command=setstage).pack(side=LEFT)
    Radiobutton(frtopstage,text="startfromurlsimilarity",value=cconfigurator.startfromurlsimilarity,variable=stage, command=setstage).pack(side=LEFT)
    Radiobutton(frtopstage,text="startfromcrawling",value=cconfigurator.startfromcrawling,variable=stage, command=setstage).pack(side=LEFT)
    
            
    frtoprest1=Frame(frtop, relief=RAISED, borderwidth=1)
    frtoprest1.pack()
    crawlerdepth = IntVar()
    crawlerdepth.set(2)
    Label(frtoprest1,text="Crawler Depth").pack(side=LEFT)
    Tkinter.Entry(frtoprest1,textvariable=crawlerdepth).pack(side=LEFT)
    
    loglevel= IntVar()
    loglevel.set(logging.DEBUG)
    Label(frtoprest1,text="Log Level").pack(side=LEFT)
    Tkinter.Entry(frtoprest1,textvariable=loglevel).pack(side=LEFT)
    
    
    minclusterlength= IntVar()
    minclusterlength.set(10)
    Label(frtoprest1,text="min Cluster Length").pack(side=LEFT)
    Tkinter.Entry(frtoprest1,textvariable=minclusterlength).pack(side=LEFT)   
         
    frtoprest2=Frame(frtop, relief=RAISED, borderwidth=1)
    frtoprest2.pack()
    
    minsimilarityforclustering=Tkinter.StringVar()
    minsimilarityforclustering.set("0.9")
    Label(frtoprest2,text="minimum similarity for clustering (0.0<value<=1.0)").pack(side=LEFT)
    Tkinter.Entry(frtoprest2,textvariable=minsimilarityforclustering).pack(side=LEFT)  

    userurlhitscoresweight= Tkinter.StringVar()
    userurlhitscoresweight.set(2.0)
    Label(frtoprest2,text="user url hit scores weight").pack(side=LEFT)
    Tkinter.Entry(frtoprest2,textvariable=userurlhitscoresweight).pack(side=LEFT)      
    
    numusers= IntVar()
    numusers.set(20)
    Label(frtoprest2,text="number of users").pack(side=LEFT)
    Tkinter.Entry(frtoprest2,textvariable=numusers).pack(side=LEFT)
    
#     frtoprest3=Frame(frtop, relief=RAISED, borderwidth=1)
#     frtoprest3.pack()
    
        
        
    Button(frbottom,text="OK", fg="red",bg="green", relief=SOLID, command=fillconfig).pack(fill=BOTH, side = RIGHT)  
    Button(frbottom,text="CANCEL", fg="green", bg="RED", relief=GROOVE, command=lambda: root.destroy()).pack(fill=BOTH, side = RIGHT)
    root.mainloop()
    