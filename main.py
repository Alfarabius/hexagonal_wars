import pygame

import music_player
from game import HexagonalWarGame
from window import Window


def initialization():
	if not pygame.image.get_extended():
		raise 'image format error'
	pygame.fastevent.init()
	pygame.init()


def main():
	initialization()
	music_player.MusicPlayer(music_player.PLAYLIST, 0.05).launch_thread()
	game_window = Window('hexagonal wars', pygame.FULLSCREEN)
	new_game = HexagonalWarGame('configs/game.json', game_window)
	new_game.start()


if __name__ == '__main__':
	main()
