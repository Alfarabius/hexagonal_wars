import os

import pygame

import global_vars
import utils


class Button:
	def __init__(self, path, size, position, text=None):
		self.button_normal = utils.get_adopted_image(path + '_normal', size)
		self.button_hover = utils.get_adopted_image(path + '_hover', size)
		self.button_pushed = utils.get_adopted_image(path + '_pushed', (
			size[0] - int(global_vars.RATIO * 2), size[1] - int(global_vars.RATIO * 2)))
		self.states_images = {
			'normal': (self.button_normal, self.button_normal.get_rect(center=position)),
			'hover': (self.button_hover, self.button_hover.get_rect(center=position)),
			'pushed': (self.button_pushed, self.button_pushed.get_rect(center=position))
		}
		self._is_pushed = False
		self.sound = global_vars.BUTTON_SOUND
		if text is not None:
			self.text = global_vars.font.render(text, True, global_vars.BLACK)
			self.text_position = self.text.get_rect(center=(size[0] // 2, size[1] // 2))
			for surface in self.states_images.values():
				surface[0].blit(self.text, self.text_position)

	def is_pushed(self):
		return bool(self._is_pushed)

	def play_sound(self):
		self.sound.play()
		pygame.time.wait(250)

	def push(self):
		self._is_pushed = True
		self.play_sound()

	def release(self):
		self._is_pushed = False


class Interface:
	def __init__(self):
		self.end_turn_button = \
			Button('assets/button', global_vars.BUTTON_SIZE, (global_vars.RATIO * 10.1, global_vars.RATIO * 2.4))
		self.next_phase_button = \
			Button('assets/button1', global_vars.BUTTON_SIZE, (global_vars.RATIO * 10.1, global_vars.RATIO * 6.6))
		self.main_surface = pygame.Surface((global_vars.RATIO * 20.2, global_vars.RATIO * 21))
		self.main_surface_position = self.main_surface.get_rect(
			topleft=(3 * global_vars.RATIO, 3.3 * global_vars.RATIO))
		self.units_surface = pygame.Surface((global_vars.RATIO * 20.2, global_vars.RATIO * 21))
		self.units_surface_position = self.units_surface.get_rect(
			topleft=(3 * global_vars.RATIO, 27.3 * global_vars.RATIO))
		self.control_surface = pygame.Surface((global_vars.RATIO * 20.2, global_vars.RATIO * 8.6))
		self.control_surface_position = self.control_surface.get_rect(
			topleft=(3 * global_vars.RATIO, 51.4 * global_vars.RATIO))
		self.ability_surface = pygame.Surface((global_vars.RATIO * 50, global_vars.RATIO * 8))
		self.ability_surface_position = self.ability_surface.get_rect(
			topleft=(36.6 * global_vars.RATIO, 52.8 * global_vars.RATIO))

	def draw(self, mouse_position, lmb_is_pressed):
		cursor_is_on_end_turn_button = self.end_turn_button.states_images.get('normal')[1].collidepoint(
				mouse_position[0] - self.control_surface_position.topleft[0],
				mouse_position[1] - self.control_surface_position.topleft[1])
		cursor_is_on_next_phase_button = self.next_phase_button.states_images.get('normal')[1].collidepoint(
				mouse_position[0] - self.control_surface_position.topleft[0],
				mouse_position[1] - self.control_surface_position.topleft[1])
		global_vars.window.blit(self.main_surface, self.main_surface_position)
		self.main_surface.fill(global_vars.INFO_COLOR)
		global_vars.window.blit(self.units_surface, self.units_surface_position)
		self.units_surface.fill(global_vars.INFO_COLOR)
		global_vars.window.blit(self.control_surface, self.control_surface_position)
		self.control_surface.fill(global_vars.INFO_COLOR)
		global_vars.window.blit(self.ability_surface, self.ability_surface_position)
		self.ability_surface.set_alpha(20)
		self.key_handler(cursor_is_on_end_turn_button, lmb_is_pressed, self.end_turn_button)
		self.key_handler(cursor_is_on_next_phase_button, lmb_is_pressed, self.next_phase_button)

	def key_handler(self, cursor_is_on_button, lmb_is_pressed, button):
		if cursor_is_on_button and not lmb_is_pressed:
			self.control_surface.blit(*button.states_images.get('hover'))
			button.release()
		elif cursor_is_on_button and lmb_is_pressed:
			self.control_surface.blit(*button.states_images.get('pushed'))
			button.push()
		else:
			self.control_surface.blit(*button.states_images.get('normal'))
			button.release()


class ModalWindow:
	def __init__(self, buttons_text, text, size, picture=None):
		pygame.image.save(global_vars.window, 'assets/screenshot' + global_vars.FORMAT)
		self.screenshot = pygame.image.load('assets/screenshot' + global_vars.FORMAT)
		self.screenshot.set_alpha(160)
		self.surface = utils.get_adopted_image(global_vars.MODAL_WINDOW, size)
		self.surface_position = self.surface.get_rect(center=global_vars.MIDDLE_POINT)
		self.color_surface = pygame.Surface((global_vars.MODAL_SIZE[0] / 1.05, global_vars.MODAL_SIZE[1] / 1.06))
		self.color_surface_position = self.color_surface.get_rect(center=(size[0] / 2, size[1] / 2))
		self.text = global_vars.font.render(text, True, global_vars.BLACK)
		self.text_position = self.text.get_rect(center=(size[0] / 2, size[1] / 1.4))
		self.size = size
		self.is_alive = True
		self.buttons = list()
		self.pushed_button = None
		buttons_amount = len(buttons_text)
		for i in range(buttons_amount):
			b_pos = (size[0] // (buttons_amount + 1) + global_vars.BUTTON_SIZE[0] * i, size[1] - global_vars.RATIO * 6)
			self.buttons.append(Button('assets/mbutton', global_vars.BUTTON_SIZE, b_pos, buttons_text[i]))
		if picture is not None:
			self.image = utils.get_adopted_image(picture, (int(size[0] / 2), int(size[1] / 2)))
			self.image_position = self.image.get_rect(center=(size[0] / 2, size[1] / 3))
		else:
			self.image = None

	def __del__(self):
		os.remove('assets/screenshot.png')
		print('button is dead')

	def draw(self, mouse_position, lmb_is_pressed):
		global_vars.window.blit(self.screenshot, global_vars.ZERO_POINT)
		global_vars.window.blit(self.surface, self.surface_position)
		self.surface.blit(self.color_surface, self.color_surface_position)
		self.color_surface.fill(global_vars.INFO_COLOR)
		self.color_surface.blit(self.text, self.text_position)
		if self.image is not None:
			self.color_surface.blit(self.image, self.image_position)
		for button in self.buttons:
			cursor_is_on_button = button.states_images.get('hover')[1].collidepoint(
				mouse_position[0] - self.surface_position.topleft[0],
				mouse_position[1] - self.surface_position.topleft[1])
			if cursor_is_on_button and not lmb_is_pressed:
				self.color_surface.blit(*button.states_images.get('hover'))
			elif cursor_is_on_button and lmb_is_pressed:
				self.color_surface.blit(*button.states_images.get('pushed'))
			else:
				self.color_surface.blit(*button.states_images.get('normal'))

	def modal_window_process(self):
		clock = pygame.time.Clock()
		while self.is_alive:
			pygame.event.get()
			mouse_position = pygame.mouse.get_pos()
			mouse_buttons = pygame.mouse.get_pressed(3)
			global_vars.window.fill(global_vars.BLACK)
			self.draw(mouse_position, mouse_buttons[0])
			pygame.display.update()
			clock.tick(30)
			for i in range(len(self.buttons)):
				cursor_is_on_button = self.buttons[i].states_images.get('hover')[1].collidepoint(
					mouse_position[0] - self.surface_position.topleft[0],
					mouse_position[1] - self.surface_position.topleft[1])
				if cursor_is_on_button and mouse_buttons[0]:
					self.pushed_button = i
					self.is_alive = False
		return self.pushed_button



