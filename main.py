import pygame

import game
import global_vars
import utils


def get_next_track(playlist):
	music = playlist.pop()
	playlist.insert(0, music)
	return music


def game_music_play():
	playlist = [
		'sounds/sound_Ambient_full_simple.ogg',
		'sounds/strange.ogg',
		'sounds/slezi.ogg'
	]
	while True:
		while pygame.mixer.music.get_busy():
			pygame.time.wait(100)
		music = get_next_track(playlist)
		pygame.mixer.music.load(music)
		pygame.mixer.music.set_volume(0.05)
		pygame.mixer.music.play()


def main():
	utils.launch_thread(game_music_play)
	game_ = game.Game(global_vars.game_map, ('armies/p1_army.txt', 'armies/p2_army.txt'), None, 9)
	game_.game_loop()


if __name__ == '__main__':
	main()
