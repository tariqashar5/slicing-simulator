import sys
sys.path.append(".")
from gnb import base_station
from client import client
import Kmeans as km
import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KDTree

bs = [base_station(random.randrange(1,1000), random.randrange(1,1000), random.randrange(80,279)) for i in range(1,6)]

bs_coor = [(800,200), (200, 800), (500,500), (0,0), (800,800), (250,700)]

for i, b in zip(bs_coor, bs):
	b.x = i[0]
	b.y = i[1]


clients = [client(random.randrange(1,1000), random.randrange(1,1000)) for i in range(1,50)]

bx = [b.x for b in bs]
by = [b.y for b in bs]
br = [b.coverage for b in bs]

fig, ax = plt.subplots()

for x, y, r in zip(bx, by, br):
	circle = plt.Circle((x, y), r, color = [random.random(), random.random(), random.random()], alpha=0.25)
	ax.add_patch(circle)

cx = [c.x for c in clients]
cy = [c.y for c in clients]

query = km.kdtree(clients, bs)

for client, q in zip(clients, query[1]):
	#print("closest base station to client with coordinates x:", client.x, " y:", client.y, " is the base station with coordinates", bs[q[0]].x, bs[q[0]].y)
	plt.plot((client.x, bs[q[0]].x), (client.y, bs[q[0]].y), alpha=0.5)

plt.xlim(0, 1000)
plt.ylim(0, 1000)
plt.scatter(cx, cy)
plt.show()