import sys
sys.path.append(".")
from gnb import base_station
from client import client
from slices import slicec
import Kmeans as km
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree
import simpy

env = simpy.Environment()

embb = slicec(1000, 80, 10)
urllc = slicec(200, 40, 0.01)
mmtc = slicec(100, 150, 15)
connect_count=0
no_connect_count=0
connect_ratio=[]
total_count=[]
connect_ratio.append(0)
total_count.append(0)

bs = [base_station(random.randrange(1,1000), random.randrange(1,1000), env,random.choice([10000000000000,1000000000,100000000000]), random.randrange(200,279), slice_ratio = [0.3, 0.3, 0.4]) for i in range(1,13)]
bs[0].x, bs[0].y = (100,150)
bs[1].x, bs[1].y = (650,800)
bs[2].x, bs[2].y = (123,872)
bs[3].x, bs[3].y = (288,600)
bs[4].x, bs[4].y = (832,732)
bs[5].x, bs[5].y = (318,800)
bs[6].x, bs[6].y = (712,532)
bs[7].x, bs[7].y = (800,200)
bs[8].x, bs[8].y = (432,200)

client.tree = km.init_tree(bs)
client.bs = bs
clients = [client(random.randrange(1,1000), random.randrange(1,1000), env, slice_used = random.choice([embb, urllc, mmtc])) for i in range(1,350)]


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
plt.title("Geography of clients and base stations")
plt.xlabel("Distance (in meters)")
plt.ylabel("Distance (in meters)")
plt.show()

for client in clients:
	if client.gnb:
		connect_count+=1
	else:
		no_connect_count+=1
	connect_ratio.append(connect_count/(connect_count+no_connect_count))
	total_count.append(connect_count+no_connect_count)
	plt.title("Client Connection Ratio")
	plt.xlabel("Number of clients")
	plt.ylabel("Connection ratio")
	plt.plot(total_count, connect_ratio, '-')
plt.show()


time=list(client.dic.keys())
max_client=list(client.dic.values())
plt.title("Client count per second")
plt.xlabel("Time in seconds")
plt.ylabel("Connected Client count")
plt.plot(time,max_client,'-')
plt.show()



id_1=0
id_2=0
id_3=0
slice_id=[1,2,3]
clients_per_slice=[]
for client in clients:
	if client.gnb and client.slice_used.id==1:
		id_1+=1
	elif client.gnb and client.slice_used.id==2:
		id_2+=1
	elif client.gnb and client.slice_used.id==3:
		id_3+=1
clients_per_slice.append(id_1)
clients_per_slice.append(id_2)
clients_per_slice.append(id_3)
plt.bar(slice_id, clients_per_slice)
plt.title("Clients connected per slice")
plt.xlabel("Slice ID")
plt.ylabel("Number of clients")
plt.show()
#latency = pd.DataFrame(range(len(client.dic)))
embb_ltn = list(embb.timedict.values())
urllc_ltn = list(urllc.timedict.values())
mmtc_ltn = list(mmtc.timedict.values())
max_ltn = min(len(embb_ltn),min(len(urllc_ltn),len(mmtc_ltn)))
max1 = max(max(max(embb_ltn),max(urllc_ltn)),max(mmtc_ltn))
for i in range(len(embb_ltn)):
	embb_ltn[i] =embb.latency*embb_ltn[i]/1000
print(embb_ltn)

for i in range(len(urllc_ltn)):
	urllc_ltn[i] =urllc.latency*urllc_ltn[i]/1000
print(urllc_ltn)
for i in range(len(mmtc_ltn)) :
	mmtc_ltn[i] =mmtc.latency*mmtc_ltn[i]/1000
print(mmtc_ltn)
embb_ltn = embb_ltn[:max_ltn]
urllc_ltn = urllc_ltn[:max_ltn]
mmtc_ltn = mmtc_ltn[:max_ltn]
df=pd.DataFrame({'Latency': range(0,max_ltn), 
                 'Embb': embb_ltn, 
                 'urllc': urllc_ltn, 
                 'mmtc': mmtc_ltn})
#df = df.transpose()
# multiple line plot
"""
Latency issues 
Congestion in traffic in Radio Link , Access Network.
Wire Break and other hardware issues in Core Network
Hardware latency in Content Servers
"""
plt.plot( 'Latency', 'Embb', data=df, marker='', color='blue', linewidth=2, linestyle="-")
plt.plot( 'Latency', 'urllc', data=df, marker='', color='red', linewidth=2,linestyle="-")
plt.plot( 'Latency', 'mmtc', data=df, marker='', color='green', linewidth=2)
plt.title("Latency comparison between slices")
plt.xlabel("Time in seconds")
plt.ylabel("Latency") 
plt.legend()
plt.show()
time_bw = max_ltn;
embb_bw = list(embb.timedict.values())
mmtc_bw = list(mmtc.timedict.values())
urllc_bw = list(urllc.timedict.values())
embb_bw = embb_bw[:max_ltn]
urllc_bw = urllc_bw[:max_ltn]
mmtc_bw = mmtc_bw[:max_ltn]
for i in range(0,max_ltn):
	embb_bw[i] *= embb.bw_guarantee
	mmtc_bw[i] *= mmtc.bw_guarantee
	urllc_bw[i] *= urllc.bw_guarantee
print(embb_bw,mmtc_bw,urllc_bw)
df=pd.DataFrame({'Time': range(0,max_ltn), 
                 'Embb': embb_bw, 
                 'urllc': urllc_bw, 
                 'mmtc': mmtc_bw})
#df = df.transpose()
# multiple line plot
plt.plot( 'Time', 'Embb', data=df, marker='', color='blue', linewidth=2, linestyle="-")
plt.plot( 'Time', 'urllc', data=df, marker='', color='red', linewidth=2,linestyle="-")
plt.plot( 'Time', 'mmtc', data=df, marker='', color='green', linewidth=2)
plt.title("Usage in different Slices")
plt.xlabel("Time in seconds")
plt.ylabel("Slice Usage") 
plt.legend()
plt.show()


	
time=list(embb.timedict.keys())
max_client=list(embb.timedict.values())
plt.title("Client count per slice wrt time (Embb)")
plt.xlabel("Time in seconds")
plt.ylabel("Connected Client count")
plt.plot(time,max_client,'-')
plt.show()

time=list(urllc.timedict.keys())
max_client=list(urllc.timedict.values())
plt.title("Client count per slice wrt time(urllc)")
plt.xlabel("Time in seconds")
plt.ylabel("Connected Client count")
plt.plot(time,max_client,'-')
plt.show()

time=list(mmtc.timedict.keys())
max_client=list(mmtc.timedict.values())
plt.title("Client count per slice wrt time(mmtc)")
plt.xlabel("Time in seconds")
plt.ylabel("Connected Client count")
plt.plot(time,max_client,'-')
plt.show()

#print(time)
#print(max_client)
print(embb.timedict)
#print(client.dic)
print(embb.timecount)
#print(urllc.timecount)
#print(mmtc.timecount)


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
