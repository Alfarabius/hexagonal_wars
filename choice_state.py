from game import Game
from state import State


class Choice(State):

	def __init__(self, game: Game):
		super().__init__(game)

	def update(self):
		pass

	def draw(self, surface):
		pass
