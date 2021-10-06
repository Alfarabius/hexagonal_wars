import pygame.sprite

import utils
from on_map_object import Unit


class Player:
	def __init__(self, path, game_map):
		self.army = pygame.sprite.Group()
		self.reserve = pygame.sprite.Group()
		self._parse_army(path, game_map)
		self.map_surface = game_map.surface

	def draw(self, surface):
		self.army.draw(self.map_surface)

	def update(self):
		self.army.update()

	def _parse_army(self, path, game_map):
		player_config = utils.json_to_dict(path)
		units_dict = player_config.get('parameters', '')
		army = player_config.get('list', '')
		for unit in army:
			parameters = units_dict.get(unit[0])
			Unit(
				game_map.get_hexagon_by_number(unit[1]),
				parameters[0],
				self.army,
				parameters[1],
				parameters[2],
				int(path[-6])
			)

	def restore(self):
		for unit in self.army:
			unit.restore()
