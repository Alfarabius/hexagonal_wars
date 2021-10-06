from pygame import font

from global_sizes import Sizes


class Fonts:
	font.init()
	UI_FONT = font.SysFont('arial', Sizes.UI_FONT)
	INFO = font.SysFont('arial', int(Sizes.RATIO * 3))


class Colors:
	WHITE = (255, 255, 255)
	RED = (255, 0, 0)
	DARK_GREEN = (0, 50, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)
	BLACK = (0, 0, 0)
	FILL = (210, 210, 210)
	SELECT = (200, 0, 0)
	INFO = (203, 193, 163)
	MAP = (240, 255, 240)
	ROAD = (230, 210, 200)
	RIVER = (0, 150, 255)
