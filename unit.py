import global_vars as gb


class Unit:
	def __init__(self, power, movement_points, unit_type):
		self.surface = unit_type
		self.occupied_hex = gb.game_map.get_random_hex()
		self.coordinates = self.get_coordinates(self.occupied_hex)
		self.is_selected = False
		self.power = power
		self.movement_points = movement_points
		self.current_power = power
		self.current_movement_points = movement_points
		self.parameters_text = gb.unit_font.render(''.join(str(power) + '-' + str(movement_points)), 1, gb.WHITE)
		self.parameters_position = self.parameters_text.get_rect(center=(gb.UNIT_WIDTH//2, gb.UNIT_HEIGHT//2 + 14))
		self.surface.blit(self.parameters_text, self.parameters_position)

	def write_unit_info(self):
		info_text = gb.font.render(''.join('MP: ' + str(self.current_movement_points)), 1, gb.DARK_GREEN)
		info_position = info_text.get_rect(topleft=(gb.TEXT_OFFSET, gb.TEXT_OFFSET * 16))
		gb.INFO_SURFACE.blit(info_text, info_position)

	def is_possible_to_move(self, hexagon):
		river = 1 if self.crossing_the_river(hexagon) else 0
		if self.uses_road_movement(hexagon):
			mp_factor = self.current_movement_points - 1 - river >= 0
		else:
			mp_factor = self.current_movement_points - self.occupied_hex.terrain.movement_cost - river >= 0
		stack_limit = True
		return self.occupied_hex.is_adjacent(hexagon) and mp_factor and stack_limit

	def uses_road_movement(self, hexagon):
		return gb.game_map.connected_by_road(self.occupied_hex, hexagon)

	def crossing_the_river(self, hexagon):
		return gb.game_map.is_river_on_edge(self.occupied_hex, hexagon)

	def move(self, hexagon):
		if self.is_possible_to_move(hexagon):
			self.coordinates = self.get_coordinates(hexagon)
			self.current_movement_points -= 1 if self.uses_road_movement(hexagon) else hexagon.terrain.movement_cost
			self.current_movement_points -= 1 if self.crossing_the_river(hexagon) else 0
			self.occupied_hex = hexagon

	def select(self):
		self.is_selected = True

	def unselect(self):
		self.is_selected = False

	def get_coordinates(self, hexagon):
		self.coordinates = list(hexagon.relative_position)
		self.coordinates[0] -= gb.UNIT_WIDTH / 2
		self.coordinates[1] -= gb.UNIT_HEIGHT / 2
		return self.coordinates

	def appear(self):
		self.coordinates = self.get_coordinates(self.occupied_hex)
		gb.game_map.screen.map_surface.blit(self.surface, self.coordinates)

	def restore_movement_points(self):
		self.current_movement_points = self.movement_points

