#
def lcm(x,y):
    import numpy as np
#    return (np.int64(x)*np.int64(y))//np.gcd(x,y, dtype=np.int64)
    return np.lcm(x,y, dtype=np.int64)
#

def lcm2(integers):
    '''
    Finds the least common multiple of a collection
    of POSITIVE integers (1 or greater). The 1s are filtered anyway.
    '''
    # mediocre algorithm: prime factorization of each entry,
    # then build up the product from a maximal set of the prime factors.
    import numpy as np

    if True:
        return np.lcm.reduce(integers)
    else:
        if len(integers)==1:
            return integers[0]
        factors = []
        for i in integers:
            if i>1:
                factors.append(i)
        if len(factors)==0:
            # There must have only been 1s in the list.
            return 1

        # TODO: implement caching and/or lookup table in final version.
        factorizations = [prime_factors(f) for f in factors]
        ref_list = []
        for fact in factorizations:
            for f in fact:
                if f not in ref_list:
                    ref_list.append(f)
        #
        counts = [0 for _ in ref_list]
        for fact in factorizations:
            for j,r in enumerate(ref_list):
                exponent = fact.count(r)
                counts[j] = max(counts[j], exponent)
        #
        lcm_result = np.prod([r**c for r,c in zip(ref_list, counts)])
        return lcm_result
    #
#

def gcd2(integers):
    '''
    Find the greatest common multiple of a list of numbers.

    Ex:
    gcd2([1,2,3]) = 1
    gcd2([8,16,28]) = 4
    gcd2([0,2,3]) = 1
    '''
    import numpy as np
    if len(integers)==1:
        return integers[0]
    result = np.gcd(integers[0], integers[1], dtype=np.int64)
    for i in integers[2:]:
        result = np.gcd(result, i, dtype=np.int64)
    return result
#

def prime_factors(n):
    '''
    Get prime factors (incl. multiplicity) of an integer n
    Shamelessly taken/tweaked from
    https://www.geeksforgeeks.org/print-all-prime-factors-of-a-given-number/
    '''
    import math

    prime_list = []
    # Print the number of two's that divide n
    while n % 2 == 0:
#        print 2,
        prime_list.append(2)
        n = n // 2

    # n must be odd at this point
    # so a skip of 2 ( i = i + 2) can be used
    for i in range(3,int(math.sqrt(n))+1,2):
        # while i divides n , print i and divide n
        while n % i== 0:
#            print i,
            prime_list.append( i )
            n = n // i

    # Condition if n is a prime
    # number greater than 2
    if n > 2:
        prime_list.append( n )
    return prime_list
#


def multipliers(x,y):
    # Get minimal multipliers a1,a2 such that a1*x==a2*y.
    import numpy as np
    common = lcm(x,y)
    return np.int64(common)//np.int64(x), np.int64(common)//np.int64(y)
#

def row_swap(mat,i,j):
    if i==j:
        return
    import copy
    temp = copy.copy(mat[i])
    mat[i] = mat[j]
    mat[j] = temp
    return
#

def axpby(alpha, vec1, beta, vec2):
    return alpha*vec1 + beta*vec2
#

def row_reduce(A, verbosity=0):
    '''
    Row reduction, with pivoting, over the integers.
    Operations are done in-place; that is, A is overwritten.
    Note that the pivot entries may or may not be zero.

    This is NOT reduced row echelon form.
    '''
    import numpy as np
    m,n = np.shape(A)

    for i in range(m):
        # Do a row-first search for a nonzero value
        # to identify a pivot.
        pivot=-1
        flag=False
        for jj in range(i,n):
            for kk in range(i,m):
                if A[kk,jj]!=0:
                    pivot_row = kk
                    pivot_col = jj
                    flag=True
                    break
            if flag:
                break
        if not flag:
            # could not identify a single nonzero entry.
            # Therefore, the forward sweep is done.
            break
        else:
            # we've identified a pivot element.
            # swap rows and begin work.
            row_swap(A, i, pivot_row)
            if verbosity>0:
                print('Swap R_%i and R_%i'%(i,pivot_row))
            if verbosity>1:
                print('=================\n',A)
        #

        # note that the pivot is in column jj, by design.
        # sweep downwards and eliminate nonzero entries.
        if verbosity>0:
            print('Row %i; pivot column %i'%(i,pivot_col))
        for j in range(i+1,m):
            if A[j,pivot_col]==0:
                continue
            a1,a2 = multipliers(A[i,pivot_col], A[j,pivot_col])
            A[j,pivot_col:] = axpby(-a1, A[i,pivot_col:], a2, A[j,pivot_col:])

            if verbosity>0:
                print('R_%i <- (%i)R_%i + (%i)R_%i'%(j,-a1,i,a2,j))
            if verbosity>1:
                print('=================\n',A)
        #

        # ...that should be it.
    #
