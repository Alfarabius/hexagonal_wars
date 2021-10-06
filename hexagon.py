import math

import pygame

import utils
from constants import Fonts, Colors
from global_sizes import Sizes
from on_map_object import Unit

HEX_EDGE = Sizes.RATIO * 3
HEX_SIZE = (HEX_EDGE * 2.0, HEX_EDGE * math.sqrt(3.0))
RADIAN = math.pi / 180
TYPES = {
		'flat_topped': (0, math.sqrt(3), 2),
		'pointy_topped': (30, 2, math.sqrt(3))
	}
BLACK = (0, 0, 0)


class Terrain:
	TERRAN_TABLE = {
		'rock': (False, True),
		'open': (True, False)
	}

	def __init__(self, terrain_type):
		self.type = terrain_type
		self.is_passable = self.TERRAN_TABLE.get(self.type)[0]
		self.is_los_block = self.TERRAN_TABLE.get(self.type)[1]


class Space:
	PATH = 'assets/terrain/'

	def __init__(self, terrain: Terrain, size: tuple):
		self.terrain = terrain

		self.image = utils.get_adopted_image(self.PATH + self.terrain.type, size)
		self.rect = self.image.get_rect()

		self.unit = None

	def is_passable(self):
		return self.terrain.is_passable

	def draw(self, surface: pygame.Surface, position):
		self.rect = self.image.get_rect(center=position)
		surface.blit(self.image, self.rect)

	def add_unit(self, unit: Unit):
		self.unit = unit

	def remove_unit(self):
		self.unit = None


class Hexagon:
	def __init__(self, coordinates, edge, type_, container: Space = None):
		self.axial = coordinates
		self.cube: [int, int, int] = self._axial_to_cube_coordinates()

		self.edge_len = edge
		self.width = edge * TYPES.get(type_)[2]
		self.height = edge * TYPES.get(type_)[1]

		self.type = type_
		self.adjacent_hexes = None

		self.position = self.get_center_coordinates()

		self.corners = self._get_corners()

		self.container = container

		self.info = self._create_container()

	def _get_corner_point(self, num) -> tuple[float, float]:
		angle_degree = 60 * num - TYPES.get(self.type)[0]
		angle_radian = RADIAN * angle_degree
		x = self.position[0] + self.edge_len * math.cos(angle_radian)
		y = self.position[1] + self.edge_len * math.sin(angle_radian)
		return x, y

	def _get_corners(self) -> tuple[tuple[float, float], ...]:
		return tuple((self._get_corner_point(i) for i in range(6)))

	def _axial_to_cube_coordinates(self) -> tuple[int, int, int]:
		x = self.axial[0]
		z = self.axial[1] - (self.axial[0] - (self.axial[0] & 1)) // 2
		y = -x - z
		return x, y, z

	def get_center_coordinates(self) -> tuple[float, float]:
		width = self.edge_len * 2
		x = self.axial[0] * width * 3 / 4 + self.edge_len
		y = self.axial[1] * self.height + (self.axial[0] & 1) * self.height / 2 + self.edge_len
		return x + self.edge_len, y + self.edge_len

	def is_point_inside_hexagon(self, x, y, offset) -> bool:
		new_x = x - offset
		dx = abs(self.position[0] - new_x) / self.height
		dy = abs(self.position[1] - y) / self.height
		a = 0.29 * math.sqrt(3.0)
		return dy <= a and (a * dx + 0.25 * dy) <= 0.57 * a
		# (new_x - self.position[0])**2 + (y - self.position[1])**2 < (self.height / 2)**2

	def distance_to_hex(self, hexagon) -> int:
		coordinate = list()
		for i in range(3):
			coordinate.append(abs(self.cube[i] - hexagon.cube[i]))
		return max(coordinate[0], coordinate[1], coordinate[2])

	def is_adjacent(self, hexagon) -> bool:
		return self.distance_to_hex(hexagon) == 1

	def get_edge_midpoint(self, num):
		distance = self.height / 2
		angle_deg = 60 * num - 30
		angle_rad = RADIAN * angle_deg
		x = self.position[0] + distance * math.cos(angle_rad)
		y = self.position[1] + distance * math.sin(angle_rad)
		return x, y

	def draw_edge(self, color, edge, width, surface):
		edge -= 3 if edge >= 3 else -3
		self.corners = tuple((self._get_corner_point(i) for i in range(6)))
		next_point = edge + 1 if edge < 5 else 0
		pygame.draw.line(surface, color, self.corners[edge], self.corners[next_point], width)

	def draw_normal_to_edge(self, color, edge, width, surface):
		edge += 4 if edge < 2 else -2
		edge_midpoint = self.get_edge_midpoint(edge)
		pygame.draw.line(surface, color, self.position, edge_midpoint, width)

	def draw(self, surface):
		if self.container is not None:
			self.container.draw(surface, self.position)
			return

	def draw_midpoint(self, surface, size, color):
		pygame.draw.circle(surface, color, self.position, size)

	def change_hex_position(self, offset_x, offset_y) -> tuple[float, float]:
		new_x_position = self.position[0] + offset_x
		new_y_position = self.position[1] + offset_y
		return new_x_position, new_y_position

	def get_adjacent_hexagons(self, game_map):
		self.adjacent_hexes = game_map.get_adjacent_hexes(self)

	def _create_container(self) -> list:
		container = []
		font = Fonts.INFO
		color = Colors.DARK_GREEN
		container.append(self.container.image)
		container.append(font.render(''.join(str('Type: ' + self.container.terrain.type)), True, color))

		return container
