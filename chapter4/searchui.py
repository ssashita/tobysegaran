'''
Created on Mar 15, 2014

@author: ssashita
'''
from searchengine import searcher
# from urlsimilarity import urlsimilarity
# from runcrawl import dbcleanup as dbcleanup_runcrawl
# from runurlsimilarity import dbcleanup as dbcleanup_runurlsimilarity
# from runuserurlhits import dbcleanup as dbcleanup_runuserurlhits
# from runuserurlhits import createuserurlhitsfromsimilarurls, getuseridcountfromdbase
from Tkinter import *
import sys
import cconfigurator
import Tkinter
import tkMessageBox
import logging
#from ttk import Frame


config=cconfigurator.configure("test")

# def createconfig(ev):
#     config = cconfigurator.configure(dbnamevar.get())
#     tkMessageBox.showinfo("Configue", config.dbname)


def fillconfig():
    global config
    try :
        config = cconfigurator.configure(dbnamevar.get())
        config.loglevel=loglevel.get()
#         config.minsimilarityforclustering = float(minsimilarityforclustering.get())
        config.userurlhitscoresweight = float(userurlhitscoresweight.get())
        config.userid = userid.get()
    except:
        print "Error:", sys.exc_info()
        tkMessageBox.showerror("Input Error", sys.exc_info())
        raise
  
def firesearch():
    outputwidget.delete(1.0,END)
    fillconfig()
    s=searcher(config.dbname)
    q=queryvar.get()
    urllist=[]
    try:
        widlist,urlidlist = s.query(q,config.userid,config.userurlhitscoresweight)
        for urlid in urlidlist:
            url=s.geturlname(urlid)
            urllist.append(url)
        outputwidget.insert(END, '\n'.join(urllist))
    except:
        print "Error:", sys.exc_info()
        tkMessageBox.showerror("Input Error", sys.exc_info())
        raise
                    
    
    
appname = """Search UI"""

if __name__ == '__main__':
    #root = Tk("400x200+200+200")
    root = Tk("0:0")
    root.title(appname)
    frtop = Frame(root, relief=RAISED, borderwidth=1)
    frtop.pack()
    frconfig= Frame(root, relief=RAISED, borderwidth=1)
    frconfig.pack()
    frbottom = Frame(root, relief=RAISED, borderwidth=1)
    frbottom.pack()
    frtoptitle = StringVar()
    frtoptitle.set("QUERY STRING")
    Label(frtop,textvariable=frtoptitle, height=4, bg='light pink').pack(side=TOP)    
    

    
    frconfigtitle=StringVar()
    frconfigtitle.set("CONFIGURE SEARCH")
    Label(frconfig,textvariable=frconfigtitle, height=4, bg='light cyan').pack(fill=BOTH,side=TOP)
    
    
    queryvar = StringVar()
    queryvar.set("q u e r y   s t r i n g")
    queryentry= Tkinter.Entry(frtop,textvariable=queryvar)
    queryentry.bind('<Return>', firesearch)
    queryentry.pack(side=BOTTOM)
    
    
            
    frconfig1=Frame(frconfig, relief=RAISED, borderwidth=1)
    frconfig1.pack()
    dbnamelabel = StringVar()
    dbnamelabel.set("db name")
    Label(frconfig1,textvariable=dbnamelabel, height=4, bg='light cyan').pack(side=LEFT)
    dbnamevar = StringVar()
    dbnamevar.set("test")
    dbnameentry= Tkinter.Entry(frconfig1,textvariable=dbnamevar)
    dbnameentry.pack(side=LEFT)
    
    
    loglevel= StringVar()
    loglevel.set(logging.DEBUG)
    Label(frconfig1,text="Log Level", bg='light cyan').pack(side=LEFT)
    Tkinter.Entry(frconfig1,textvariable=loglevel).pack(side=LEFT)
    
         
    frconfig2=Frame(frconfig, relief=RAISED, borderwidth=1)
    frconfig2.pack()
    
#     minsimilarityforclustering=Tkinter.StringVar()
#     minsimilarityforclustering.set("0.9")
#     Label(frconfig2,text="minimum similarity for clustering (0.0<value<=1.0)", bg='light cyan').pack(side=LEFT)
#     Tkinter.Entry(frconfig2,textvariable=minsimilarityforclustering).pack(side=LEFT)  

    userurlhitscoresweight= Tkinter.StringVar()
    userurlhitscoresweight.set(2.0)
    Label(frconfig2,text="user url hit scores weight", bg='light cyan').pack(side=LEFT)
    Tkinter.Entry(frconfig2,textvariable=userurlhitscoresweight).pack(side=LEFT)      
    
    userid= IntVar()
    userid.set(1)
    Label(frconfig2,text="userid (int)", bg='light cyan').pack(side=LEFT)
    Tkinter.Entry(frconfig2,textvariable=userid).pack(side=LEFT)
      
    frconfig3=Frame(frconfig, relief=RAISED, borderwidth=1)
    frconfig3.pack()
    outputwidget = Tkinter.Text(frconfig3, bg='light yellow')
    outputwidget.pack()
    
    Button(frbottom,text="OK", fg="red",bg="green", relief=SOLID, command=firesearch).pack(fill=BOTH, side = RIGHT)  
    Button(frbottom,text="CANCEL", fg="green", bg="RED", relief=GROOVE, command=lambda: root.destroy()).pack(fill=BOTH, side = RIGHT)
    root.mainloop()
    
