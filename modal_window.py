import utils
from global_sizes import Sizes


class ModalWindow:

	IMAGE_PATH = 'assets/modal_window'
	SIZE = (int(Sizes.RATIO * 26), int(Sizes.RATIO * 60))

	def __init__(self, picture, text, buttons):
		self.surface = utils.get_adopted_image(self.IMAGE_PATH, self.SIZE)
		self.rect = self.surface.get_rect(center=(Sizes.RATIO * 86, Sizes.RATIO * 31.3))
		self.objects = []
		self.objects.append(picture) if picture else None
		self.objects.append(text) if text else None
		for button in buttons:
			self.objects.append(button)

	def draw(self, surface):
		surface.blit(self.surface, self.rect)
		for obj in self.objects:
			obj.draw(surface)

	def update(self):
		for obj in self.objects:
			obj.update()
