# Another example manually building the
# boundary operators.
# this one is inspired by a 3d point cloud,
# where a threshold of 1 produces a graph
# which should (?) have betti numbers (1,0,1) (i.e. a sphere)
#

import numpy as np
#from scipy import linalg as spla
import intmatop
import utils

# partial_3
p3 = [
[-1,1,-1,1,0,0,0],
[0,0,0,-1,1,-1,1]
]
p3 = np.array(p3, dtype=int).T

# partial_2
p2 = [
[1,-1,0,1,0,0,0,0,0],
[1,0,-1,0,1,0,0,0,0],
[0,1,-1,0,0,0,1,0,0],
[0,0,0,1,-1,0,1,0,0],
[0,0,0,1,0,-1,0,1,0],
[0,0,0,0,1,-1,0,0,1],
[0,0,0,0,0,0,1,-1,1]
]
p2 = np.array(p2, dtype=int).T

# partial_1
p1 = [
[1,-1,0,0,0],
[1,0,-1,0,0],
[1,0,0,-1,0],
[0,1,-1,0,0],
[0,1,0,-1,0],
[0,1,0,0,-1],
[0,0,1,-1,0],
[0,0,1,0,-1],
[0,0,0,1,-1]
]
p1 = np.array(p1, dtype=int).T

ker_p1 = intmatop.null(p1)
ker_p2 = intmatop.null(p2)

print('dim(ker(p1)): %i'%ker_p1.shape[1])
print('dim(ker(p2)): %i'%ker_p2.shape[1])
