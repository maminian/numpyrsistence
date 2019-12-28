import point_cloud
import numpy as np
from matplotlib import pyplot

n = 20
eps = 0.1
np.random.seed(2)

th = np.linspace(0,2*np.pi,n)
X = np.array([np.cos(th),np.sin(th)]).T + eps*np.random.randn(n,2)

# quick and dirty distance matrix.
D = np.array([[np.linalg.norm(x-y) for x in X] for y in X])

dmin = D[D!=0].min()

if __name__=="__main__":
    pc = point_cloud.Point_cloud(X)
    pc.visualize(s=20)

    multiples = list(range(1,5))
    base_color = np.array([0.6,0,0.6])
    for k,j in enumerate( multiples ):
        for i in range(n):
            shade_of_gray = (k/(1+len(multiples)))*base_color
            pc.draw_ball(i,j*dmin/2,c=shade_of_gray)


    pyplot.ion()
