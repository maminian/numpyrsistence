# Doing a couple things new this example:
#
# 1. Different data structure for
#    distance matrix to facilitate
#    access of points
# 2. Iterating the first three smallest
#    distances and associated points using this
#    approach.
#

import point_cloud
import ex1
import numpy as np
from matplotlib import pyplot

n = 50
eps = 0.3
np.random.seed(123234)

th = np.linspace(0,2*np.pi,n)
X = np.array([np.cos(th),np.sin(th)]).T + eps*np.random.randn(n,2)

reorder = np.random.permutation(n)
X = X[reorder]

# new and shiny distance matrix class.
class Distmat2:
    def __init__(self,Dmat):
        n,d = np.shape(Dmat)
        self.n = n
        self.d = d

        self._nc = (self.n*(self.n-1))//2
        self.coords = np.zeros( (self._nc, 2), dtype=int )
        self.distances = np.zeros( self._nc, dtype=float )

        if self.n!=self.d:
            # assume a point cloud was passed;
            # compute the euclidean distance matrix.
            from sklearn import metrics
            Dmat2 = metrics.pairwise_distances(Dmat, metric='euclidean')
        else:
            Dmat2 = Dmat
        #

        idx = 0
        for i in range(self.n):
            for j in range(i+1,self.n):
                self.coords[idx] = (i,j)
                self.distances[idx] = Dmat2[i,j]
                idx += 1

        self.order = np.argsort(self.distances)

        return
    #
#

if __name__=="__main__":
    import numpy as np
    import point_cloud
    from matplotlib import pyplot
    import ex1

    pc = point_cloud.Point_cloud(X)

    D2 = Distmat2(X)
    order = np.argsort(D2.distances)

    pc.visualize()
    nr = 12
    base_color = np.array([0.5,0,0.5])
    for j,o in enumerate( order[:nr] ):
        if j==nr-1:
            pc.draw_balls(D2.distances[o]/2., c=base_color)

        iijj = D2.coords[o]
        xxyy = X[iijj]
        pc.ax.plot(xxyy[:,0], xxyy[:,1], c=pyplot.cm.tab10(j%10), lw=2)

    #
    pc.ax.axis('square')
    pc.fig.show()
    pyplot.ion()
