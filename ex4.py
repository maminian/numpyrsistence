import ex3
import point_cloud
import numpy as np
from matplotlib import pyplot

from matplotlib import patches

#
# an attempt at constructing the
# boundary operators of the graph
# from the given threshold in ex3.py.
#
# SCRATCH THAT
# First, just try to manually visualize
# all 2-simplices
# (complete graphs on 3 vertices).
#

node_list = {j:list( ex3.pairs[ex3.pairs[:,0]==j,1] ) for j in np.unique(ex3.pairs[:,0])}
loops = []
for k,v in node_list.items():
    for i in range(len(v)):
        for j in range(i+1,len(v)):
            if (v[i] in node_list.keys()) and (v[j] in node_list[v[i]]):
                loops.append([k,v[i],v[j]])
#

if __name__=="__main__":
    ex3.pc.visualize()
    ex3.pc.draw_ball(ex3.which, ex3.thresh/2., c=[0.5,0,0.5])



    for j,o in enumerate(ex3.D2.order[:len(ex3.pairs)]):
        iijj = ex3.D2.coords[o]
        xxyy = ex3.X[iijj]
        middle = np.mean(xxyy, axis=0)
        ex3.pc.ax.plot(xxyy[:,0], xxyy[:,1], c=pyplot.cm.tab10(j%10), lw=2)
    #

    loop_coords = [ex3.X[l] for l in loops]

    polys = []
    for lc in loop_coords:
        triangle = patches.Polygon(lc, facecolor=[0,0,0,0.5], edgecolor='k')
        tripatch = ex3.pc.ax.add_patch(triangle)
        polys.append(tripatch)
    #

    if False:
        for j,o in enumerate(ex3.D2.order[:len(ex3.pairs)]):
            iijj = ex3.D2.coords[o]
            xxyy = ex3.X[iijj]
            middle = np.mean(xxyy, axis=0)
            ex3.pc.ax.text(middle[0],middle[1], '%.2f'%ex3.D2.distances[o], c='w', fontsize=11, ha='center', va='center')
        for j,co in enumerate(ex3.pc.pts):
             ex3.pc.ax.text(co[0], co[1], j, c='w', fontsize=10, ha='center', va='center', bbox={'facecolor':'r', 'alpha':0.5})
        ex3.pc.ax.set_title('Threshold %.2f'%ex3.thresh, c='k', fontsize=18)
        ex3.pc.fig.tight_layout()
        ex3.pc.fig.subplots_adjust(top=0.9)
    #

    ex3.pc.ax.axis('square')
    pyplot.ion()
