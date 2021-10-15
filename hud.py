from typing import Optional

from pygame import Surface

import button
import utils
from global_sizes import Sizes


class HUD:
	__instance = None

	def __new__(cls, *args, **kwargs):
		if not isinstance(cls.__instance, cls):
			cls.__instance = super(HUD, cls).__new__(cls)
		else:
			print('HUD already exist')
		return cls.__instance

	def __init__(self, image, buttons, size):
		self.surface = utils.get_adopted_image(image, size)
		self.surface_buffer = self.surface.copy()
		self.rect = self.surface.get_rect(topleft=(0, 0))
		self.top_room_position = (Sizes.RATIO * 13, Sizes.RATIO * 5)
		self.mid_room_position = (Sizes.RATIO * 13, Sizes.RATIO * 30)
		self.size = size
		self.buttons: list[button.Button] = buttons
		self.container: Optional[dict] = None

	def set_container(self, container: dict):
		self.container = container

	def update(self):
		for _button in self.buttons:
			_button.update()
		self.surface = self.surface_buffer

	def draw(self, surface: Surface):
		surface.blit(self.surface, self.rect)
		for _button in self.buttons:
			_button.draw(surface)
		self._draw_containers(surface)

	def _draw_containers(self, surface):
		if self.container is None:
			return
		self.__draw_containers(surface, self.container.get('top', 'error'), self.top_room_position)
		self.__draw_containers(surface, self.container.get('mid', 'error'), self.mid_room_position)

	@staticmethod
	def __draw_containers(surface, information: list[Surface, ...], position):
		if information is None:
			return
		step = 0
		for info in information:
			rect = info.get_rect(center=(position[0], position[1] + step))
			step += info.get_height()
			surface.blit(info, rect)