#    return A
    return
#

def back_substitute(A, verbosity=0):
    '''
    Assumes matrix A is the result of row_reduce(),
    perform back-substitution as the second step to
    putting it in reduced row echelon form (rref)
    specifically over the integers.
    '''
    import numpy as np
    m,n = np.shape(A)

    # preprocessing step: identify pivots.
    pivots = []
    for i in range(m):
        for ii in range(i,n):
            if A[i,ii]!=0:
                pivots.append( [i,ii] )
                break
    #

    # back-substitute along the pivots.
    for i,p in pivots[::-1]:
        for j in range(i-1,-1,-1):
            if A[j,p]==0:
                continue
            a1,a2 = multipliers(A[i,p], A[j,p])

            # Cannot restrict focus of the axpby operation here;
            # entries to the left will be affected by the axpby operation.
            A[j] = axpby(-a1, A[i,:], a2, A[j,:])
    #

    # Attempt to scale rows if possible.
    for i,p in pivots:
        divisor = gcd2(A[i,p:])
        if divisor not in [0,1]:
            A[i,p:] //= divisor
            A[i,p:] *= np.sign(A[i,p], dtype=np.int64)
    #

    # ... is that it?
    return
#

def rref(A, verbosity=0):
    '''
    Reduced row echelon form for a matrix A.
    Calls row_reduce, then back_substitute.
    '''
    import numpy as np
    if A.dtype != np.int64:
        print('Casting to numpy.int64; else overflow can happen.')
        A = np.array(A, dtype=np.int64)
    #
    row_reduce(A, verbosity=verbosity)
    back_substitute(A, verbosity=verbosity)
    return
#

def null_from_rref(A, verbosity=0):
    '''
    Find integer basis for nullspace of a matrix A
    assumed to be in rref form.
    '''
    import numpy as np
    m,n = np.shape(A)

    # find pivot elements
    pivots = []
    for i in range(m):
        for j in range(n):
            if A[i,j]!=0:
                pivots.append([i,j])
                break
    #

    dependents = np.array([p[1] for p in pivots])
    independents = np.setdiff1d(np.arange(n), dependents)

    common_factor = lcm2([A[i,p] for i,p in pivots])
    multipliers = [common_factor//A[i,p] for i,p in pivots]

    nullspace = np.zeros((n, len(independents)), dtype=np.int64)

    for (i,p),m in zip(pivots,multipliers):
        nullspace[p] = -m*A[i,independents]
    #
    for j,ind in enumerate(independents):
        nullspace[ind,j] = common_factor
    return nullspace
#

def null(A, verbosity=0):
    '''
    Black box nullspace function from arbitrary matrix A
    (though we only have confidence it works for wide matrices).
    '''
    import numpy as np
    A2 = np.array(A, dtype=np.int64)
    rref(A2, verbosity=verbosity)
    nullspace = null_from_rref(A2, verbosity=verbosity)

    return nullspace
#

######################################################

def ex1():
    import numpy as np
    return np.array([
        [2,1,-1,1,1,0],
        [3,0,0,1,-1,0],
        [1,1,-1,0,0,0],
        [0,0,1,0,0,0],
        [0,0,1,1,0,1]
    ], dtype=np.int64)
#

def ex2():
    import numpy as np
    return np.array([
        [0,1,1],
        [0,0,1],
        [1,1,1]
    ], dtype=np.int64)

def ex3():
    import numpy as np
    return np.array([
        [0,5,1,1,0,1,0],
        [0,0,-1,-1,2,3,0],
        [0,3,1,1,1,1,1],
        [0,-1,-1,-1,-1,-1,-1]
    ], dtype=np.int64)

if __name__=="__main__":
    import numpy as np
    verbosity=1

    A = ex1()
    row_reduce(A, verbosity=2)
