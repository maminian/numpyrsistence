import utils
import examples
import distmat2
import intmatop
import numpy as np
from matplotlib import pyplot

#
# Next step in the full pipeline...
# intmatop contains the row reduction operations over the integers.
# still need to do some smoothing out for the last steps between
# constructing the graph and getting the boundary operators.
#

#X = examples.house()
X = examples.noisy_circle()
D = distmat2.Distmat2(X)
idx = D.get_subgraph(thresh=0.74)
pairs = D.coords[idx]

p1,p2 = utils.get_boundary_operators(pairs)

thing = np.array(p1, dtype=int)
intmatop.rref(thing, verbosity=1)

tscale = max(abs(thing.min()), abs(thing.max()))

# visualize things for fun.
fig,ax = pyplot.subplots(1,1)
ax.matshow(thing, vmin=-tscale, vmax=tscale, cmap=pyplot.cm.bwr)

ax2 = utils.vis_cloud(X, thresh=0.74)

# what significance do the pivots have, if any?
pivots = []
for i in range(thing.shape[0]):
    for j in range(thing.shape[1]):
        if thing[i,j]!=0:
            pivots.append([i,j])
            edge = pairs[j]
            xxyy = X[edge]
            ax2.plot(xxyy[:,0], xxyy[:,1], c='w', lw=2)
            break
print('\nPivots seem to associate with edges constructing a spanning tree of the graph... maybe not surprising?')

fig.show()
fig2.show()
pyplot.ion()
