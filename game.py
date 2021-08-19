import pygame

import global_vars
import interface
import map
import player


class Game:
	def __init__(self, game_map_file, players, sequence, turns=9):
		pygame.display.set_caption(global_vars.NAME)
		self._screen_flags = pygame.FULLSCREEN
		self.window = pygame.display.set_mode(global_vars.SCREEN, self._screen_flags)
		self.interface = interface.Interface()
		self.game_map = map.Map(game_map_file)
		self.players = [player.Player(players[0]), player.Player(players[1])]
		self.clock = pygame.time.Clock()
		self.turns = turns
		self.sequence = sequence
		self.turn = 0
		self._mouse_pos = (0, 0)
		self.is_running = True

	def game_loop(self):
		while self.is_running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					self.quit_procedure()
			for unit in (self.players[x].army for x in range(2)):
				if unit.is_selected:
					unit.write_unit_info()
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
		mouse_pressed = pygame.mouse.get_pressed(5)
		if new_mouse_pos != self._mouse_pos:
			self._mouse_pos = tuple(new_mouse_pos)
		for that_hex in self.game_map.hexes:
			if that_hex.is_point_inside_hexagon(self._mouse_pos[0], self._mouse_pos[1]):
				that_hex.fill_hex(global_vars.SELECT_COLOR, global_vars.SELECT_SIZE)
				that_hex.info_box.write_info()
				current_hex = that_hex
			else:
				that_hex.clear_hex()
		if current_hex and mouse_pressed[0]:
			current_hex.select()
			global_vars.game_map.unselect_other_hexes(current_hex)
			for unit in (self.players[x].army for x in range(2)):
				if unit.occupied_hex == current_hex:
					unit.select()
				elif unit.is_selected:
					unit.move(current_hex)
					unit.unselect()
		global_vars.game_map.scroll(self._mouse_pos)

	def redraw_screen(self):
		self.game_map.screen.draw()
		self.game_map.draw_map()
		for unit in (self.players[x].army for x in range(2)):
			unit.appear()

	def play_turn(self):
		self.key_handler()
		self.mouse_handler()
		self.redraw_screen()

	def end_turn(self):
		#   end turn procedure
		for unit in (self.players[x].army for x in range(2)):
			unit.restore_movement_points()
		self.turn += 1
