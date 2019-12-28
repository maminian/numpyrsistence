import ex2
import point_cloud
import numpy as np
from matplotlib import pyplot

X = ex2.X
pc = point_cloud.Point_cloud(X)

D2 = ex2.Distmat2(X)

nr = 220

# choose arbitrary threshold
r1 = D2.distances[D2.order[nr]]
r2 = D2.distances[D2.order[nr+1]]
thresh = (r1+r2)/2.

# we're interested in the subgraph associated
# with this threshold.

pairs_idx = np.where(D2.distances <= thresh)[0]
pairs = D2.coords[pairs_idx]
which = np.unique(pairs)

if __name__=="__main__":
    pc.visualize()
    pc.draw_ball(which, thresh/2., c=[0.5,0,0.5])

    for j,o in enumerate( D2.order[:nr] ):

        iijj = D2.coords[o]
        xxyy = X[iijj]
        pc.ax.plot(xxyy[:,0], xxyy[:,1], c=pyplot.cm.tab10(j%10), lw=2)


    pc.ax.axis('square')
    pyplot.ion()
