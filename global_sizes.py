import pygame.display


class Sizes:
	pygame.display.init()
	DISPLAY_INFO = pygame.display.Info()
	RATIO = DISPLAY_INFO.current_w / 100
	HEIGHT_RATIO = DISPLAY_INFO.current_h / 100
	WINDOW_H = DISPLAY_INFO.current_h
	WINDOW_W = DISPLAY_INFO.current_w
	MAP_OFFSET = RATIO * 25
	UI_FONT = int(RATIO * 2)
