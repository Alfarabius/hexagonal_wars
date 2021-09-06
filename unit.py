import pygame.time

import global_vars
import utils


class Unit:
	def __init__(self, power, movement_points, unit_type, name, hexagon=global_vars.game_map.get_random_hex()):
		self.surface = utils.get_adopted_image(unit_type, global_vars.UNIT_SIZE)
		self.name = name
		self.occupied_hex = hexagon
		self.coordinates = self.get_coordinates(self.occupied_hex, self.occupied_hex.get_units_offset_value())
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

	def write_unit_info(self, surface, x_offset, y_offset):
		if self.name is None:
			info_text = global_vars.unit_font.render(
				''.join('MP: ' + str(self.current_movement_points)), 1, global_vars.BLACK)
		else:
			info_text = global_vars.unit_font.render(self.name, 1, global_vars.BLACK)
		info_position = info_text.get_rect(
			topleft=(global_vars.TEXT_OFFSET + x_offset, int(global_vars.UNIT_HEIGHT * 1.1) + y_offset))
		unit_image_position = self.surface.get_rect(
			topleft=(int(global_vars.RATIO * 0.2) + x_offset, int(global_vars.UNIT_HEIGHT * 0.1) + y_offset))
		surface.blit(self.surface, unit_image_position)
		surface.blit(info_text, info_position)

	def is_possible_to_move(self, hexagon):
		if not self.occupied_hex.is_adjacent(hexagon):
			return False
		river = 1 if self.crossing_the_river(hexagon) else 0
		if self.uses_road_movement(hexagon):
			mp_factor = self.current_movement_points - 1 - river >= 0
		else:
			mp_factor = self.current_movement_points - self.occupied_hex.terrain.movement_cost - river >= 0
		stack_limit = hexagon.units_stack < hexagon.terrain.stack_limit
		return self.occupied_hex.is_adjacent(hexagon) and mp_factor and stack_limit

	def uses_road_movement(self, hexagon):
		return global_vars.game_map.connected_by_road(self.occupied_hex, hexagon)

	def crossing_the_river(self, hexagon):
		return global_vars.game_map.is_river_on_edge(self.occupied_hex, hexagon)

	def move(self, hexagon):
		if self.is_possible_to_move(hexagon):
			global_vars.MOVE_SOUND.play()
			pygame.time.wait(50)
			self.coordinates = self.get_coordinates(hexagon, hexagon.get_units_offset_value())
			self.current_movement_points -= 1 if self.uses_road_movement(hexagon) else hexagon.terrain.movement_cost
			self.current_movement_points -= 1 if self.crossing_the_river(hexagon) else 0
			self.occupied_hex.decrease_unit_stack()
			self.occupied_hex = hexagon
			self.occupied_hex.increase_unit_stack()

	def attack(self):
		return self.power

	def select(self):
		global_vars.SELECT_SOUND.play()
		pygame.time.wait(250)
		self.is_selected = True

	def unselect(self):
		self.is_selected = False

	def get_coordinates(self, hexagon, offset):
		off = offset * (global_vars.RATIO / 5)
		self.coordinates = list(hexagon.relative_position)
		self.coordinates[0] -= global_vars.UNIT_WIDTH / 2 - off
		self.coordinates[1] -= global_vars.UNIT_HEIGHT / 2 - off
		return self.coordinates

	def appear(self, offset):
		self.coordinates = self.get_coordinates(self.occupied_hex, offset)
		global_vars.game_map.screen.map_surface.blit(self.surface, self.coordinates)

	def restore_movement_points(self):
		self.current_movement_points = self.movement_points
