class State:
	def __init__(self, game):
		self.game = game

		self.current_hex = None
		self.selected_player = None

	def start(self):
		self.game.add_object(self)

	def update(self): ...

	def draw(self, surface):
		pass

	def end(self, next_state):
		self.game.remove_object(self)
		next_state.start()
