import pygame

import globals


class Screen:
	def __init__(self, col, row):
		self.width = col * globals.HEX_EDGE * 1.5 + globals.HEXES_OFFSET * 4
		self.height = row * globals.HEX_EDGE * 1.8 + globals.HEXES_OFFSET * 2
		self.top_left = [0, 0]
		self.info_surface = pygame.Surface(globals.INFO_SIZE)
		self.map_surface = pygame.Surface(globals.MAP_SIZE)
		self.scroll_zone = pygame.Surface((globals.MAP_WIDTH + globals.FRAME, globals.HEIGHT))
		self.not_scroll_zone = pygame.Surface((globals.MAP_WIDTH - globals.RATIO*4, globals.HEIGHT - globals.H_RATIO*6))
		self.info_color = globals.INFO_COLOR
		self.map_color = globals.MAP_COLOR

	def scroll_possible(self, direction):
		if direction == (0, 1) and self.top_left[1] > 0:     # UP
			return True
		if direction == (0, -1) and self.top_left[1] < self.height - globals.MAP_HEIGHT:     # DOWN
			return True
		if direction == (1, 0) and self.top_left[0] > 0:    # LEFT
			return True
		if direction == (-1, 0) and self.top_left[0] < self.width - globals.MAP_WIDTH:  # RIGHT
			return True
		return False

	def draw(self):
		map_offset = globals.FRAME + globals.INFO_WIDTH
		globals.window.blit(self.info_surface, (globals.FRAME, globals.FRAME))
		globals.window.blit(self.map_surface, (map_offset, globals.FRAME))
		self.info_surface.fill(self.info_color)
		self.map_surface.fill(self.map_color)
