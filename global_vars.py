import numpy
import pygame

import map
import utils

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.font.init()
pygame.display.init()
pygame.init()

# vars:
display_info = pygame.display.Info()
WIDTH = display_info.current_w
HEIGHT = display_info.current_h
# WIDTH = 1280
# HEIGHT = 800
RATIO = WIDTH / 100
H_RATIO = HEIGHT / 100
SCREEN = (WIDTH, HEIGHT)
# sizes:
RADIAN = numpy.pi / 180
SELECT_SIZE = int(RATIO // 2)
DOT_SIZE = int(RATIO // 6)
FRAME = 0.5 * RATIO
HEX_EDGE = 4 * RATIO
HEX_HEIGHT = HEX_EDGE * numpy.sqrt(3)
HEX_WIDTH = HEX_EDGE * 2
UNIT_WIDTH = int(4.5 * RATIO)
UNIT_HEIGHT = int(4.5 * RATIO)
UNIT_SIZE = (UNIT_WIDTH, UNIT_HEIGHT)
INFO_WIDTH = 25 * RATIO
INFO_HEIGHT = 98.5 * H_RATIO
INFO_SIZE = (int(INFO_WIDTH), int(INFO_HEIGHT))
FONT_SIZE = int(RATIO * 2)
TEXT_OFFSET = int(RATIO) * 1
MAP_WIDTH = 74 * RATIO
MAP_HEIGHT = 98.5 * H_RATIO
MAP_SIZE = (int(MAP_WIDTH), int(MAP_HEIGHT))
OFFSET = FRAME + INFO_WIDTH
HEXES_OFFSET = 20
ROAD_WIDTH = int(RATIO//3)
RIVER_WIDTH = int(RATIO//2)
UNIT_PARAM_OFF = UNIT_WIDTH//2, UNIT_HEIGHT//2 + RATIO * 1.3
TERRAIN_SIZE = (int(HEX_WIDTH - RATIO//8), int(HEX_HEIGHT - RATIO//8))
# time constants:
FPS = 90
# names and paths:
NAME = "I had a comrade"
ICO = "assets/ico.bmp"
pygame.display.set_caption(NAME)
_screen_flags = pygame.FULLSCREEN
window = pygame.display.set_mode(SCREEN, _screen_flags)
window.fill((255, 255, 255))
FORMAT = ".bmp"
if pygame.image.get_extended():
	FORMAT = '.png'

OPEN = utils.get_adopted_image('assets/open0', TERRAIN_SIZE)
CAPITAL = utils.get_adopted_image('assets/capital0', TERRAIN_SIZE)
CITY = utils.get_adopted_image('assets/city0', TERRAIN_SIZE)
FOREST = utils.get_adopted_image('assets/forest0', TERRAIN_SIZE)
HILL = utils.get_adopted_image('assets/hill0', TERRAIN_SIZE)
MOUNTAIN = utils.get_adopted_image('assets/mountain0', TERRAIN_SIZE)
TOWN = utils.get_adopted_image('assets/town0', TERRAIN_SIZE)
# units:
BLACK_ELITE_CAVALRY = 'assets/black_elite_cavalry0'
BLACK_MECH_INFANTRY = 'assets/black_mech_infantry0'
BLACK_INFANTRY = 'assets/black_infantry0'
BLACK_GREEN_INFANTRY = 'assets/black_infantry0'
BLACK_ELITE_INFANTRY = 'assets/black_elite_infantry0'
BLACK_LEADER = 'assets/black_leader0'
BLACK_MILITIA = 'assets/black_militia0'
BLACK_FANATIC_MILITIA = 'assets/black_fanatic_militia0'
RED_CAVALRY = 'assets/red_cavalry0'
RED_CAVALRY_RECON = 'assets/red_cavalry_recon0'
RED_ELITE_CAVALRY = 'assets/red_elite_cavalry0'
RED_MECH_INFANTRY = 'assets/red_mech_infantry0'
RED_RECON_INFANTRY = 'assets/red_mech_infantry0'
RED_INFANTRY = 'assets/red_infantry0'
RED_LEADER = 'assets/red_leader0'
RED_MARINE = 'assets/red_marine0'
RED_RECON_MARINE = 'assets/red_marine0'
RED_MILITIA = 'assets/red_militia0'
RED_POLIT_INFANTRY = 'assets/red_polit_infantry0'

UNIT_TYPES_DICT = {
	'BMI': BLACK_MECH_INFANTRY,
	'BEI': BLACK_ELITE_INFANTRY,
	'BI': BLACK_INFANTRY,
	'BGI': BLACK_GREEN_INFANTRY,
	'BFM': BLACK_FANATIC_MILITIA,
	'BM': BLACK_MILITIA,
	'BL': BLACK_LEADER,
	'REC': RED_ELITE_CAVALRY,
	'RC': RED_CAVALRY,
	'RRC': RED_CAVALRY_RECON,
	'RI': RED_INFANTRY,
	'REI': RED_MECH_INFANTRY,
	'RPI': RED_POLIT_INFANTRY,
	'RRI': RED_RECON_INFANTRY,
	'RM': RED_MARINE,
	'RRM': RED_RECON_MARINE,
	'RMI': RED_MILITIA,
	'RL': RED_LEADER,
}
# colors:
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_GREEN = (0, 50, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)
FILL_COLOR = (210, 210, 210)
SELECT_COLOR = (200, 0, 0)
INFO_COLOR = (203, 193, 163)
MAP_COLOR = (240, 255, 240)
ROAD_COLOR = (230, 210, 200)
# points:
ZERO_POINT = (0, 0)
# HEX:
HEX_EDGES = {
	(-1, +1, 0): 0,
	(0, +1, -1): 1,
	(+1, 0, -1): 2,
	(+1, -1, 0): 3,
	(0, -1, +1): 4,
	(-1, 0, +1): 5
}
# speeds:
SCROLL_SPEED = int(HEX_EDGE // 4)
# font:
font = pygame.font.SysFont('arial', FONT_SIZE)
unit_font = pygame.font.SysFont('calibri', int(RATIO))
# sounds:
BUTTON_SOUND = pygame.mixer.Sound('sounds/point.ogg')
BUTTON_SOUND.set_volume(0.3)
SELECT_SOUND = pygame.mixer.Sound('sounds/end_turn.ogg')
SELECT_SOUND.set_volume(0.3)
MOVE_SOUND = pygame.mixer.Sound('sounds/inf.ogg')
MOVE_SOUND.set_volume(0.3)
# map:
game_map = map.Map('maps/map_0.map')
INFO_SURFACE = game_map.screen.info_surface
