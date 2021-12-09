gnb_id = 0
import random
class base_station:
	def __init__(self, x, y, env, max_bw = 100000000, coverage = 80, max_users = 100, slice_ratio = []):
		global gnb_id
		gnb_id += 1
		self.id = gnb_id
		self.x = x
		self.y = y
		self.id = gnb_id
		self.coverage = coverage
		self.max_bw = max_bw
		self.env = env
		self.slice_ratio = slice_ratio
		self.waiting_room = list()
		self.client_list = list()
		self.slices = {x:0 for x in range(1,10)}
		self.ratios = list()
		self.color = [random.random(), random.random(), random.random()]
		self.slice_allocation = [max_users * i for i in self.slice_ratio]


	def add_client(self, client):
		
		print("slices for gnb with", self.id, self.slices)

		if client.slice_used.id not in self.slices:
			self.client_list.append(client)
			self.slices[client.slice_used.id] = 1
			client.slice_used.add_user()
			return
		
		elif self.is_free(client.slice_used.id):
			self.client_list.append(client)
			self.slices[client.slice_used.id] += 1
			print("number of clients in slice", client.slice_used.id, "is", self.slices[client.slice_used.id])
			client.slice_used.add_user()
			return

		else:
			print("adding client to waiting room")
			self.waiting_room.append(client)

	def remove_client(self,client):
		if client in self.client_list:
			self.client_list.remove(client)
			self.slices[client.slice_used.id] -= 1
			print("decrementing count for slice", client.slice_used.id)
			client.slice_used.remove_user()
		if client in self.waiting_room:
			self.waiting_room.remove(client)

	def is_free(self, sliceid):
		if self.slices[sliceid] < self.slice_allocation[sliceid - 1]:
			return True
		else:
			return False






	







	

"""
	add a client only when there's place in its slice
	keep checking how many clients are waiting
	try to dynamically change the slice ratio to allocate more clients in a particular slice
	example one slice has less clients, but a higher ratio, change the ratio in the basestation to allocate that client 
"""