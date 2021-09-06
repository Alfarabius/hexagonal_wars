import random
import threading

import pygame

import global_vars


def launch_thread(function):
	new_thread = threading.Thread(target=function)
	new_thread.setDaemon(True)
	new_thread.start()
	return new_thread


def get_adopted_image(path, size):
	image = pygame.image.load(path + global_vars.FORMAT).convert_alpha()
	image = pygame.transform.smoothscale(image, size)
	return image


def get_random_color():
	r = random.randint(1, 254)
	g = random.randint(1, 254)
	b = random.randint(1, 254)
	return r, g, b


def get_random_coordinates():
	x = float(random.randint(1, global_vars.WIDTH - global_vars.UNIT_WIDTH))
	y = float(random.randint(1, global_vars.HEIGHT - global_vars.UNIT_HEIGHT))
	return [x, y]


def roll_d6():
	return random.randint(1, 6)


def roll_2d6():
	return roll_d6() + roll_d6()