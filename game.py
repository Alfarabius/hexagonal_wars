
import pygame

import combat
import global_vars
import interface
import player


class Game:
	__instance = None

	def __new__(cls, *args, **kwargs):
		if not isinstance(cls.__instance, cls):
			cls.__instance = super(Game, cls).__new__(cls)
		else:
			print('Game already exist')
		return cls.__instance

	def __init__(self, game_map, army_file, sequence, turns=9, curr_player=1):
		self.interface = interface.Interface()
		self.game_map = game_map
		self.combat_table = combat.CombatTable(global_vars.COMBAT_TABLE_FILE)
		self.players = [player.Player(army_file[0]), player.Player(army_file[1])]
		self.current_player = self.players[curr_player]
		self.current_cursor = global_vars.CURSOR_SELECT
		self.scenario_queue = 0
		self.current_hex = None
		self.selected_unit = None
		self.opposite_player = self.players[(curr_player - 1) * -1]
		self.clock = pygame.time.Clock()
		self.timer = pygame.time.get_ticks()
		self.turns = turns
		self.sequence = sequence
		self.turn = 1
		self._mouse_pos = (0, 0)
		self.is_running = True
		self.lmb_is_pressed = False
		self.rmb_is_pressed = False

	def game_loop(self):
		global_vars.starting_screen()
		self.timer = pygame.time.get_ticks()
		while self.is_running:
			# print(self.clock.get_fps())  # Debug
			self.screen_update()
			self.play_turn()

	def quit_procedure(self):
		self.is_running = False
		pygame.quit()

	def interface_handler(self):
		if self.interface.end_turn_button.is_pushed():
			self.end_turn()
		elif self.interface.next_phase_button.is_pushed():
			pass

	def cursor_handler(self):
		self.current_cursor = global_vars.CURSOR_SELECT
		if self.selected_unit is not None:
			self.current_cursor = global_vars.CURSOR_MOVE
			if self.is_players_unit_in_hex(self.current_hex, self.opposite_player):
				self.current_cursor = global_vars.CURSOR_ATTACK
			if self.is_players_unit_in_hex(self.current_hex, self.current_player):
				self.current_cursor = global_vars.CURSOR_SELECT
		pygame.mouse.set_cursor(self.current_cursor)

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

		for event in pygame.fastevent.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				self.quit_procedure()

	def mouse_handler(self):
		self._mouse_pos = pygame.mouse.get_pos()
		self.current_hex = self.mouse_position_reaction()
		self.cursor_handler()
		self.scroll_check()
		self.mouse_buttons_handler()

	def mouse_buttons_handler(self):
		mouse_pressed = pygame.mouse.get_pressed(3)
		if mouse_pressed[0]:
			self.lmb_is_pressed = True
		elif self.lmb_is_pressed:
			self.lmb_reaction(self.current_hex)
			self.interface_handler()
			self.lmb_is_pressed = False
		if mouse_pressed[2]:
			self.rmb_is_pressed = True
		elif self.rmb_is_pressed:
			self.rmb_reaction(self.current_hex)
			self.rmb_is_pressed = False

	def redraw_screen(self):
		self.game_map.screen.draw()
		self.game_map.draw_map()
		self.interface.draw(self._mouse_pos, self.lmb_is_pressed)
		self.units_stack_draw()
		self.units_draw()

	def play_turn(self):
		self.key_handler()
		self.mouse_handler()
		self.modal_windows_handler()

	def end_turn(self):
		#   end turn procedure
		for unit in self.current_player.army:
			unit.restore_movement_points()
		self.turn += 1
		current_player_index = self.players.index(self.current_player)
		self.current_player = self.players[current_player_index - 1]
		self.opposite_player = self.players[current_player_index]

	def screen_update(self):
		self.redraw_screen()
		pygame.display.update()
		self.clock.tick(global_vars.FPS)

	@staticmethod
	def is_players_unit_in_hex(current_hex, this_player):
		for unit in this_player.army:
			if unit.occupied_hex == current_hex:
				return True

	@staticmethod
	def get_players_units_in_hex(current_hex, this_player):
		units = list()
		for unit in this_player.army:
			if unit.occupied_hex == current_hex:
				units.append(unit)
		return units

	def combat(self, hexagon):
		combat.Combat(
			self.current_player,
			self.get_players_units_in_hex(hexagon, self.opposite_player),
			self.combat_table,
			hexagon
		).resolve_combat()
		for player_ in self.players:
			player_.check_losses()
		self.selected_unit.unselect()
		self.selected_unit = None

	def mouse_position_reaction(self):
		current_hex = None
		for that_hex in self.game_map.hexes:
			if that_hex.is_point_inside_hexagon(self._mouse_pos[0], self._mouse_pos[1]):
				that_hex.fill_hex(global_vars.SELECT_COLOR, global_vars.SELECT_SIZE)
				that_hex.info_box.write_info(self.interface.main_surface)
				current_hex = that_hex
			else:
				that_hex.clear_hex()
		return current_hex

	def rmb_reaction(self, current_hex):
		if not current_hex:
			return
		current_hex.select()
		global_vars.game_map.unselect_other_hexes(current_hex)
		for unit in self.current_player.army:
			if not unit.is_selected and unit.occupied_hex == current_hex:
				if self.selected_unit is not None:
					self.selected_unit.unselect()
					self.selected_unit = None
				unit.select()
				self.current_player.replace_unit_to_top(unit)
				self.selected_unit = unit
				break

	def lmb_reaction(self, current_hex):
		if current_hex and self.selected_unit is not None:
			if not self.is_players_unit_in_hex(current_hex, self.opposite_player):
				self.selected_unit.move(current_hex)
			elif self.selected_unit.occupied_hex.is_adjacent(current_hex):
				self.combat(current_hex)

	def scroll_check(self):
		if global_vars.game_map.scroll(self._mouse_pos):
			self.current_cursor = global_vars.CURSOR_SCROLL
			pygame.mouse.set_cursor(self.current_cursor)

	def modal_windows_handler(self):
		if self.turn == 1 and self.scenario_queue == 0 and self.timer + 600 < pygame.time.get_ticks():
			interface.ModalWindow(
				['Understand', 'Ok', 'Yeah', 'Cool'],
				'Test modal window',
				global_vars.MODAL_SIZE,
				'assets/screen0'
			).modal_window_process()
			self.scenario_queue += 1

	def units_stack_draw(self):
		y_offset, x_offset, n = 0, 0, 0
		for unit in self.current_player.army:
			if self.selected_unit is not None and self.selected_unit.occupied_hex == unit.occupied_hex:
				n += 1
				unit.write_unit_info(self.interface.units_surface, x_offset, y_offset)
				x_offset += int(global_vars.UNIT_WIDTH * 1.1)
				y_offset += int(global_vars.UNIT_HEIGHT * 1.3) if n % 4 == 0 else 0
				x_offset = 0 if n % 4 == 0 else x_offset

	def units_draw(self):
		for _player in self.players:
			for unit in _player.army:
				unit.appear(unit.occupied_hex.get_units_offset_value())
				unit.occupied_hex.decrease_offset()
		for hexagon in self.game_map.hexes:
			hexagon.restore_offset()
