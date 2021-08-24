import numpy
import pygame
import random

import game_screen
import global_vars


class Terrain:
	def __init__(self, terrain_type, settlement, rivers, roads):
		self.type = terrain_type    # open, hill, forest, mountain
		self.settlement = settlement    # city, town, capital
		self.surfaces = self.get_surfaces()
		self.rivers = rivers    # (0, 1, 0, 0, 0, 0)
		self.roads = roads  # (0, 1, 0, 0, 0, 0)
		self.stack_limit = self.get_stack_limit()
		self.movement_cost = self.get_movement_cost()
		self.defence_shift = self.get_defence_shift()

	def get_surfaces(self):
		surf_1 = None
		if self.type == 'open':
			surf_1 = global_vars.OPEN
		elif self.type == 'hill':
			surf_1 = global_vars.HILL
		elif self.type == 'forest':
			surf_1 = global_vars.FOREST
		elif self.type == 'mountain':
			surf_1 = global_vars.MOUNTAIN
		surf_2 = None
		if self.settlement == 'town':
			surf_2 = global_vars.TOWN
		elif self.settlement == 'city':
			surf_2 = global_vars.CITY
		elif self.settlement == 'capital':
			surf_2 = global_vars.CAPITAL
		return surf_1, surf_2

	def get_stack_limit(self):
		value = 3
		if self.settlement == 'city' or 'capital':
			return 6
		elif self.type == 'forest' or 'hill' or 'mountain':
			value = 2
		if self.settlement == 'town':
			return value + 1

	def get_movement_cost(self):
		if self.type == 'mountain':
			return 3
		elif self.type == 'open':
			return 1
		return 2

	def get_defence_shift(self):
		if self.type == 'open':
			return 0
		elif self.settlement == 'city' or 'capital':
			return 2
		return 1


class HexInfoBox:
	def __init__(self, axial, cube_coordinates, terrain):
		self.axial_text = global_vars.font.render(', '.join(str(v) for v in axial), 1, (0, 0, 0))
		self.cube_text = global_vars.font.render(', '.join(str(v) for v in cube_coordinates), 1, (100, 0, 0))
		self.type_text = global_vars.font.render(terrain.type, 1, (0, 0, 0))
		self.settlement_text = global_vars.font.render(terrain.settlement, 1, (0, 0, 0))
		self.rivers_text = global_vars.font.render(str(terrain.rivers), 1, (0, 0, 200))
		self.roads_text = global_vars.font.render(str(terrain.roads), 1, (100, 100, 0))
		self.info_position = self.axial_text.get_rect(topleft=(global_vars.TEXT_OFFSET, global_vars.RATIO * 3))
		self.cube_position = self.cube_text.get_rect(topleft=(global_vars.TEXT_OFFSET, global_vars.RATIO * 5))
		self.type_position = self.type_text.get_rect(topleft=(global_vars.TEXT_OFFSET, global_vars.RATIO * 7))
		self.settlement_position = self.settlement_text.get_rect(topleft=(global_vars.TEXT_OFFSET, global_vars.RATIO * 9))
		self.rivers_position = self.rivers_text.get_rect(topleft=(global_vars.TEXT_OFFSET, global_vars.RATIO * 11))
		self.roads_position = self.roads_text.get_rect(topleft=(global_vars.TEXT_OFFSET, global_vars.RATIO * 13))

	def write_info(self, surface):
		surface.blit(self.axial_text, self.info_position)
		surface.blit(self.cube_text, self.cube_position)
		surface.blit(self.type_text, self.type_position)
		surface.blit(self.settlement_text, self.settlement_position)
		surface.blit(self.rivers_text, self.rivers_position)
		surface.blit(self.roads_text, self.roads_position)


