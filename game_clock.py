import time


class GameClock:
	def __init__(self):
		self.prev_time = time.time()
		self.dt = 0

	def update(self):
		now = time.time()
		self.dt = now - self.prev_time
		self.prev_time = now

	def draw(self, surface):
		pass
