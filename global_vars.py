import numpy
import pygame as pg
import pygame.transform

import map

pg.font.init()
pg.display.init()

# vars:
display_info = pg.display.Info()
WIDTH = display_info.current_w
HEIGHT = display_info.current_h
# WIDTH = 640
# HEIGHT = 480
RATIO = WIDTH / 100
H_RATIO = HEIGHT / 100
SCREEN = (WIDTH, HEIGHT)
screen_flags = pg.FULLSCREEN
window = pg.display.set_mode(SCREEN, screen_flags)
# sizes:
RADIAN = numpy.pi / 180
SELECT_SIZE = int(RATIO // 2)
DOT_SIZE = int(RATIO // 6)
FRAME = 0.5 * RATIO
HEX_EDGE = 4 * RATIO
HEX_HEIGHT = HEX_EDGE * numpy.sqrt(3)
HEX_WIDTH = HEX_EDGE * 2
UNIT_WIDTH = 3 * RATIO
UNIT_HEIGHT = 3 * RATIO
UNIT_SIZE = (UNIT_WIDTH, UNIT_HEIGHT)
INFO_WIDTH = 25 * RATIO
INFO_HEIGHT = 98.5 * H_RATIO
INFO_SIZE = (int(INFO_WIDTH), int(INFO_HEIGHT))
FONT_SIZE = int(RATIO * 2)
TEXT_OFFSET = int(RATIO)
MAP_WIDTH = 74 * RATIO
MAP_HEIGHT = 98.5 * H_RATIO
MAP_SIZE = (int(MAP_WIDTH), int(MAP_HEIGHT))
OFFSET = FRAME + INFO_WIDTH
HEXES_OFFSET = 20
ROAD_WIDTH = int(RATIO//3)
RIVER_WIDTH = int(RATIO//2)
# time constants:
FPS = 90
# names and paths:
NAME = "I had a comrade"
ICO = "assets/ico.bmp"
FORMAT = ".bmp"
if pg.image.get_extended():
	FORMAT = '.png'
OPEN_PATH = 'assets/open0' + FORMAT
CAPITAL_PATH = 'assets/capital0' + FORMAT
CITY_PATH = 'assets/city0' + FORMAT
FOREST_PATH = 'assets/road_forest0' + FORMAT
HILL_PATH = 'assets/hill0' + FORMAT
MOUNTAIN_PATH = 'assets/mountain0' + FORMAT
TOWN_PATH = 'assets/town0' + FORMAT
BLACK_INFANTRY_PATH = 'assets/black_mech_infantry0' + FORMAT
RED_INFANTRY_PATH = 'assets/red_mech_infantry0' + FORMAT
OPEN = pg.image.load(OPEN_PATH).convert_alpha()
CAPITAL = pg.image.load(CAPITAL_PATH).convert_alpha()
CITY = pg.image.load(CITY_PATH).convert_alpha()
FOREST = pg.image.load(FOREST_PATH).convert_alpha()
HILL = pg.image.load(HILL_PATH).convert_alpha()
MOUNTAIN = pg.image.load(MOUNTAIN_PATH).convert_alpha()
TOWN = pg.image.load(TOWN_PATH).convert_alpha()
RED_INFANTRY = pg.image.load(RED_INFANTRY_PATH).convert_alpha()
BLACK_INFANTRY = pg.image.load(BLACK_INFANTRY_PATH).convert_alpha()
OPEN = pygame.transform.smoothscale(OPEN, (int(HEX_WIDTH - RATIO//8), int(HEX_HEIGHT - RATIO//8)))
CAPITAL = pygame.transform.smoothscale(CAPITAL, (int(HEX_WIDTH - RATIO//8), int(HEX_HEIGHT - RATIO//8)))
CITY = pygame.transform.smoothscale(CITY, (int(HEX_WIDTH - RATIO//8), int(HEX_HEIGHT - RATIO//8)))
FOREST = pygame.transform.smoothscale(FOREST, (int(HEX_WIDTH - RATIO//8), int(HEX_HEIGHT - RATIO//8)))
HILL = pygame.transform.smoothscale(HILL, (int(HEX_WIDTH - RATIO//8), int(HEX_HEIGHT - RATIO//8)))
MOUNTAIN = pygame.transform.smoothscale(MOUNTAIN, (int(HEX_WIDTH - RATIO//8), int(HEX_HEIGHT - RATIO//8)))
TOWN = pygame.transform.smoothscale(TOWN, (int(HEX_WIDTH - RATIO//8), int(HEX_HEIGHT - RATIO//8)))
RED_INFANTRY = pg.transform.smoothscale(RED_INFANTRY, (int(UNIT_WIDTH), int(UNIT_HEIGHT)))
BLACK_INFANTRY = pg.transform.smoothscale(BLACK_INFANTRY, (int(UNIT_WIDTH), int(UNIT_HEIGHT)))
# colors:
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_GREEN = (0, 50, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)
FILL_COLOR = (210, 210, 210)
SELECT_COLOR = (200, 0, 0)
INFO_COLOR = (220, 220, 220)
MAP_COLOR = (240, 255, 240)
ROAD_COLOR = (230, 210, 200)
# points:
ZERO_POINT = (0, 0)
# HEX:
HEX_EDGES = {(-1, +1, 0): 0, (0, +1, -1): 1, (+1, 0, -1): 2, (+1, -1, 0): 3, (0, -1, +1): 4, (-1, 0, +1): 5}
# speeds:
SCROLL_SPEED = int(HEX_EDGE // 4)
# font:
font = pg.font.SysFont('arial', FONT_SIZE)
unit_font = pg.font.SysFont('calibri', int(RATIO))
# map:
game_map = map.Map('maps/map_0.map')
INFO_SURFACE = game_map.screen.info_surface
