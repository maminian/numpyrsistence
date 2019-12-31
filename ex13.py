import utils
import examples
import distmat2
import numpy as np
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from sklearn import metrics

# works for n=5 to n=8; then points forced too far away
# for the top/bottom points to be unit distance to everything.

ns = [5,6,7,8]

fig = pyplot.figure(figsize=(8,8))
axs = [fig.add_subplot(2,2,i+1, projection='3d') for i in range(len(ns))]
# D = metrics.pairwise_distances(X)

for n,ax in zip(ns,axs):
    X = examples.thing2(n=n)
    utils.vis_cloud(X, axh=ax, thresh=1.00001, draw_balls=False,draw_loops=False)
#
fig.tight_layout()

pyplot.ion()
