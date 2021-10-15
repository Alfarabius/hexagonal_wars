import math

import pygame

import utils
from global_sizes import Sizes
from hexagon import Hexagon, Space, Terrain

HEX_EDGES = {
	(-1, +1, 0): 0,
	(0, +1, -1): 1,
	(+1, 0, -1): 2,
	(+1, -1, 0): 3,
	(0, -1, +1): 4,
	(-1, 0, +1): 5
}


class Map:
	HEX_EDGE = Sizes.RATIO * 3
	HEX_SIZE = (HEX_EDGE * 2, HEX_EDGE * math.sqrt(3))
	HEX_SIZE_INT = (int(HEX_SIZE[0]), int(HEX_SIZE[1]))
	SCROLL_SPEED = int(HEX_EDGE * 6)

	def __init__(self, path, timer):
		self.spaces = []
		self.fov_top_left = [0, 0]
		self._parse_map(path)

		self.hexes = self._create_map(self.HEX_EDGE)

		self.width = self.size[0] * self.HEX_EDGE * 1.55 + self.HEX_EDGE
		self.height = self.size[1] * self.HEX_EDGE * 1.8 + self.HEX_EDGE

		self.surface = pygame.Surface((int(self.width),	int(self.height)))
		self.rect = self.surface.get_rect(topleft=(25 * Sizes.RATIO, 0))

		self.timer = timer

		self.scroll_speed = self.SCROLL_SPEED * self.timer.dt
		self.scroll_lock = False

	def _parse_map(self, path):
		map_config = utils.json_to_dict(path)
		self.size = tuple(map_config.get('size', {'width': 10, 'height': 10}).values())
		self.type = map_config.get('type', 'flat_topped')
		rows = map_config.get('hexes', '')
		for i in range(self.size[1]):
			self.spaces.extend(rows.get('row' + str(i + 1), ['open' in range(self.size[0])]))

	def _create_map(self, edge):
		hexes = []
		for i in range(self.size[1]):
			for j in range(self.size[0]):
				hexes.append(
					Hexagon(
						(j, i),
						edge,
						self.type,
						Space(Terrain(self.spaces[i * self.size[0] + j]), self.HEX_SIZE_INT))
				)
		return hexes

	def update(self):
		if self.scroll_lock:
			return
		self.scroll_speed = self.SCROLL_SPEED * self.timer.dt
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self._scroll_to_direction((1, 0))
		elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self._scroll_to_direction((-1, 0))
		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			self._scroll_to_direction((0, -1))
		elif keys[pygame.K_UP] or keys[pygame.K_w]:
			self._scroll_to_direction((0, 1))

	def draw(self, surface):
		surface.blit(self.surface, self.rect)
		self.surface.fill((150, 200, 150))
		for hexagon in self.hexes:
			hexagon.draw(self.surface)

	def get_hexagon_by_number(self, number):
		return self.hexes[number]

	def get_hexagon_by_axial(self, axial):
		for hexagon in self.hexes:
			if hexagon.axial == axial:
				return hexagon

	def get_hexagon_by_cube(self, cube):
		for hexagon in self.hexes:
			if hexagon.cube == cube:
				return hexagon

	def get_adjacent_hexes(self, target_hex):
		adjacent_hexes = []
		for hexagon in self.hexes:
			if hexagon.is_adjacent(target_hex):
				adjacent_hexes.append(hexagon)
		return adjacent_hexes

	def hexagons_line(self, hex1: Hexagon, hex2: Hexagon):
		length = hex1.distance_to_hex(hex2)
		hexagons = []
		for i in range(length):
			hexagons.append(self.get_hexagon_by_cube(self._cube_lerp(hex1, hex2, 1.0 / length * i)))
		return hexagons

	def _make_scroll_buffer(self, offset_x, offset_y):
		for hexagon in self.hexes:
			hexagon.position = hexagon.change_hex_position(offset_x, offset_y)
			hexagon.unit_position = (
				hexagon.position[0] + hexagon.edge_len,
				hexagon.position[1] + hexagon.edge_len * 0.8
			)

	def _scroll_is_possible(self, direction):
		if direction == (0, 1) and self.fov_top_left[1] > 0:     # UP
			return True
		if direction == (0, -1) and self.fov_top_left[1] < self.height - Sizes.WINDOW_H:     # DOWN
			return True
		if direction == (1, 0) and self.fov_top_left[0] > 0:    # LEFT
			return True
		if direction == (-1, 0) and self.fov_top_left[0] < self.width - Sizes.RATIO * 75:  # RIGHT
			return True
		return False

	def _scroll_to_direction(self, direction):
		if self._scroll_is_possible(direction):
			self._make_scroll_buffer(self.scroll_speed * direction[0], self.scroll_speed * direction[1])
			self.fov_top_left[0] -= self.scroll_speed * direction[0]
			self.fov_top_left[1] -= self.scroll_speed * direction[1]

	def lock_scroll(self):
		self.scroll_lock = True

	def unlock_scroll(self):
		self.scroll_lock = False

	@staticmethod
	def _edge_between(hex1: Hexagon, hex2: Hexagon) -> int:
		offset: list[int, int, int] = []
		for i in range(3):
			offset.append(hex1.cube[i] - hex2.cube[i])
		return HEX_EDGES.get(tuple(offset))

	@staticmethod
	def _cube_lerp(hex1, hex2, t):
		return utils.cube_round((
			utils.lerp(hex1.cube[0], hex2.cube[0], t),
			utils.lerp(hex1.cube[1], hex2.cube[1], t),
			utils.lerp(hex1.cube[2], hex2.cube[2], t)
		))
