import numpy as np
from scipy.spatial.distance import squareform,pdist
import networkx as nx
import seaborn as sns
import shapely.geometry as sg
import matplotlib.pyplot as plt
import descartes
from subprocess import Popen, PIPE
import edmonds
import sys

N = int(sys.argv[1])
if len(sys.argv)==3:
	seed = int(sys.argv[2])
	np.random.seed(seed)
points = np.random.uniform(low=-N,high=N,size=(N+1,2))

points[-1] = [0,0]

plt.scatter(points[:-1,0],points[:-1,1],color='green')
plt.scatter(points[-1:,0],points[-1:,1],color='red')

z = points[:-1,0]
y = points[:-1,1]
for i, txt in enumerate(range(N)):
    plt.annotate(txt, (z[i],y[i]))

Distances = squareform(pdist(points))

# print Distances

point_distances = Distances[:-1,:-1]

# print point_distances

destination_distances = Distances[-1]

for i in range(N):
	for j in range(N):
		point_distances[i,j] += min(destination_distances[i],destination_distances[j])

print point_distances

nodes = 2*N
edges = N*N
L=[]
for i in range(N):
	L.append((i,i+N,point_distances[i,i]))

for i in range(N):
	for j in range(i):

		if point_distances[i,j] < destination_distances[i] + destination_distances[j]:
			L.append((i,j,point_distances[i,j]/2.0))
			L.append((i+N,j+N,point_distances[i,j]/2.0))

X = edmonds.run_edmonds(nodes,edges,L)
Y=[]
for x in X:
	a=x[0]
	b=x[1]
	if a>=N:
		a-=N
	if b>=N:
		b-=N
	Y.append((a,b))

Y=set(Y)
print Y

for y in Y:
	a=None
	b=None
	if destination_distances[y[0]]<destination_distances[y[1]]:
		a=y[0]
		b=y[1]
	else:
		a=y[1]
		b=y[0]
	plt.plot([points[a,0],points[b,0]],[points[a,1],points[b,1]],color='green')
	plt.plot([points[a,0],points[-1,0]],[points[a,1],points[-1,1]],color='green')


# (p,q) = points[-1]
# for (r,s) in Y:
# 	print i
# 	if destination_distances[r]>destination_distances[s]:
# 		(x,y) = points[r]
# 		a = sg.Point(x,y).buffer(Distances[-1,r])
# 		b = sg.Point(p,q).buffer(Distances[-1,r])
# 	else:
# 		(x,y) = points[s]
# 		a = sg.Point(x,y).buffer(Distances[-1,s])
# 		b = sg.Point(p,q).buffer(Distances[-1,s])
	

	# # compute the 3 parts
	# left = a.difference(b)
	# right = b.difference(a)
	# middle = a.intersection(b)

	# # use descartes to create the matplotlib patches
	# ax = plt.gca()
	# ax.add_patch(descartes.PolygonPatch(middle, fc='g', ec='k', alpha=0.1))

plt.show()
