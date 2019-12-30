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
X = examples.noisy_lemniscate(permute=True)
D = distmat2.Distmat2(X)
idx = D.get_subgraph(thresh=0.8)
pairs = D.coords[idx]

p1,p2 = utils.get_boundary_operators(pairs)

nullspace = intmatop.null(p1)

if False:
    # naive algorithm to remove some, but not all,
    # nullspace elements clearly in the image of p2.
    nz_pattern_null = [tuple( np.where(col!=0)[0] ) for col in nullspace.T]
    nz_pattern_p2 = [tuple( np.where(col!=0)[0] ) for col in p2.T]

    to_remove = []
    for i,ci in enumerate(nz_pattern_null):
        for j,cj in enumerate(nz_pattern_p2):
            if ci==cj:
                to_remove.append(i)
                break
    #
    to_keep = np.setdiff1d(np.arange(nullspace.shape[1]), to_remove)
else:
    to_keep = np.arange(nullspace.shape[1])
#

fig2,ax2 = pyplot.subplots(1,1, figsize=(10,6))
utils.vis_cloud(X, thresh=0.8, draw_edges=False, draw_loops=False, axh=ax2)

for i,column in enumerate( nullspace[:,to_keep].T ):
    line_set = []
    text_set = []
    to_annotate = []
    for j,c in enumerate(column):   # Jimmy Carter
        if c!=0:
            to_annotate += list(pairs[j])
            xxyy = X[pairs[j]]
            l = ax2.plot(xxyy[:,0], xxyy[:,1], c='w', lw=2)
            line_set.append( l[0] )
    #
    to_annotate = np.unique(to_annotate)
    for ta in to_annotate:
        x,y = X[ta]
        a = ax2.text(x,y, ta, c='w', fontsize=11, ha='right', va='top', bbox={'facecolor':'r', 'alpha':0.7})
        text_set.append( a )
    #

    # fig2.savefig('frames/frame_%s.png'%str(i).zfill(4), dpi=120, bbox_inches='tight')

    #
    pyplot.pause(0.1)
    for l in line_set[::-1]:
        l.remove()
    for a in text_set[::-1]:
        a.remove()
#
