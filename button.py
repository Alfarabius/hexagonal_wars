import pygame
from pygame import Rect

import colors
import utils
from global_sizes import Sizes
from constants import Fonts


class Button:
	BORDER_RADIUS = int(Sizes.RATIO)
	ELEVATION = Sizes.RATIO // 3

	def __init__(self, text, size, pos, color, hotkey, function):
		# function
		self.function = function
		self.hotkey = hotkey

		# top surface
		self.top_rect = Rect(pos, size)
		self.top_rect.center = pos
		self.basic_color = color
		self.current_color = color

		# bottom surface
		self.bottom_rect = Rect(pos, size)
		self.bottom_rect.midtop = (pos[0], pos[1] + self.ELEVATION)
		self.bottom_color = utils.get_darker_tone(color)

		# text
		self.text_surface = Fonts.UI_FONT.render(text, True, colors.BLACK)
		self.text_rect = self.text_surface.get_rect(center=self.top_rect.center)

		# state
		self.pressed = False
		self.hotkey_is_pressed = False
		self.block_hotkey = False
		self.elevation = self.ELEVATION
		self.top_y = pos[1]

	def draw(self, surface):
		self.top_rect.y = self.top_y - self.elevation
		self.text_rect.center = self.top_rect.center

		pygame.draw.rect(surface, self.bottom_color, self.bottom_rect, border_radius=self.BORDER_RADIUS)
		pygame.draw.rect(surface, self.current_color, self.top_rect, border_radius=self.BORDER_RADIUS)
		surface.blit(self.text_surface, self.text_rect)

	def click_handler(self, mouse_position, mouse_button_is_pressed):
		if self.top_rect.collidepoint(mouse_position):
			self.block_hotkey = True
			self.current_color = utils.get_brighter_tone(self.basic_color)
			if mouse_button_is_pressed:
				self.elevation = 0
				self.pressed = True
			elif self.pressed:
				self.elevation = self.ELEVATION
				self.function()
				self.pressed = False
		else:
			self.elevation = self.ELEVATION
			self.current_color = self.basic_color
			self.pressed = False
			self.block_hotkey = False

	def hotkey_handler(self):
		if self.block_hotkey:
			return
		if pygame.key.get_pressed()[self.hotkey]:
			self.elevation = 0
			self.hotkey_is_pressed = True
		elif self.hotkey_is_pressed:
			self.elevation = self.ELEVATION
			self.function()
			self.hotkey_is_pressed = False
		else:
			self.elevation = self.ELEVATION
			self.current_color = self.basic_color
			self.hotkey_is_pressed = False
