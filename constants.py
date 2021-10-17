from pygame import font

from global_sizes import Sizes

FPS = 60


class Fonts:
	font.init()
	UI = font.SysFont('arial', Sizes.UI_FONT)
	PIXEL = font.Font('fonts/editundo.ttf', Sizes.UI_FONT)
	PIXEL_1 = font.Font('fonts/ka1.ttf', Sizes.UI_FONT)
	PIXEL_2 = font.Font('fonts/manaspc.ttf', Sizes.UI_FONT)
	PIXEL_3 = font.Font('fonts/ARCADECLASSIC.TTF', Sizes.UI_FONT)
	PIXEL_3_TITLE = font.Font('fonts/ARCADECLASSIC.TTF', int(Sizes.RATIO * 2.4))
	PIXEL_4 = font.Font('fonts/prstart.ttf', Sizes.UI_FONT)
	PIXEL_5 = font.Font('fonts/pcsenior.ttf', Sizes.UI_FONT)
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


hk_font_title = font.Font('fonts/editundo.ttf', int(Sizes.RATIO * 2.4))
hk_font = font.Font('fonts/editundo.ttf', int(Sizes.RATIO * 2))
color = Colors.INFO

HOTKEYS = [
	hk_font_title.render('Hot Keys:', False, Colors.DARK_GREEN),
	hk_font.render('Select, Move: LMB', False, color),
	hk_font.render('Unselect: RMB', False, color),
	hk_font.render('Scroll: W, A, S, D', False, color),
	hk_font.render('End Turn: E', False, color),
	hk_font.render('Attack: SpaceBar, LMB', False, color),
	hk_font.render('Choice: 1, 2, 3, ... ', False, color),
	hk_font.render('Next unit: TAB', False, color)
]

digit_font = font.Font('fonts/pcsenior.ttf', int(Sizes.RATIO * 1.2))

DIGITS = [
	digit_font.render('0', False, color),
	digit_font.render('1', False, color),
	digit_font.render('2', False, color),
	digit_font.render('3', False, color),
	digit_font.render('4', False, color),
	digit_font.render('5', False, color),
	digit_font.render('6', False, color),
	digit_font.render('7', False, color),
	digit_font.render('8', False, color),
	digit_font.render('9', False, color)
]
