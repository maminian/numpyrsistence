class Distmat2:
    def __init__(self,Dmat):
        import numpy as np

        n,d = np.shape(Dmat)
        self.n = n
        self.d = d

        self._nc = (self.n*(self.n-1))//2
        self.coords = np.zeros( (self._nc, 2), dtype=int )
        self.distances = np.zeros( self._nc, dtype=float )

        if self.n != self.d:
            # assume a point cloud was passed;
            # compute the euclidean distance matrix.
            from sklearn import metrics
            Dmat2 = metrics.pairwise_distances(Dmat, metric='euclidean')
        else:
            Dmat2 = Dmat
        #

        idx = 0
        for i in range(self.n):
            for j in range(i+1,self.n):
                self.coords[idx] = (i,j)
                self.distances[idx] = Dmat2[i,j]
                idx += 1

        self.order = np.argsort(self.distances)

        return
    #

    def get_subgraph(self, thresh):
        import numpy as np
        pairs_idx = np.where(self.distances <= thresh)[0]
        #pairs = D2.coords[pairs_idx]
        return pairs_idx
    #
#
