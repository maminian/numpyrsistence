import utils
import intmatop
import numpy as np

# test generic implementation.
np.random.seed(0)

m = 6
n = 13
reps = 3

for i in range(reps):
    A = np.random.choice(np.arange(-4,8), m*n).reshape((m,n))
    nope = intmatop.null(A)
    print('\nIteration %i...\n==================================\n'%i)
    print(A)
    print(np.dot(A,nope))
#
