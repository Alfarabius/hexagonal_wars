import utils
from choice_state import Choice


class GameScript:
	def __init__(self, game):
		self.game = game

	def update(self):
		if self.game.turn == 0:
			self.game.turn = 1
			main_menu = Choice(
				self.game,
				None,
				'Main Menu',
				{
					'New Game': [self.game.change_state, [self.game.state]],
					'Load Game': [utils.plug, None],
					'Settings': [utils.plug, None],
					'Exit': [self.game.quit, None]
				}
			)
			self.game.state.change_state(main_menu)

	def draw(self, surface):
		pass
