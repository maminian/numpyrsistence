
class Point_cloud:
    def __init__(self,pts):
        import numpy as np
        self.pts = np.array(pts)
        self.n, self.d = np.shape(self.pts)

        self.circles = {i:[] for i in range(self.n)}
        return
    #
    def draw_ball(self,i,r, c=[0.5,0,0]):
        if not hasattr(self,'ax'):
            raise Exception('Must visualize first; run self.visualize()')

        from matplotlib import patches
        if hasattr(i,'__iter__'):
            for j in i:
                self.draw_ball(j,r,c=c)
            #
            return
        else:
            xy = self.pts[i][:2]
            circ = patches.Circle(xy, radius=r, edgecolor=c, linewidth=1, facecolor=list(c)+[0.4], zorder=-100)
            circobj = self.ax.add_patch(circ)
            self.circles[i].append(circobj)

        return
    #
    def draw_balls(self,r, c=[0.5,0,0]):
#        for i in range(self.n):
#            self.draw_ball(i,r, c=c)
        self.draw_ball(list(range(self.n)), r, c=c)
        return
    #

    def visualize(self,*args,**kwargs):
        if self.d == 3:
            # switch to visualize3d
            self.visualize3d(*args,**kwargs)
            return
        elif self.d == 2:
            pass
        else:
            raise Exception('Visualization only supported in 2d and 3d.')
        from matplotlib import pyplot

        if 'axh' in kwargs:
            ax = kwargs['axh']
            fig = ax.get_figure()
            kwargs.pop('axh')
        else:
            fig,ax = pyplot.subplots(1,1)
        #

        self.fig = fig
        self.ax = ax

        ax.scatter(self.pts[:,0], self.pts[:,1], *args, **kwargs)

        # fig.tight_layout()
#        ax.axis('equal')

        fig.show()
        return
    #

    def visualize3d(self,*args,**kwargs):
        from matplotlib import pyplot
        from mpl_toolkits import mplot3d

        if 'axh' in kwargs:
            ax = kwargs['axh']
            fig = ax.get_figure()
            kwargs.pop('axh')
        else:
            fig = pyplot.figure()
            ax = fig.add_subplot(111, projection='3d')
        #

        self.fig = fig
        self.ax = ax

        ax.scatter(self.pts[:,0], self.pts[:,1], self.pts[:,2], *args, **kwargs)

        # fig.tight_layout()
        # ax.axis('square')

        fig.show()
        return
    #
#
