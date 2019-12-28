import examples
import point_cloud
import utils
import distmat2

import numpy as np
from matplotlib import pyplot

from scipy import linalg as spla

#
X = examples.house2()
D2 = distmat2.Distmat2(X)
pc = point_cloud.Point_cloud(X)

#
edge_idx = D2.get_subgraph(thresh=1.)
pairs = D2.coords[edge_idx]

loops = utils.get_K3s(pairs)
# loop_coords = [X[l] for l in loops] # If I wanted I could do this

# Don't need an ordering for the K3 loops, but register it here
# just in case for later.
_loops = list(loops)

# Definitely DO need to specify an ordering for the edges.
# It's probably going to be a good idea to build it in ascending
# order of distance (which we already have in D2).
_edges = list(pairs)
_edgedict = {tuple(list(row)):j for j,row in enumerate(_edges)}

# now build the boundary operator partial_2.
partial_2 = np.zeros( (len(_edges), len(_loops)), dtype=int )
for j,_l in enumerate(_loops):
    partial_2[_edgedict[(_l[0],_l[1])],j] = 1
    partial_2[_edgedict[(_l[0],_l[2])],j] = -1
    partial_2[_edgedict[(_l[1],_l[2])],j] = 1
#

# build the boundary operator partial_1.
# Just use the provided ordering for vertices.
partial_1 = np.zeros( (len(X), len(_edges)), dtype=int )
for j,_e in enumerate(_edges):
    partial_1[_e[0],j] = 1
    partial_1[_e[1],j] = -1
#

# Build orthonormal bases for the kernel of partial_1
# and the image of partial_2.
#
# Use built-in functions for now - these are really flawed
# for this task since this really needs to be done with
# integers for interpretability.
#
ker_p1 = spla.null_space(partial_1)
Q,R = np.linalg.qr(partial_2)

im_p2 = Q

# Get a basis for the kernel of partial_1 orthogonal to the space
# spanned by the image of partial_2.
thing = np.dot( utils.orth_proj(im_p2), ker_p1 )

#
# **************************************
#
# NOTE: operations included column operations including
# working with partial_2 directly.
#
# **************************************
#
# This time, the reduced form for thing was
# [0,0,1,-1,0,1,0,0,1], and two columns of zeros.
#
print('loop: ')
for j,dir in enumerate([0,0,1,-1,0,1,0,0,1]):
    if dir==0:
        continue
    print( _edges[j][::dir] )
