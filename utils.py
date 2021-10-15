import json
import random
import threading

import pygame

from global_sizes import Sizes

FORMAT = '.png'


def launch_thread(function) -> threading.Thread:
	new_thread = threading.Thread(target=function)
	new_thread.setDaemon(True)
	new_thread.start()
	return new_thread


def get_adopted_image(path, size) -> pygame.Surface:
	try:
		image = pygame.image.load(path + FORMAT).convert_alpha()
	except Exception as error:
		print(f'Exception, while reading {path + FORMAT} - {error}')
		raise SystemExit()
	image = pygame.transform.smoothscale(image, size)
	return image


def get_adopted_image_format(path, size) -> pygame.Surface:
	try:
		image = pygame.image.load(path).convert_alpha()
	except Exception as error:
		print(f'Exception, while reading {path} - {error}')
		raise SystemExit()
	image = pygame.transform.smoothscale(image, size)
	return image


def get_random_color() -> tuple[int, int, int]:
	r = random.randint(1, 254)
	g = random.randint(1, 254)
	b = random.randint(1, 254)
	return r, g, b


def get_brighter_tone(color) -> tuple[int, int, int]:
	brighter_tone = list()
	for component in color:
		brighter_tone.append(component + 30 if component < 226 else 255)
	return brighter_tone[0], brighter_tone[1], brighter_tone[2]


def get_darker_tone(color) -> tuple[int, int, int]:
	darker_tone = list()
	for component in color:
		darker_tone.append(component - 50 if component > 50 else 0)
	return darker_tone[0], darker_tone[1], darker_tone[2]


def roll_d6() -> int:
	return random.randint(1, 6)


def roll_2d6() -> int:
	return roll_d6() + roll_d6()


def get_adopted_value(value) -> float:
	return value * Sizes.RATIO


def get_adopted_height_value(value) -> float:
	return value * Sizes.HEIGHT_RATIO


def json_to_dict(path) -> dict:
	try:
		with open(path, 'r') as file:
			config = dict(json.load(file))
	except Exception as error:
		print(f'Exception, while reading {path} - {error}')
		raise SystemExit()
	return config


def ignore_exception(func):
	def inner(args):
		value = None
		try:
			if args is None:
				func()
			else:
				value = func(*args)
		except Exception as error:
			print(f'Exception {error} was ignored')
		return value
	return inner


def lerp(a, b, t):
	return a + (b - a) * t


def cube_round(cube):
	rx = round(cube[0])
	ry = round(cube[1])
	rz = round(cube[2])

	x_diff = abs(rx - cube[0])
	y_diff = abs(ry - cube[1])
	z_diff = abs(rz - cube[2])

	if x_diff > y_diff and x_diff > z_diff:
		rx = -ry - rz
	elif y_diff > z_diff:
		ry = -rx - rz
	else:
		rz = -rx - ry

	return rx, ry, rz


def plug():
	pass

