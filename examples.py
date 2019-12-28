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
