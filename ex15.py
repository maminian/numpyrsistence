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

n=100

X = examples.noisy_sphere(n=n)
pc = point_cloud.Point_cloud(X)
D2 = distmat2.Distmat2(X)

# some experimenting shows this is okay for n=100.
thresh = np.median(D2.distances)/2.

ax = utils.vis_cloud(X, thresh=thresh, draw_balls=False, draw_loops=False,)

idx = D2.get_subgraph(thresh=thresh)
pairs = D2.coords[idx]

# Construct the operators and the nullspaces.
p1,p2 = utils.get_boundary_operators(pairs)

null_p1 = intmatop.null(p1)
null_p2 = intmatop.null(p2)

#########
# visualize p1 nullspace element.
#
o = np.argsort(-np.sum(null_p1!=0, axis=0))
which_p1 = np.where(null_p1[:,o[0]])[0]

for e in np.unique(which_p1):
    vidx = np.where(p1[:,e])[0]
    ax.plot(X[vidx,0], X[vidx,1], X[vidx,2], c='r', lw=10, alpha=0.7)


#####
# visualize p2 nullspace element.
#

# Find and look at the densest nullspace element.
o = np.argsort(-np.sum(null_p2!=0, axis=0))

# which faces are involved?
which = np.where(null_p2[:,o[0]])[0]

# Which edges are involved with those faces?
edge_idx =  np.unique( np.where(p2[:,which])[0] )

# Plot every single edge involved.
for e in edge_idx:
    vidx = np.where(p1[:,e])[0] # vertex pair for the edge.
    ax.plot(X[vidx,0], X[vidx,1], X[vidx,2], c='k', lw=10, alpha=0.7)

pyplot.ion()
