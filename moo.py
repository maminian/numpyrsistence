import numpy as np
from matplotlib import pyplot

n = 20
eps = 0.1
np.random.seed(0)

th = np.linspace(0,2*np.pi,n)

X = np.array([np.cos(th),np.sin(th)]).T + eps*np.random.randn(n,2)

fig,ax = pyplot.subplots(1,1)

ax.scatter(X[:,0], X[:,1], c='k', s=80)

# quick and dirty distance matrix.
D = np.array([[np.linalg.norm(x-y) for x in X] for y in X])

dmin,dmax = D[D!=0].min(),D.max()

###################################

fig.show()
pyplot.ion()
