import pygame

import global_vars
import utils


class Interface:
	def __init__(self):
		self.end_turn_button = self.make_button('assets/button', (
			int(14 * global_vars.RATIO), int(5 * global_vars.RATIO)),
			(global_vars.RATIO * 10.1, global_vars.RATIO * 2.4))
		self.next_phase_button = self.make_button('assets/button1', (
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
		cursor_is_on_end_turn_button = self.end_turn_button.get('normal')[1].collidepoint(
				mouse_position[0] - self.control_surface_position.topleft[0],
				mouse_position[1] - self.control_surface_position.topleft[1])
		cursor_is_on_next_phase_button = self.next_phase_button.get('normal')[1].collidepoint(
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
			self.control_surface.blit(*button.get('hover'))
		elif cursor_is_on_button and lmb_is_pressed:
			self.control_surface.blit(*button.get('pushed'))
			global_vars.BUTTON_SOUND.play()
			pygame.time.wait(250)
		else:
			self.control_surface.blit(*button.get('normal'))

	@staticmethod
	def make_button(path, size, position):
		button_normal = utils.get_adopted_image(path + '_normal', size)
		button_hover = utils.get_adopted_image(path + '_hover', size)
		button_pushed = utils.get_adopted_image(path + '_pushed', (
			size[0] - int(global_vars.RATIO*2), size[1] - int(global_vars.RATIO*2)))
		button = {
			'normal': (button_normal, button_normal.get_rect(center=position)),
			'hover': (button_hover, button_hover.get_rect(center=position)),
			'pushed': (button_pushed, button_pushed.get_rect(center=position))
		}
		return button
