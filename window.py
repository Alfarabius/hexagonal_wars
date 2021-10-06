import pygame

from global_sizes import Sizes


class Window:
	__instance = None

	def __new__(cls, *args, **kwargs):
		if not isinstance(cls.__instance, cls):
			cls.__instance = super(Window, cls).__new__(cls)
		else:
			print('Window already exist')
		return cls.__instance

	def __init__(self, name, flags):
		self.clock = pygame.time.Clock()
		self.width = Sizes.DISPLAY_INFO.current_w
		self.height = Sizes.DISPLAY_INFO.current_h
		self.size = (self.width, self.height)
		self.surface = self._get_window(name, flags)
		self.middle_point = (self.width / 2, self.height / 2)
		self.zero_point = (0, 0)

	def _get_window(self, name, flags) -> pygame.Surface:
		pygame.display.set_caption(name)
		return pygame.display.set_mode(self.size, flags)

	def update(self):
		pygame.display.update()
		self.clock.tick(64)

	def draw(self, surface):
		self.surface.fill((100, 100, 120))

	def get_point(self, width_divider, height_divider) -> tuple[float, float]:
		return self.width / width_divider, self.height / height_divider
