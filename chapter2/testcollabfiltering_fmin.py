from collabfiltering import *
from scipy.optimize import fmin_bfgs
from scipy.optimize import fmin
from scipy.optimize import fmin_cg
import pdb


# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


def initlog(loglevel=logging.ERROR):
  log = logging.Logger("collaborativefiltering", level=loglevel)
  fh = logging.FileHandler('collaborativefiltering.log')
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  fh.setFormatter(formatter)
  log.addHandler(fh)
  return log

def verify():
  for user in critics:
    i = userlist.index(user)
    for movie in critics[user]:
      j = movielist.index(movie)
      print user , movie, critics[user][movie], np.dot(params[i],np.concatenate((np.array([1.],dtype=float), coords[j])))
    
if __name__ == '__main__':    
    pdb.set_trace()
    log=initlog()
    dimension = 4
    lamda=0.0
    params, coords,userlist,movielist = initparamsandcoords(critics, dimension)
    xx = params.reshape(params.size).tolist()
    xxx = coords.reshape(coords.size).tolist()
    xx.extend(xxx)
    i=len(xx)
    x = np.array(xx,dtype=float)
    xprev=None
#    def callback(xk):
#        global xprev
#        if xprev != None :
#            print "mean sq sum  error is " , sum((xk-xprev)**2)/xk.size
#        xprev = xk
    xopt=fmin(costfunction,x,args=(critics, dimension,userlist,movielist,lamda), maxiter=100)
    log.debug('xopt is \n' +  repr(xopt))
    nu = len(userlist)
    nm = len(movielist)
    dimension1 = dimension + 1
    params = xopt[0:(nu*dimension1)].reshape((nu,dimension1))
    coords = xopt[(nu*dimension1):].reshape((nm,dimension))
    #print params
    #print coords
    log.debug('params are \n' + repr(params))
    log.debug('coords are \n' + repr(coords))
    verify()
 #   print 'fopt ', fopt
 #   print 'gopt ',gopt
 #   print 'Bopt ' , Bopt
 #   print 'funccalls ', funccals
 #   print 'gradcalls ', gradcalls
 #   print 'warnflag ', warnflag
 #   print 'allvecs ',allvecs



