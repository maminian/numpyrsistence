#
def noisy_circle(n=50, eps=0.3, seed=123234, permute=False):
    import numpy as np
    np.random.seed(seed)

    th = np.linspace(0,2*np.pi,n)
    X = np.array([np.cos(th),np.sin(th)]).T
    X += eps*np.random.randn(n,2)

    if permute:
        X = _permute(X)
    return X
#

def noisy_sphere(n=50, eps=0.05, seed=2468024, permute=False):
    # uniform sampling on sphere having a uniform expected
    # euclidean distance from a point to its nearest neighbors
    #
    # Seems this can be done scaling normal random vars by magnitude;
    # see http://corysimon.github.io/articles/uniformdistn-on-sphere/
    # The eps here represents noise in the magnitude.
    import numpy as np
    np.random.seed(seed)

    X = np.random.randn(n,3)
    rho = np.linalg.norm(X, axis=1)

    X = (X.T/rho*(1 + eps*np.random.randn(len(rho)))).T

    if permute:
        X = _permute(X)
    return X
#

def noisy_torus(nu=20,nv=20, eps=0.05, seed=14285714, permute=False):
    '''
    naive generation of torus followed by subsampling to desired value of n.
    '''
    import numpy as np
    t1 = np.linspace(0,2*np.pi, nu+1)[::-1]
    t2 = np.linspace(0,2*np.pi, nv+1)[::-1]
    x = np.concatenate([ (2+np.cos(t))*np.cos(t1) for t in t2 ])
    y = np.concatenate([ (2+np.cos(t))*np.sin(t1) for t in t2 ])
    z = np.concatenate([ np.sin(t)*np.ones(t1.shape) for t in t2 ])
    X = np.vstack([x,y,z]).T

    # subsampling in an unbiased way requires a permutation.
    if permute:
        X = _permute(X)

    X *= (1 + eps*np.random.randn(*X.shape))

    return X
#

#

def house(permute=False):
    import numpy as np
    X = np.array([
    [-np.cos(np.pi/6), np.sin(np.pi/6)],
    [0,1],
    [1,1],
    [1,0],
    [0,0]
    ])

    if permute:
        X = _permute(X)
    return X
#

def house2(permute=False):
    # my own extension of the "house" example.
    import numpy as np
    X = np.array([
    [-np.cos(np.pi/6), np.sin(np.pi/6)],
    [0,1],
    [1,1],
    [1,0],
    [0,0],
    [np.cos(np.pi/3), 1+np.sin(np.pi/3)],
    [2,1]
    ])

    if permute:
        X = _permute(X)
    return X
#

def thing1(permute=False):
    import numpy as np
    X = np.array([
        [0,0,-np.sqrt(2./3)],
        [-0.5, -1./np.sqrt(12), 0],
        [0.5, -1./np.sqrt(12), 0],
        [0, 1./np.sqrt(3), 0],
        [0,0,+np.sqrt(2./3)]
    ])

    if permute:
        X = _permute(X)
    return X
#

def thing2(n=6, permute=False):
    import numpy as np
    X = [np.array([np.cos(th), np.sin(th),0]) for th in np.linspace(0,2*np.pi,n-1)[:-1]]
    plane_center = np.mean(X, axis=0)
    X = [xi - plane_center for xi in X]
    scaling = np.linalg.norm(X[1] - X[0])
    X /= scaling

    moo = np.sqrt(np.abs(1. - np.linalg.norm(X[0])**2))
    X = [[0,0,-moo]] + list(X) + [[0,0,+moo]]
    X = np.array(X)

    if permute:
        X = _permute(X)
    return X

def noisy_lemniscate(n=50, eps=0.2, seed=271828, permute=False):
    import numpy as np
    np.random.seed(seed)

    th = np.linspace(0,2*np.pi,n)
    X = np.array([2*np.cos(th),np.sin(2*th)]).T
    X += eps*np.random.randn(n,2)

    if permute:
        X = _permute(X)
    return X
#

def _permute(pts):
    import numpy as np
    return np.random.permutation(pts)
#

if __name__=="__main__":
    import utils
    from matplotlib import pyplot

    figs,axs = [],[]
    for ex,thresh in zip([noisy_circle, house, house2], [0.5,1,1]):
        X = ex()
        fig,ax = utils.vis_cloud(X, thresh=thresh)
        figs.append( fig )
        axs.append( ax )
    #
    pyplot.ion()
#
