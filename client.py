class client:
	
	def __init__(self, x, y, slice_used = None):
		self.x = x
		self.y = y
		self.slice = slice_used.name
		slice_used.add_user()
		self.connected = False

	def connect(self, gnb):
		self.connected =  True
		self.gnb = gnb

	