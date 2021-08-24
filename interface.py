import pygame

import global_vars
import utils


class Button:
	def __init__(self, path, size, position):
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
		self.end_turn_button = Button('assets/button', (
			int(14 * global_vars.RATIO), int(5 * global_vars.RATIO)),
			(global_vars.RATIO * 10.1, global_vars.RATIO * 2.4))
		self.next_phase_button = Button('assets/button1', (
			int(14 * global_vars.RATIO), int(5 * global_vars.RATIO)),
			(global_vars.RATIO * 10.1, global_vars.RATIO * 6.6))
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

