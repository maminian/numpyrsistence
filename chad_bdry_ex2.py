# Really, my example.
# the toy example has been extended
# to include another 2-simplex, and
# a dead-end leaf.
#
# the operators happen to look like...
#

import numpy as np
from scipy import linalg as spla

def proj(vec):
    n = len(vec)
    vec = np.array(vec)
    vec.shape = (n,1)

    return np.dot(vec,vec.T)/np.dot(vec.T,vec)
#
def orth_proj(vec):
    import numpy as np
    thing = np.shape(vec)
    n = thing[0]
    if len(thing)==1:
        return np.eye(n) - proj(vec)
    else:
        return np.eye(n) - sum([proj(vi) for vi in vec.T])
#

# partial_2
p2 = [
[1,0,0,0,1,-1,0,0,0],
[0,1,0,0,0,0,-1,1,0]
]
p2 = np.array(p2, dtype=int).T

# partial_1
p1 = [
[1,0,0,0,-1,0,0,0,0],
[-1,1,0,0,0,-1,1,0,0],
[0,-1,1,0,0,0,0,1,1],
[0,0,-1,1,0,0,0,0,0],
[0,0,0,-1,1,1,0,0,0],
[0,0,0,0,0,0,-1,-1,0],
[0,0,0,0,0,0,0,0,-1]
]
p1 = np.array(p1, dtype=int)

ker_p1 = spla.null_space(p1)
Q,R = np.linalg.qr(p2)

im_p2 = Q
