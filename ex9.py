import utils
import intmatop
import numpy as np

# test on toy example for now.

thing = np.array([
[3,0,2,-4,-1,0],
[0,2,1,-1,1,0],
[0,0,0,0,0,1],
[0,0,0,0,0,0]
], dtype=int)

# find pivot elements
pivots = []
for i in range(thing.shape[0]):
    for j in range(thing.shape[1]):
        if thing[i,j]!=0:
            pivots.append([i,j])
            break
#

dependents = np.array([p[1] for p in pivots])
independents = np.setdiff1d(np.arange(thing.shape[1]), dependents)

ker_p1 = np.zeros((thing.shape[1], len(independents)), dtype=int)
common_factor = intmatop.lcm2([thing[i,p] for i,p in pivots])
multipliers = [common_factor//thing[i,p] for i,p in pivots]

#idx=
idx=0
for (i,p),m in zip(pivots,multipliers):
    ker_p1[p] = -m*thing[i,independents]
#
for j,ind in enumerate(independents):
    ker_p1[ind,j] = common_factor
###
print('Original rref matrix:')
print(thing)
print('Integer basis for nullspace:')
print(ker_p1)
print('proof: ')
print(np.dot(thing,ker_p1))
