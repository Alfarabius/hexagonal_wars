import pygame

import global_vars
import utils


class Screen:
	def __init__(self, col, row):
		self.width = col * global_vars.HEX_EDGE * 1.5 + global_vars.HEXES_OFFSET * 4
		self.height = row * global_vars.HEX_EDGE * 1.8 + global_vars.HEXES_OFFSET * 2
		self.top_left = [0, 0]
		self.info_surface = pygame.Surface(global_vars.INFO_SIZE)
		self.frame_surface = utils.get_adopted_image('assets/frame', global_vars.SCREEN)
		self.frame_position = self.frame_surface.get_rect(topleft=(0, 0))
		self.map_surface = pygame.Surface(global_vars.MAP_SIZE)
		self.scroll_zone = pygame.Surface((global_vars.MAP_WIDTH + global_vars.FRAME, global_vars.HEIGHT))
		self.not_scroll_zone = pygame.Surface((global_vars.MAP_WIDTH - global_vars.RATIO * 4, global_vars.HEIGHT - global_vars.H_RATIO * 6))
		self.info_color = global_vars.INFO_COLOR
		self.map_color = global_vars.MAP_COLOR

	def scroll_possible(self, direction):
		if direction == (0, 1) and self.top_left[1] > 0:     # UP
			return True
		if direction == (0, -1) and self.top_left[1] < self.height - global_vars.MAP_HEIGHT:     # DOWN
			return True
		if direction == (1, 0) and self.top_left[0] > 0:    # LEFT
			return True
		if direction == (-1, 0) and self.top_left[0] < self.width - global_vars.MAP_WIDTH:  # RIGHT
			return True
		return False

	def draw(self):
		map_offset = global_vars.FRAME + global_vars.INFO_WIDTH
		global_vars.window.blit(self.info_surface, (global_vars.FRAME, global_vars.FRAME))
		global_vars.window.blit(self.map_surface, (map_offset, global_vars.FRAME))
		self.info_surface.fill(global_vars.INFO_COLOR)
		global_vars.window.blit(self.frame_surface, self.frame_position)
		self.map_surface.fill(self.map_color)
