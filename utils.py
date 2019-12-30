
def vis_cloud(X, thresh=0., draw_edges=True, draw_loops=True, axh=None):
    import point_cloud
    import distmat2
    from matplotlib import patches
    import numpy as np
    from matplotlib import pyplot

    pc = point_cloud.Point_cloud(X)

    D2 = distmat2.Distmat2(X)
    edge_idx = D2.get_subgraph(thresh)
    pairs = D2.coords[edge_idx]

    node_list = {j:list( pairs[pairs[:,0]==j,1] ) for j in np.unique(pairs[:,0])}

    if axh:
        ax = axh
        pc.visualize(axh=ax)
    else:
        pc.visualize()
        ax = pc.ax
    #

    pc.draw_ball(np.unique(pairs), thresh/2., c=[0.5,0,0.5])

    ######################
    # edges
    if draw_edges:
        for j,o in enumerate(D2.order[:len(pairs)]):
            iijj = D2.coords[o]
            xxyy = X[iijj]
            #middle = np.mean(xxyy, axis=0)
            ax.plot(xxyy[:,0], xxyy[:,1], c=pyplot.cm.tab10(j%10), lw=2)
        #

    ######################
    # K_3 subgraphs
    loops = []
    for k,v in node_list.items():
        for i in range(len(v)):
            for j in range(i+1,len(v)):
                if (v[i] in node_list.keys()) and (v[j] in node_list[v[i]]):
                    loops.append([k,v[i],v[j]])
    loop_coords = [X[l] for l in loops]

    polys = []
    if draw_loops:
        for lc in loop_coords:
            triangle = patches.Polygon(lc, facecolor=[0,0,0,0.25], edgecolor='k')
            tripatch = ax.add_patch(triangle)
            polys.append(tripatch)
        #

    # ax.axis('square')

    return ax
#


def get_K3s(pairs):
    '''
    Given an unweighted, undirected graph parameterized as
    a list of pairs of integers indexing vertices,
    return all K_3 subgraphs (2-simplices).

    Pairs MUST be indexed in ascending order! In other
    words, [0,2] is ok; [2,0] might introduce bugs.
    '''
    import numpy as np
    pairs = np.array(pairs)

    node_list = {j:list( pairs[pairs[:,0]==j,1] ) for j in np.unique(pairs[:,0])}
    loops = []
    for k,v in node_list.items():
        for i in range(len(v)):
            for j in range(i+1,len(v)):
                if (v[i] in node_list.keys()) and (v[j] in node_list[v[i]]):
                    loops.append([k,v[i],v[j]])
    return loops
#

def proj(vec):
    '''
    Construct projection operator (matrix) for a single vector vec.
    '''
    import numpy as np
    n = len(vec)
    vec = np.array(vec)
    vec.shape = (n,1)

    return np.dot(vec,vec.T)/np.dot(vec.T,vec)
#
def orth_proj(vec):
    '''
    Construct projection operator (matrix) to the space orthogonal
    to one or input vectors vec. A one-dimensional array is
    interpreted as a single vector. A two-dimensional array is
    interpreted as a basis for a subspace to be projected away from;
    the projector is constructed in pieces.
    '''
    import numpy as np
    thing = np.shape(vec)
    n = thing[0]
    if len(thing)==1:
        return np.eye(n) - proj(vec)
    else:
        return np.eye(n) - sum([proj(vi) for vi in vec.T])
#


#X = examples.noisy_circle()
def get_boundary_operators(pairs):
    '''
    Construct the boundary operators for partial_1 and partial_2
    associated with a list of edges associated with a graph.

    pairs: list of lists or similar of edges. These are expected
        to be in ascending order; so [[2,3],[0,4],[1,2]] is valid.
    '''
    import utils
    import numpy as np

    loops = get_K3s(pairs)
    # loop_coords = [X[l] for l in loops] # If I wanted I could do this

    _nv = np.max(pairs)+1
    _vertices = np.arange(_nv)

    # Don't need an ordering for the K3 loops, but register it here
    # just in case for later.
    _loops = list(loops)

    # Definitely DO need to specify an ordering for the edges.
    # It's probably going to be a good idea to build it in ascending
    # order of distance (which we already have in D2).
    _ne = len(pairs)
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
    partial_1 = np.zeros( (_nv, _ne), dtype=int )
    for j,_e in enumerate(_edges):
        partial_1[_e[0],j] = 1
        partial_1[_e[1],j] = -1
    #
    return partial_1, partial_2
#
