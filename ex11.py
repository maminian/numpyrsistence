import utils
import examples
import distmat2
import intmatop
import numpy as np
from matplotlib import pyplot

pyplot.ion()

#
# Return to the noisy circle. Can we identify Ker(partial_1) successfully?
#

#X = examples.house()
X = examples.noisy_circle(permute=True)
D = distmat2.Distmat2(X)
idx = D.get_subgraph(thresh=0.74)
pairs = D.coords[idx]

p1,p2 = utils.get_boundary_operators(pairs)

nullspace = intmatop.null(p1)

fig2,ax2 = pyplot.subplots(2,3, figsize=(12,8), sharex=True, sharey=True)
fig2.tight_layout()

#fig2,ax2 = utils.vis_cloud(X, thresh=0.74, draw_edges=False, draw_loops=False)

if False:
    # switch for a neato animation!
    for i,column in enumerate( nullspace.T ):
        # if i!=0:
        #     break
        line_set = []
        for j,c in enumerate(column):   # Jimmy Carter
            if c!=0:
                xxyy = X[pairs[j]]
                l = ax2.plot(xxyy[:,0], xxyy[:,1], c='w', lw=2)
                line_set.append( l[0] )
        #
        pyplot.pause(0.1)
        for l in line_set[::-1]:
            l.remove()
    #
#

# for now, look for the largest basis elements.
cycle_lengths = np.sum(nullspace!=0, axis=0)
order = np.argsort(-cycle_lengths)
colors = [np.sqrt(pyplot.cm.tab10(j)) for j in range(6)]

for idx,o in enumerate(order[:6]):
    axi,axj = idx//3,idx%3
    utils.vis_cloud(X, thresh=0.74, draw_edges=False, draw_loops=False, axh=ax2[axi,axj])
    column = nullspace[:,o]
    for j,c in enumerate(column):   # Jimmy Carter
        if c!=0:
            xxyy = X[pairs[j]]
            ax2[axi,axj].plot(xxyy[:,0], xxyy[:,1], c=colors[idx], lw=5)
    #

    # plot vertex indexes
    vertices = np.unique(pairs[np.where(column!=0)])
    for v in vertices:
        xy = X[v]
        ax2[axi,axj].text(xy[0],xy[1], '%i'%v, c='w', ha='center', va='center', bbox={'facecolor':'r', 'alpha':0.8})
#

fig2.tight_layout()
fig2.savefig('partial_1_nullspace.png', dpi=120, bbox_inches='tight')
