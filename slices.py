class slice:

	def __init__(self, name, qos, bw_max, bw_req):
		self.slice = name
		self.qos = qos
		self.bw_max = bw_max
		self.bw_guarantee = bw_guarantee
		self.users = 0

	def add_user(self):
		self.users += 1

	def check_slice_usage(self):
		free_bw = self.bw_max / (self.bw_guarantee * self.users) 
		return free_bw

	