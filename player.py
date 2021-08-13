class Player:
	def __init__(self, army):
		self.army = self.parse_army(army)
		self.cards = self.get_random_hand_of_cards()

	def parse_army(self, army):
		return None

	def get_random_hand_of_cards(self):
		return None