class Hex:
	def __init__(self, col, row, edge, terrain, info):
		self.axial = (col, row)
		self.cube_coordinates = self.axial_to_cube_coordinates()
		self.edge_len = edge
		self.height = global_vars.HEX_HEIGHT
		self.relative_position = self.get_center_coordinates()
		self.corners = tuple((self.get_corner_point(i) for i in range(6)))
		self.terrain = terrain
		self.info_box = HexInfoBox(self.axial, self.cube_coordinates, self.terrain)
		self.units_inside = list()
		self.is_filled = False
		self.is_selected = False

	def get_center_coordinates(self):
		width = self.edge_len * 2
		x = self.axial[0] * width * 3 / 4 + self.edge_len + global_vars.HEXES_OFFSET
		y = self.axial[1] * self.height + (self.axial[0] & 1) * self.height / 2 + self.edge_len + global_vars.HEXES_OFFSET
		return x, y

	def axial_to_cube_coordinates(self):
		x = self.axial[0]
		z = self.axial[1] - (self.axial[0] - (self.axial[0] & 1)) // 2
		y = -x - z
		return x, y, z

	def get_corner_point(self, num):
		angle_deg = 60 * num
		angle_rad = global_vars.RADIAN * angle_deg
		x = self.relative_position[0] + self.edge_len * numpy.cos(angle_rad)
		y = self.relative_position[1] + self.edge_len * numpy.sin(angle_rad)
		return x, y

	def get_edge_midpoint(self, num):
		distance = global_vars.HEX_HEIGHT / 2
		angle_deg = 60 * num - 30
		angle_rad = global_vars.RADIAN * angle_deg
		x = self.relative_position[0] + distance * numpy.cos(angle_rad)
		y = self.relative_position[1] + distance * numpy.sin(angle_rad)
		return x, y

	def draw_edge(self, color, edge, width):
		edge -= 3 if edge >= 3 else -3
		screen = global_vars.game_map.screen.map_surface
		self.corners = tuple((self.get_corner_point(i) for i in range(6)))
		next_point = edge + 1 if edge < 5 else 0
		pygame.draw.line(screen, color, self.corners[edge], self.corners[next_point], width)

	def draw_normal_to_edge(self, color, edge, width):
		edge += 4 if edge < 2 else -2
		screen = global_vars.game_map.screen.map_surface
		edge_midpoint = self.get_edge_midpoint(edge)
		pygame.draw.line(screen, color, self.relative_position, edge_midpoint, width)

	def draw_hex(self, color):
		screen = global_vars.game_map.screen.map_surface
		surface = self.terrain.surfaces
		if surface[0] is not None:
			surface_rect = surface[0].get_rect(center=(self.relative_position[0], self.relative_position[1]))
			screen.blit(surface[0], surface_rect)
		if self.terrain.rivers is not None:
			for edge in range(6):
				if self.terrain.rivers[edge] == 1:
					self.draw_edge(global_vars.BLUE, edge, global_vars.RIVER_WIDTH)
		if self.terrain.roads is not None:
			for edge in range(6):
				if self.terrain.roads[edge] == 1:
					self.draw_normal_to_edge(global_vars.ROAD_COLOR, edge, global_vars.ROAD_WIDTH)
		if surface[1] is not None:
			surface_rect = surface[1].get_rect(center=(self.relative_position[0], self.relative_position[1]))
			screen.blit(surface[1], surface_rect)
		pygame.draw.circle(screen, color, self.relative_position, global_vars.DOT_SIZE)

	def fill_hex(self, color, size):
		self.corners = tuple((self.get_corner_point(i) for i in range(6)))
		pygame.draw.polygon(global_vars.game_map.screen.map_surface, color, self.corners, size)
		self.is_filled = True

	def clear_hex(self):
		self.is_filled = False

	def is_point_inside_hexagon(self, x, y):
		new_x = x - global_vars.OFFSET
		return (new_x - self.relative_position[0])**2 + (y - self.relative_position[1])**2 < (self.height / 2)**2

	def distance_to_hex(self, hexagon):
		coordinate = list()
		for i in range(3):
			coordinate.append(abs(self.cube_coordinates[i] - hexagon.cube_coordinates[i]))
		return max(coordinate[0], coordinate[1], coordinate[2])

	def is_adjacent(self, hexagon):
		if self.distance_to_hex(hexagon) == 1:
			return True
		return False

	def select(self):
		self.is_selected = True

	def change_hex_position(self, off_x, off_y):
		new_x_position = self.relative_position[0] + off_x
		new_y_position = self.relative_position[1] + off_y
		return new_x_position, new_y_position


