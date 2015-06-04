import numpy as np
import logging

loglevel = logging.DEBUG
log = logging.Logger("collaborativefiltering", level=loglevel)

def initlog(loglevel=logging.DEBUG):
  global log
  log = logging.Logger("collaborativefiltering", level=loglevel)
  fh = logging.FileHandler('collaborativefiltering.log')
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  fh.setFormatter(formatter)
  log.addHandler(fh)
  
def initparamsandcoords(prefs, dimension):
    '''
    From prefs create and return arrays of parameters and coordinates 
    for feeding to a gradient descent or other optimization method
    Imagine a table of word counts
          url1 url2 url3 ...
    word1 
    word2
    word3

    paramters are specific to each column and coordinates are specific to each row
    '''
    initlog()
    urllist =[]
    wordset= set([])
    for url in prefs:
        urllist.append(url)
        wordset.update(prefs[url].keys())
    wordlist = list(wordset)

    initparamvals = [np.random.random() for i in range(dimension +1)]
    initcoordvals = [np.random.random() for i in range(dimension)]
    params=np.array([initparamvals for i in range(len(urllist))],dtype=float)       
    coords=np.array([initcoordvals for i in range(len(wordlist))],dtype=float)

    return params,coords,urllist,wordlist

def costfunction(x, *args):
    prefs,dimension,users,movielist, lamda = args
    nusers = len(users)
    nmovies = len(movielist)
    dimension1 = 1 + dimension
    i = x.size
    params = x[0:(nusers*dimension1)].reshape( (nusers,dimension1))
    coords = x[(nusers*dimension1):].reshape( ( nmovies, dimension) )
    J = 0.
    lamdaerror = 0.
    for user in prefs:
        i= users.index(user)
        movies = prefs[user]
        lamdaerror = lamdaerror + sum(params[i]**2)
        for mv in movies:
            j= movielist.index(mv)
            coordsextended=np.array([1.],dtype=float)
            coordsextended = np.concatenate((coordsextended,coords[j]))
            calculatedrank = np.dot(params[i], coordsextended)
            error = 0.5*(calculatedrank - prefs[user][mv])**2
            lamdaerror = lamdaerror + sum(coords[j]**2)
            J = J + error
    J = J + 0.5*lamda*lamdaerror
    return J

def gradientfunction(x, *args) :
    prefs,dimension,users, movielist,lamda = args
    nusers = len(users)
    nmovies = len(movielist)
    dimension1 = 1 + dimension
    params = x[0:nusers*dimension1].reshape( (nusers,dimension1))
    coords = x[nusers*dimension1:].reshape( ( nmovies, dimension) )
    coordgradlist = np.zeros(dimension*nmovies, dtype=float)
    paramgradlist = np.zeros(dimension1*nusers, dtype=float)
    for user in prefs:
        i= users.index(user)
        movies = prefs[user]
        grads = np.zeros(dimension1,dtype=float)
        for mv in movies:
            j= movielist.index(mv)
            coordsextended = np.array([1.], dtype=float)
            coordsextended = np.concatenate((coordsextended,coords[j]))
            calculatedtemps= \
                       (np.dot(params[i],coordsextended) - prefs[user][mv]) * np.array(coordsextended,float)
            grads = grads + calculatedtemps
        grads = grads + lamda*params[i]
        np.add.at(paramgradlist, range(i*dimension1,(i+1)*dimension1),grads)
    for mv in movielist:
        j = movielist.index(mv)
        userlist = [user for user in prefs if mv in prefs[user]]
        grads = np.zeros(dimension,dtype=float)
        coordsextended = np.array([1.], dtype=float)
        coordsextended = np.concatenate((coordsextended,coords[j]))
        for user in userlist:
            i = userlist.index(user)
            calculatedtemps= \
               (np.dot(params[i],coordsextended )-prefs[user][mv]) * params[i,1:]
            grads = grads + calculatedtemps
        grads = grads + lamda*coords[j]
        np.add.at(coordgradlist, range(j*dimension,(j+1)*dimension),grads)

    gradarr = np.concatenate((paramgradlist,coordgradlist))
    log.debug('gradarr is ' + repr(gradarr))
    return gradarr    

