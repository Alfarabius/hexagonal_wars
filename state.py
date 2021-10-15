class State:
	def __init__(self, game):
		self.game = game

		self.current_hex = None
		self.selected_player = None

	def update(self): ...

	def draw(self, surface): ...

	def change_state(self, state):
		self.game.state = state
		self.game.add_object(state)
		self.game.remove_object(self)

	def unselect_unit(self):
		pass
