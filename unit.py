import pygame.time

import global_vars
import utils


class Unit:
	def __init__(self, power, movement_points, unit_type, name, hexagon=global_vars.game_map.get_random_hex()):
		self.surface = utils.get_adopted_image(unit_type, global_vars.UNIT_SIZE)
		self.name = name
		self.occupied_hex = hexagon
		self.coordinates = self.get_coordinates(self.occupied_hex)
		self.is_selected = False
		self.is_stacked = False
		self.power = power
		self.movement_points = movement_points
		self.current_power = power
		self.current_movement_points = movement_points
		if name is None:
			self.parameters_text = global_vars.unit_font.render(
				''.join(str(power) + ' - ' + str(movement_points)), 1, global_vars.WHITE)
		else:
			self.parameters_text = global_vars.unit_font.render(self.name, 1, global_vars.WHITE)
		self.parameters_position = self.parameters_text.get_rect(center=global_vars.UNIT_PARAM_OFF)
		self.surface.blit(self.parameters_text, self.parameters_position)

	def write_unit_info(self, surface):
		if self.name is None:
			info_text = global_vars.font.render(
				''.join('MP: ' + str(self.current_movement_points)), 1, global_vars.DARK_GREEN)
		else:
			info_text = global_vars.font.render(self.name, 1, global_vars.DARK_GREEN)
		info_position = info_text.get_rect(topleft=(global_vars.TEXT_OFFSET, int(global_vars.RATIO) * 16))
		surface.blit(info_text, info_position)

	def is_possible_to_move(self, hexagon):
		print(self.occupied_hex)
		print(hexagon)
		if not self.occupied_hex.is_adjacent(hexagon):
			return False
		river = 1 if self.crossing_the_river(hexagon) else 0
		if self.uses_road_movement(hexagon):
			mp_factor = self.current_movement_points - 1 - river >= 0
		else:
			mp_factor = self.current_movement_points - self.occupied_hex.terrain.movement_cost - river >= 0
		stack_limit = True
		return self.occupied_hex.is_adjacent(hexagon) and mp_factor and stack_limit

	def uses_road_movement(self, hexagon):
		return global_vars.game_map.connected_by_road(self.occupied_hex, hexagon)

	def crossing_the_river(self, hexagon):
		return global_vars.game_map.is_river_on_edge(self.occupied_hex, hexagon)

	def move(self, hexagon):
		if self.is_possible_to_move(hexagon):
			global_vars.MOVE_SOUND.play()
			pygame.time.wait(50)
			self.coordinates = self.get_coordinates(hexagon)
			self.current_movement_points -= 1 if self.uses_road_movement(hexagon) else hexagon.terrain.movement_cost
			self.current_movement_points -= 1 if self.crossing_the_river(hexagon) else 0
			self.occupied_hex = hexagon

	def select(self):
		global_vars.SELECT_SOUND.play()
		pygame.time.wait(250)
		self.is_selected = True

	def unselect(self):
		self.is_selected = False

	def get_coordinates(self, hexagon):
		self.coordinates = list(hexagon.relative_position)
		self.coordinates[0] -= global_vars.UNIT_WIDTH / 2
		self.coordinates[1] -= global_vars.UNIT_HEIGHT / 2
		return self.coordinates

	def appear(self):
		self.coordinates = self.get_coordinates(self.occupied_hex)
		global_vars.game_map.screen.map_surface.blit(self.surface, self.coordinates)

	def restore_movement_points(self):
		self.current_movement_points = self.movement_points

