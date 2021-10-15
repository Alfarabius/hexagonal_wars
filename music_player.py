import pygame
import pygame.mixer as mixer

import utils
from utils import launch_thread

PLAYLIST = [
	'music/music_ambient1.ogg'
]


class MusicPlayer:
	__instance = None

	def __new__(cls, *args, **kwargs):
		if not isinstance(cls.__instance, cls):
			cls.__instance = super(MusicPlayer, cls).__new__(cls)
		else:
			print('MusicPlayer already exist')
		return cls.__instance

	def __init__(self, playlist, volume):
		mixer.init()
		self.playlist = playlist
		self.volume = volume

	@staticmethod
	def _get_next_track(playlist):
		music = playlist.pop()
		playlist.insert(0, music)
		return music

	def _music_loop_play(self):
		while True:
			while mixer.music.get_busy():
				pygame.time.wait(100)
			music = self._get_next_track(self.playlist)
			mixer.music.load(music)
			mixer.music.set_volume(self.volume)
			utils.ignore_exception(mixer.music.play)(None)

	def launch_thread(self):
		launch_thread(self._music_loop_play)
