import random
import math

class client:
	connect_array = []
	dic={}
	connect_count = 0
	tree = []
	bs = []
	def __init__(self, x, y, env, movement = 20, slice_used = None):
		self.x = x
		self.y = y
		self.gnb = None
		if slice_used:
			self.slice_used = slice_used
			slice_used.add_user()
		self.connected = False
		self.env = env
		self.process = env.process(self.sim())
		self.movement = movement

	

	def sim(self):
		if not self.connected:
			query = self.tree.query([(self.x, self.y)], k = 8)

			for b in query[1][0]:
				if self.distance(self.bs[b]) < self.bs[b].coverage and self.bs[b].is_free(self.slice_used.id):
					self.connect(self.bs[b])
					print("client at", self.x, self.y,"is now trying to be connected to", self.connected, self.gnb.id)

			if not self.connected:
				print("client could not find a match")
				
					
							
		
		yield self.env.timeout(0.25)


		self.x += random.randrange(5)
		self.y += random.randrange(5)
		
		yield self.env.timeout(0.25)

		if self.gnb and self.distance(self.gnb) > self.gnb.coverage:
			if self.connected:
				self.disconnect()

		yield self.env.timeout(0.25)

		yield self.env.process(self.sim())



	def distance(self, b):
		p = (self.x, self.y)
		q = (b.x, b.y)
		return math.dist(p, q)



	def connect(self, gnb):
		self.connected =  True
		self.gnb_id = gnb.id
		self.gnb = gnb
		client.connect_count += 1
		#self.connect_array.append((client.connect_count, float(self.env.now)))
		#self.slice_used.timecount.append((self.slice_used.users, self.env.now))
		if float(self.env.now) not in self.slice_used.timedict.keys():
			self.slice_used.timedict[float(self.env.now)]=self.slice_used.users
		elif self.slice_used.users>self.slice_used.timedict[float(self.env.now)]:
			self.slice_used.timedict[float(self.env.now)]=self.slice_used.users
		if float(self.env.now) not in client.dic.keys():
			client.dic[float(self.env.now)]=client.connect_count
		elif client.connect_count>client.dic[float(self.env.now)]:
			client.dic[float(self.env.now)]=client.connect_count
		gnb.add_client(self)

	def disconnect(self):
		if self.connected == False:
			print("client is already disconnected")
			return
		client.connect_count -= 1
		self.connect_array.append((client.connect_count, float(self.env.now)))
		self.slice_used.timecount.append((self.slice_used.users, self.env.now))
		self.connected = False
		self.gnb_id = -1
		self.gnb.remove_client(self)
		self.gnb = None
		print("successfull disconnect")
