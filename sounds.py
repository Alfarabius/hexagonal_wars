import pygame


class Sounds:
	def __init__(self, volume):
		pygame.mixer.pre_init(44100, -16, 1, 512)
		pygame.mixer.init()
		self.volume = volume
		self.button = self._setup_sound('sounds/button.wav')
		self.select = self._setup_sound('sounds/select.wav')
		self.move = self._setup_sound('sounds/tracked_move.wav')
		self.march = self._setup_sound('sounds/inf_move.wav')
		self.attack = self._setup_sound('sounds/attack.wav')
		self.wrong = self._setup_sound('sounds/wrong.wav')

	def _setup_sound(self, path) -> pygame.mixer.Sound:
		sound = pygame.mixer.Sound(path)
		sound.set_volume(self.volume)
		return sound


SOUNDS = Sounds(0.3)
