from pygame import cursors, mouse, key

import hud
from typing import Protocol


class InterfaceObjects(Protocol):
	def update(self): ...


class Interface:
	__instance = None

	def __new__(cls, *args, **kwargs):
		if not isinstance(cls.__instance, cls):
			cls.__instance = super(Interface, cls).__new__(cls)
		else:
			print('Interface already exist')
		return cls.__instance

	def __init__(self, hud_image, buttons, size):
		self._objects: list[InterfaceObjects] = []
		self.keyboard = KeyboardInput()
		self.mouse = MouseInput()
		self.hud = hud.HUD(hud_image, buttons, size)
		self._add_objects([self.mouse, self.keyboard, self.hud])

	def update(self):
		for obj in self._objects:
			obj.update()

	def draw(self, surface):
		self.hud.draw(surface)

	def _add_objects(self, _objects: list[InterfaceObjects]):
		self._objects.extend(obj for obj in _objects)


class KeyboardInput:
	def __init__(self):
		self.pressed_keys = key.get_pressed()

	def handler(self, current_key, function):
		if self.pressed_keys[current_key]:
			function()

	def update(self):
		self.pressed_keys = key.get_pressed()


class MouseInput:
	CURSORS = {
		'SELECT': cursors.arrow,
		'ATTACK': cursors.broken_x,
		'MOVE': cursors.tri_left,
		'SCROLL': cursors.diamond,
		'BALL': cursors.ball
	}

	def __init__(self):
		# states
		self.lmb_is_pressed = False
		self.rmb_is_pressed = False
		self.position = mouse.get_pos()
		self.buttons = mouse.get_pressed(3)

	def update(self):
		self.position = mouse.get_pos()
		self.buttons = mouse.get_pressed(3)

	def set_cursor(self, cursor_type):
		mouse.set_cursor(self.CURSORS.get(cursor_type))

	def lmb_reaction(self, function, args):
		if self.buttons[0]:
			self.lmb_is_pressed = True
		elif self.lmb_is_pressed:
			function(*args) if args is not None else function()
			self.lmb_is_pressed = False

	def rmb_reaction(self, function, args):
		if self.buttons[2]:
			self.rmb_is_pressed = True
		elif self.rmb_is_pressed:
			function(*args) if args is not None else function()
			self.rmb_is_pressed = False

	def get_position(self) -> tuple[int, int]:
		return self.position