class Map:
	def __init__(self, file):
		self.file = file
		self.size = self.parse_size()
		self.hexes = list()
		self.screen = game_screen.Screen(self.size[0], self.size[1])
		self.hexes = self.create_map(self.parse_map())

	def create_map(self, terrain):
		info = self.screen.info_surface
		m = self.size[0]
		for i in range(self.size[1]):
			for j in range(self.size[0]):
				self.hexes.extend([(Hex(j, i, global_vars.HEX_EDGE, terrain[i * m + j], info))])
		return self.hexes

	def make_scroll_buffer(self, offset_x, offset_y):
		for that_hex in self.hexes:
			that_hex.relative_position = that_hex.change_hex_position(offset_x, offset_y)
		return True

	def draw_map(self):
		for that_hex in self.hexes:
			that_hex.draw_hex(global_vars.BLUE)
			if that_hex.is_filled:
				that_hex.fill_hex(global_vars.FILL_COLOR, global_vars.SELECT_SIZE)

	def get_random_hex(self):
		rand = random.randint(0, len(self.hexes) - 1)
		return self.hexes[rand]

	def unselect_other_hexes(self, hexagon):
		for that_hex in self.hexes:
			if that_hex != hexagon:
				that_hex.is_selected = False

	@staticmethod
	def _parse_terrain(line):
		line = line.split(', ')
		settlement = line[1] if '0' not in line[1] else None
		rivers = (0, 0, 0, 0, 0, 0) if 'r(' not in line[2] else tuple(int(x) for x in line[2] if x.isdigit())
		roads = (0, 0, 0, 0, 0, 0) if 'p(' not in line[3] else tuple(int(x) for x in line[3] if x.isdigit())
		return Terrain(line[0], settlement, rivers, roads)

	def parse_size(self):
		file = open(self.file, 'r')
		size_str = file.readline()
		size_str = size_str.split(' ')
		return int(size_str[0]), int(size_str[1])

	def parse_map(self):
		terrain = list()
		file = open(self.file, 'r')
		file.readline()
		for line in file:
			if '#' not in line:
				terrain.append(self._parse_terrain(line))
		return terrain

	def scroll(self, pos):
		ret = False
		if global_vars.OFFSET <= pos[0] <= global_vars.WIDTH:
			if 0 <= pos[1] <= global_vars.H_RATIO * 8 and self.screen.scroll_possible((0, 1)):
				ret = self.make_scroll_buffer(0, global_vars.SCROLL_SPEED)      # UP
				self.screen.top_left[1] -= global_vars.SCROLL_SPEED
			elif global_vars.HEIGHT - global_vars.H_RATIO * 8 <= pos[1] <= global_vars.HEIGHT \
				and self.screen.scroll_possible((0, -1)):
				ret = self.make_scroll_buffer(0, -global_vars.SCROLL_SPEED)     # DOWN
				self.screen.top_left[1] += global_vars.SCROLL_SPEED
		if 0 <= pos[1] <= global_vars.HEIGHT:
			if global_vars.OFFSET <= pos[0] <= global_vars.OFFSET + global_vars.RATIO * 8 and self.screen.scroll_possible((1, 0)):
				ret = self.make_scroll_buffer(global_vars.SCROLL_SPEED, 0)      # LEFT
				self.screen.top_left[0] -= global_vars.SCROLL_SPEED
			elif global_vars.WIDTH - global_vars.RATIO * 8 <= pos[0] <= global_vars.WIDTH and self.screen.scroll_possible((-1, 0)):
				ret = self.make_scroll_buffer(-global_vars.SCROLL_SPEED, 0)     # RIGHT
				self.screen.top_left[0] += global_vars.SCROLL_SPEED
		return ret

	def scroll_direct(self, direction):
		if self.screen.scroll_possible(direction):
			self.make_scroll_buffer(global_vars.SCROLL_SPEED * direction[0], global_vars.SCROLL_SPEED * direction[1])
			self.screen.top_left[0] -= global_vars.SCROLL_SPEED * direction[0]
			self.screen.top_left[1] -= global_vars.SCROLL_SPEED * direction[1]
			return True
		return False

	@staticmethod
	def edge_between(hex1, hex2):
		offset = list()
		for i in range(3):
			offset.append(hex1.cube_coordinates[i] - hex2.cube_coordinates[i])
		return global_vars.HEX_EDGES.get(tuple(offset))

	def connected_by_road(self, hex1, hex2):
		edge2 = self.edge_between(hex1, hex2)
		if edge2 is None:
			return False
		edge1 = edge2 + 3 if edge2 < 3 else edge2 - 3
		return hex1.terrain.roads[edge1] == 1 and hex2.terrain.roads[edge2] == 1

	def is_river_on_edge(self, hex1, hex2):
		edge2 = self.edge_between(hex1, hex2)
		if edge2 is None:
			return False
		edge1 = edge2 + 3 if edge2 < 3 else edge2 - 3
		return hex1.terrain.rivers[edge1] == 1 and hex2.terrain.rivers[edge2]

