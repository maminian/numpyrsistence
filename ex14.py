# In theory if I'm looking for voids,
# I can start with just the nullspace of partial_2;
# nevermind constructing partial_3 for the moment.
#
# Let's explore on the polyhedra visualized
# in ex13!
#

import utils
import examples
import distmat2
import numpy as np
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from sklearn import metrics

import intmatop

#

for n in [5,6,7,8]:
    X = examples.thing2(n=n)
    #pc = point_cloud.Point_cloud(X)
    D2 = distmat2.Distmat2(X)
    idx = D2.get_subgraph(thresh=1.0001)
    pairs = D2.coords[idx]

    p1,p2 = utils.get_boundary_operators(pairs)

    null_p2 = intmatop.null(p2)

    print('Number of vertices: ', X.shape[0])
    print('Total number of 2-simplices (faces): ', p2.shape[1])
    print('Num. members in partial_2 nullspace vectors (faces): ', np.sum(null_p2!=0, axis=0) )
    print('\n=======================')
#

print('Results seem to be mixed... possible these might be degenerate cases')
