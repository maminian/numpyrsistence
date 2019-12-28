# chad's example
# the operators happen to look like...
#

import numpy as np
from scipy import linalg as spla

# partial_2
p2 = np.array([[1,0,0,0,-1,1]], dtype=int)

# partial_1
p1 = [
[1,0,0,0,-1,0],
[-1,1,0,0,0,-1],
[0,-1,1,0,0,0],
[0,0,-1,1,0,0],
[0,0,0,-1,1,1]
]
p1 = np.array(p1, dtype=int)

ker_p1 = spla.null_space(p1)
Q,R = np.linalg.qr(p2)

im_p2 = Q
