import global_vars
import unit


class Player:
	def __init__(self, army):
		self.army = self.parse_army(army)
		self.cards = self.get_hand_of_cards()

	def parse_army(self, army):
		units = list()
		file = open(army, 'r')
		for line in file:
			if '#' not in line:
				units.append(self._parse_unit(line))
		return units

	def get_hand_of_cards(self):
		self.cards = True   # plug
		return self.cards

	@staticmethod
	def _parse_unit(line):
		line = line.split(' ')
		image = global_vars.UNIT_TYPES_DICT.get(line[0])
		power = movement_points = 0
		name = None
		if line[0][1] != 'L':
			power = int(line[1])
			movement_points = int(line[2])
		else:
			name = ''.join(symbol for symbol in line[1] if symbol.isalpha())
		hexagon = global_vars.game_map.get_random_hex()
		return unit.Unit(power, movement_points, image, name, hexagon)
