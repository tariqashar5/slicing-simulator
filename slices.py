slice_id = 0
class slicec:

	def __init__(self, bw_guarantee, max_users, latency):
		global slice_id
		slice_id += 1
		self.id = slice_id
		self.bw_guarantee = bw_guarantee
		self.max_users = max_users
		self.users = 0
		self.latency = latency
		self.timecount = []
		self.timedict={}

	def add_user(self):
		self.users += 1

	def remove_user(self):
		self.users -= 1

	def check_slice_usage(self):
		guaranteed_bw = self.users * self.bw_guarantee
		return guaranteed_bw

