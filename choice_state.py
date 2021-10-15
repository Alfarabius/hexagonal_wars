import pygame

import colors
from button import Button
from constants import Colors, Fonts
from global_sizes import Sizes
from modal_window import ModalWindow
from state import State


class Choice(State):

	BUTTON_SIZE = (Sizes.RATIO * 12, Sizes.RATIO * 5)
	HOTKEYS = {
		1: pygame.K_1,
		2: pygame.K_2,
		3: pygame.K_3,
		4: pygame.K_4,
		5: pygame.K_5,
		6: pygame.K_6
	}

	def __init__(self, game, picture_path, text: str, buttons_dict):
		super().__init__(game)

		self.selected_unit = game.state.selected_unit
		self.center = (Sizes.RATIO * 86, Sizes.RATIO * 5)

		offset = 0

		picture = None
		if picture_path:
			picture = Picture(picture_path, self.center)
			offset += picture.height

		new_text = None
		if text:
			new_text = Text(text, self.center, Fonts.PIXEL_5, offset)
			offset += new_text.height

		buttons = []
		for i, label in enumerate(buttons_dict.keys()):
			position = (self.center[0], self.center[1] + (self.BUTTON_SIZE[1] + Sizes.RATIO) * i + Sizes.RATIO + offset)
			buttons.append(Button(
				label,
				self.BUTTON_SIZE,
				position,
				Colors.DARK_GREEN,
				self.HOTKEYS.get(i + 1),
				buttons_dict.get(label)[0],
				buttons_dict.get(label)[1]
			))

		self.modal_window = ModalWindow(picture, new_text, buttons)

	def update(self):
		self.modal_window.update()

	def draw(self, surface):
		self.modal_window.draw(surface)


class Picture:

	FORMAT = '.png'

	def __init__(self, path, left_top: tuple):

		self.surface = pygame.image.load(path + self.FORMAT).convert_alpha()
		self.rect = self.surface.get_rect(center=(left_top[0], left_top[1]))

		self.height = self.surface.get_height()

	def draw(self, surface):
		surface.blit(self.surface, self.rect)

	def update(self):
		pass


class Text:
	def __init__(self, text: str, left_top: tuple, font, offset):

		i = 0
		paragraph = text.split('\n')
		self.sentences = {}

		for i, sentence in enumerate(paragraph):
			surface = font.render(sentence, True, colors.INFO)
			rect = surface.get_rect(center=(left_top[0], left_top[1] + font.get_height() * i + offset))
			self.sentences.update({surface: rect})

		self.height = font.get_height() * (i + 1)

	def draw(self, surface):
		for sentence in self.sentences.keys():
			surface.blit(sentence, self.sentences.get(sentence))

	def update(self):
		pass
