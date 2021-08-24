import pygame

import global_vars
import interface
import player


class Game:
	def __init__(self, game_map, army_file, sequence, turns=9):
		self.interface = interface.Interface()
		self.game_map = game_map
		self.players = [player.Player(army_file[0]), player.Player(army_file[1])]
		self.current_player = self.players[1]
		self.clock = pygame.time.Clock()
		self.turns = turns
		self.sequence = sequence
		self.turn = 0
		self._mouse_pos = (0, 0)
		self.is_running = True
		self.lmb_is_pressed = False
		self.selected_unit = None

	def game_loop(self):
		while self.is_running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					self.quit_procedure()
			for unit in self.current_player.army:
				if unit.is_selected:
					unit.write_unit_info(self.interface.units_surface)
			self.play_turn()
			pygame.display.update()
			self.clock.tick(global_vars.FPS)

	def quit_procedure(self):
		self.is_running = False
		pygame.quit()

	def key_handler(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.game_map.scroll_direct((1, 0))
		elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.game_map.scroll_direct((-1, 0))
		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			self.game_map.scroll_direct((0, -1))
		elif keys[pygame.K_UP] or keys[pygame.K_w]:
			self.game_map.scroll_direct((0, 1))

	def mouse_handler(self):
		current_hex = None
		new_mouse_pos = pygame.mouse.get_pos()
		mouse_pressed = pygame.mouse.get_pressed(3)
		if new_mouse_pos != self._mouse_pos:
			self._mouse_pos = tuple(new_mouse_pos)
		for that_hex in self.game_map.hexes:
			if that_hex.is_point_inside_hexagon(self._mouse_pos[0], self._mouse_pos[1]):
				that_hex.fill_hex(global_vars.SELECT_COLOR, global_vars.SELECT_SIZE)
				that_hex.info_box.write_info(self.interface.main_surface)
				current_hex = that_hex
			else:
				that_hex.clear_hex()
		if current_hex and mouse_pressed[2]:
			current_hex.select()
			global_vars.game_map.unselect_other_hexes(current_hex)
			for unit in self.current_player.army:
				if not unit.is_selected and unit.occupied_hex == current_hex:
					if self.selected_unit is not None:
						self.selected_unit.unselect()
						self.selected_unit = None
					unit.select()
					i = self.current_player.army.index(unit)    # experiment
					x = self.current_player.army.pop(i)         # experiment
					self.current_player.army.insert(0, x)       # experiment
					self.selected_unit = unit
					break
		if mouse_pressed[0] and current_hex and self.selected_unit is not None:
			self.selected_unit.move(current_hex)
		if mouse_pressed[0]:
			self.lmb_is_pressed = True
		else:
			self.lmb_is_pressed = False
		global_vars.game_map.scroll(self._mouse_pos)

	def redraw_screen(self):
		self.game_map.screen.draw()
		self.game_map.draw_map()
		self.interface.draw(self._mouse_pos, self.lmb_is_pressed)
		for _player in self.players:
			for unit in _player.army:
				unit.appear()

	def play_turn(self):
		self.key_handler()
		self.mouse_handler()
		self.redraw_screen()

	def end_turn(self):
		#   end turn procedure
		for unit in self.current_player.army:
			unit.restore_movement_points()
		self.turn += 1
