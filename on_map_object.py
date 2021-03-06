import os

import pygame

from pygame import sprite

import sounds
from global_sizes import Sizes
from constants import Colors, Fonts


class OnMapObject(sprite.Sprite):

	def __init__(self, hexagon, path: str, group: sprite.Group, timer, name):
		# parent init
		super().__init__(group)

		# place
		self.occupied_hexagon = hexagon
		self.occupied_hexagon.container.add_unit(self)

		# view
		self.image = pygame.image.load(path + '.png').convert_alpha()
		self.image_buffer = self.image.copy()
		self._hud_image = self.image.copy()
		self.rect = self.image.get_rect(center=self.occupied_hexagon.position)

		self.timer = timer

	def draw(self, surface):
		surface.blit(self.image, self.rect)

	def change_image(self, new_image: pygame.Surface):
		self.image_buffer = new_image

	def change_hexagon(self, hexagon):
		self.occupied_hexagon.container.remove_unit()
		self.occupied_hexagon = hexagon
		self.occupied_hexagon.container.add_unit(self)

	def is_unit_inside_hexagon(self, hexagon) -> bool:
		return self.occupied_hexagon == hexagon


class Animations(dict):
	animations: dict[str: (str, ...), ...]
	__instances = []

	def __new__(cls, *args, **kwargs):
		for instance in cls.__instances:
			if args[1] == instance.name:
				return instance
		new_instance = super(Animations, cls).__new__(cls)
		cls.__instances.append(new_instance)
		return new_instance

	def __init__(self, path: str, name: str):
		animations = dict()
		self.name = name

		try:
			keys = os.listdir(path)
		except FileNotFoundError:
			print('assets/ directory or it`s content are corrupted or does not exist')
			raise SystemExit()
		for key in keys:
			files = os.listdir(path + key)
			image = []
			for file in files:
				image.append(pygame.image.load('/'.join((path, key, file))).convert_alpha())
			animations.update({key: image})
		super().__init__(animations)


class Unit(OnMapObject):
	PATH = 'assets/'
	DIRECTIONS = ['right', 'left']
	STATES = ['move', 'attack', 'idle']
	SPEED = 12

	def __init__(self, timer, hexagon, name: str, group: sprite.Group, power: int, movement: int, direction: int):
		# states
		self.is_alive = True
		# 'move', 'attack', 'idle'
		self.state = 'idle'
		# 'left', 'right'
		self.direction = self.DIRECTIONS[direction - 1]
		self.path = self.PATH + name + '/'

		path = self.path + self.state + '_' + self.direction + '/' + 'idle1' + self.direction[0]
		super().__init__(hexagon, path, group, timer, name)

		# parameters
		self.attacks = 1
		self.name = name
		self.max_power = power
		self.max_movement = movement
		self.power = power
		self.movement = movement

		self.info = self._create_container()

		# animation
		self.animations = Animations(self.path, self.name)
		self.animation_frames = self.animations.get(self.state + '_' + self.direction)
		self.current_frame = 0
		self.current_speed = self.SPEED * self.timer.dt

		# sounds
		self.move_sound = sounds.SOUNDS.march if self.name[0] == 'i' or self.name[0] == 'a' else sounds.SOUNDS.move

	def update(self):
		if not self.is_alive:
			self.eliminate()

		self.current_speed = self.SPEED * self.timer.dt

		self.info = self._create_container()

		if self.state == 'attack' and self.current_frame + self.current_speed >= len(self.animation_frames):
			self.change_frame(self.current_speed)
			self.stop()

		self.change_frame(self.current_speed)
		self.image = self.image_buffer

		if self.state == 'move':
			self.change_position(Sizes.RATIO * 10 * self.timer.dt)
		else:
			self.rect.center = self.occupied_hexagon.position

	def move(self, hexagon):
		self.state = 'move'
		self.move_sound.play()
		self.movement -= 1

		self.turning_checker(hexagon)

		self.change_animation()
		self.change_hexagon(hexagon)

	def attack(self, hexagon) -> int:
		self.state = 'attack'
		sounds.SOUNDS.attack.play()
		self.attacks -= 1

		self.turning_checker(hexagon)

		self.change_animation()
		return self.power

	def stop(self):
		self.state = 'idle'
		self.rect.center = self.occupied_hexagon.position
		self.change_animation()

	def change_direction(self):
		self.direction = self.DIRECTIONS[self.DIRECTIONS.index(self.direction) - 1]

	def change_animation(self):
		self.current_frame = 0
		self.animation_frames = self.animations.get(self.state + '_' + self.direction)

	def change_frame(self, speed):
		self.image_buffer = self.animation_frames[int(self.current_frame)]
		self.current_frame += speed

		if self.current_frame >= len(self.animation_frames):
			self.current_frame = 0

	def change_position(self, speed):

		rounded_position = (
			round(self.occupied_hexagon.position[0]),
			round(self.occupied_hexagon.position[1])
		)

		if self.rect.center == rounded_position:
			self.stop()
			return

		x_direction = 1
		y_direction = 1

		if self.rect.centerx > rounded_position[0]:
			x_direction = -1
		elif self.rect.centerx == rounded_position[0]:
			x_direction = 0

		if self.rect.centery > rounded_position[1]:
			y_direction = -1
		elif self.rect.centery == rounded_position[1]:
			y_direction = 0

		y_speed = speed * y_direction
		x_speed = speed * x_direction

		new_y = self.rect.centery + y_speed
		new_x = self.rect.centerx + x_speed

		self.rect.centerx = rounded_position[0] if abs(rounded_position[0] - new_x) < speed else new_x
		self.rect.centery = rounded_position[1] if abs(rounded_position[1] - new_y) < speed else new_y

	def restore(self):
		self.movement = self.max_movement
		self.attacks = 1

	def destroy(self):
		self.is_alive = False

	def eliminate(self):
		if self.state == 'idle':
			self.occupied_hexagon.container.remove_unit()
			self.kill()

	def retreat(self, hexagon):
		if hexagon is None:
			self.eliminate()
		self.movement += 1 if self.movement < self.max_movement else 0
		self.move(hexagon)

	def turning_checker(self, hexagon):
		if self.occupied_hexagon.position[0] > hexagon.position[0] and self.direction == 'right' \
			or self.occupied_hexagon.position[0] < hexagon.position[0] and self.direction == 'left':
			self.change_direction()

	def _create_container(self) -> list:
		info = []
		font = Fonts.PIXEL_3
		color = Colors.INFO
		name = self.name.split('_')[0]
		info.append(self._hud_image)
		info.append(font.render(name, False, color))
		info.append(font.render(''.join('Power   ' + str(self.max_power)), False, color))
		info.append(font.render(''.join('MP   ' + str(self.movement)), False, color))
		info.append(font.render(''.join('Attacks   ' + str(self.attacks)), False, color))
		return info
