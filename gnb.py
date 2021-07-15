class base_station:
	
	def __init__(self, x, y, coverage = 80, slice_ratio = None, max_bw):
		self.x = x
		self.y = y
		self.coverage = coverage
		self.max_bw = max_bw
		self.slice_ratio = slice_ratio

	