import pygame

import game
import global_vars


def game_music_play():
	pygame.mixer.music.load('sounds/sound_Ambient_full_simple.ogg')
	pygame.mixer.music.set_volume(0.1)
	pygame.mixer.music.play(-1)


def main():
	game_ = game.Game(global_vars.game_map, ('armies/p1_army.txt', 'armies/p2_army.txt'), None, 9)
	game_music_play()
	while game_.is_running:
		game_.game_loop()


if __name__ == '__main__':
	main()
