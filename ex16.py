# Repeat the experiment for searching for voids,
# but with a noisy sphere.
#

import utils
import examples
import distmat2
import numpy as np
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from sklearn import metrics

import intmatop
import point_cloud

#

#n=200
nu=20   # xy direction
nv=12   # z direction

X = examples.noisy_torus(nu=nu, nv=nv, eps=0.0, permute=True)
pc = point_cloud.Point_cloud(X)
D2 = distmat2.Distmat2(X)

# some experimenting shows this is okay for n=500.
thresh = np.quantile(D2.distances, 0.03)

ax = utils.vis_cloud(X, thresh=thresh, draw_balls=False, draw_loops=False)
#fig = pyplot.figure()
#ax = fig.add_subplot(111, projection='3d')


idx = D2.get_subgraph(thresh=thresh)
pairs = D2.coords[idx]

# Construct the operators and the nullspaces.
p1,p2 = utils.get_boundary_operators(pairs)

null_p1 = intmatop.null(p1)
#null_p2 = intmatop.null(p2)

o = np.argsort(-np.sum(null_p1!=0, axis=0))


fig = pyplot.gcf()
fig.set_figwidth(8)
fig.set_figheight(6)
pyplot.ion()
fig.show()

line_coll = []

for oi in o:
    which_p1 = np.where(null_p1[:,oi])[0]

    for lc in line_coll[::-1]:
        lc.remove()

    line_coll = []
    for e in np.unique(which_p1):
        vidx = np.where(p1[:,e])[0]
        lc = ax.plot(X[vidx,0], X[vidx,1], X[vidx,2], c='r', lw=10, alpha=0.7)
        line_coll.append(lc[0])
    #
    pyplot.pause(0.5)
#

#ax.scatter(X[:,0], X[:,1], X[:,2])
