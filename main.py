import sys
sys.path.append(".")
from gnb import base_station
from client import client
from slices import slicec
import Kmeans as km
import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KDTree
import simpy

env = simpy.Environment()

embb = slicec(1000, 80, 10)
urllc = slicec(20, 40, 0.01)
mmtc = slicec(10, 150, 15)


bs = [base_station(random.randrange(1,1000), random.randrange(1,1000), env,random.choice([10000000000000,1000000000,100000000000]), random.randrange(200,279), slice_ratio = [0.3, 0.3, 0.4]) for i in range(1,10)]
client.tree = km.init_tree(bs)
client.bs = bs
clients = [client(random.randrange(1,1000), random.randrange(1,1000), env, slice_used = random.choice([embb, urllc, mmtc])) for i in range(1,200)]


env.run(until = 50)

def get_marker(client):
	if client.slice_used.id == 1:
		return '+'

	if client.slice_used.id == 2:
		return 'd'

	if client.slice_used.id == 3:
		return 'x'




bx = [b.x for b in bs]
by = [b.y for b in bs]
br = [b.coverage for b in bs]

fig, ax = plt.subplots()

for x, y, r, b in zip(bx, by, br, bs):
	circle = plt.Circle((x, y), r, color = b.color, alpha=0.25)
	ax.add_patch(circle)

for client in clients:
	if client.gnb:
		plt.scatter(client.x, client.y, marker = get_marker(client), color = client.gnb.color) #add some colour for each slice specifically
	else:
		plt.scatter(client.x, client.y, marker = get_marker(client), color = 'black')


plt.xlim(0, 1000)
plt.ylim(0, 1000)
plt.show()
print(client.connect_array)
print(embb.timecount)
print(urllc.timecount)
print(mmtc.timecount)
"""
slices = [] #list of slice dictionaries per base station
for b in bs:
	slice_dict = dict()
	slice_dict = b.slices
	slices.append(slice_dict)

print(slices)
"""

"""
cx = [c.x for c in clients]
cy = [c.y for c in clients]

for client, q in zip(clients, query[1]):
	#print("closest base station to client with coordinates x:", client.x, " y:", client.y, " is the base station with coordinates", bs[q[0]].x, bs[q[0]].y)
	plt.plot((client.x, bs[q[0]].x), (client.y, bs[q[0]].y), alpha=0.5)

plt.xlim(0, 1000)
plt.ylim(0, 1000)
plt.scatter(cx, cy)
plt.show()
"""
