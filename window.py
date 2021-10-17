import pygame

import constants
from global_sizes import Sizes


class Window:
	W = 640
	H = 480

	__instance = None

	def __new__(cls, *args, **kwargs):
		if not isinstance(cls.__instance, cls):
			cls.__instance = super(Window, cls).__new__(cls)
		else:
			print('Window already exist')
		return cls.__instance

	def __init__(self, name, flags):

		# name
		self.name = name

		# clock
		self.clock = pygame.time.Clock()

		# size
		self.width = Sizes.DISPLAY_INFO.current_w
		self.height = Sizes.DISPLAY_INFO.current_h
		self.size = (self.width, self.height)

		# surface
		self.surface = self.get_window(flags)

		# points
		self.middle_point = (self.width / 2, self.height / 2)
		self.zero_point = (0, 0)

		# states
		self.fullscreen = True

	def get_window(self, flags) -> pygame.Surface:
		pygame.display.set_caption(self.name)
		return pygame.display.set_mode(self.size, flags)

	def update(self):
		pygame.display.update()
		self.clock.tick(constants.FPS)

	def draw(self, surface):
		self.surface.fill((100, 100, 120))

	def get_point(self, width_divider, height_divider) -> tuple[float, float]:
		return self.width / width_divider, self.height / height_divider
