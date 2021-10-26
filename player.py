import pygame.sprite

import utils
from on_map_object import Unit


class Player:
	def __init__(self, path, game_map, timer):

		self.army = pygame.sprite.Group()
		self.reserve = pygame.sprite.Group()

		self.timer = timer

		self._parse_army(path, game_map)

		self.map_surface = game_map.surface

	def draw(self, surface):
		self.army.draw(self.map_surface)

	def update(self):
		self.army.update()

	def _parse_army(self, path, game_map):
		player_config = utils.json_to_dict(path)
		self.owner = player_config.get('owner', 'bot')
		units_dict = player_config.get('parameters', '')
		army = player_config.get('list', '')
		for unit in army:
			parameters = units_dict.get(unit[0])
			Unit(
				self.timer,
				game_map.get_hexagon_by_number(unit[1]),
				parameters[0],
				self.army,
				parameters[1],
				parameters[2],
				int(path[-6]),
				parameters[3]
			)

	def restore(self):
		for unit in self.army:
			unit.restore()

	def get_next_unit(self, unit):
		if unit is None and self.army:
			return self.army.sprites()[0]
		index = self.army.sprites().index(unit) + 1
		if index >= len(self.army):
			index = 0
		return self.army.sprites()[index]
