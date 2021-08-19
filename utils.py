import random
import global_vars as gb


def get_random_color():
	r = random.randint(1, 254)
	g = random.randint(1, 254)
	b = random.randint(1, 254)
	return r, g, b


def get_random_coordinates():
	x = float(random.randint(1, gb.WIDTH - gb.UNIT_WIDTH))
	y = float(random.randint(1, gb.HEIGHT - gb.UNIT_HEIGHT))
	return [x, y]


def roll_d6():
	return random.randint(1, 6)


def roll_2d6():
	return roll_d6() + roll_d6()