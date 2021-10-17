import sys

import pygame

import combat_table
import constants
import sounds
import utils
from choice_state import Choice
from constants import Fonts, Colors
from game_clock import GameClock
from game_map import Map
from game_script import GameScript
from player import Player
from button import Button
from global_sizes import Sizes
from interface import Interface
from typing import Protocol
from maneuver_state import Maneuver


class GameObject(Protocol):

	def update(self): ...

	def draw(self, surface: pygame.Surface): ...


class Game:
	__instance = None

	def __new__(cls, *args, **kwargs):
		if not isinstance(cls.__instance, cls):
			cls.__instance = super(Game, cls).__new__(cls)
		else:
			print('Game already exist')
		return cls.__instance

	def __init__(self, window):
		# states
		self.is_running = False

		# lis of GameObjects
		self.objects: list[GameObject] = []

		# objects
		self.window = window
		self.clock = GameClock()
		self.add_object(self.window)
		self.add_object(self.clock)

		# container (hud)
		self.game_info = None

	def __del__(self):
		pass

	def start(self):
		self.is_running = True
		while self.is_running:
			self._game_loop()

	def _game_loop(self):
		self.update()
		self.draw()

	def update(self):
		for game_object in self.objects:
			game_object.update()

	def draw(self):
		for game_object in self.objects:
			game_object.draw(self.window.surface)

	def add_object(self, game_object: GameObject):
		self.objects.append(game_object)

	def remove_object(self, game_object: GameObject):
		self.objects.remove(game_object)

	def quit(self):
		self.is_running = False
		pygame.quit()
		sys.exit()


class HexagonalWarGame(Game):
	def __init__(self, path, window):
		self.turn = 0
		self.players: list[Player] = []
		self.path = path

		super().__init__(window)
		self._parse_game(path)

		self.state = Maneuver(self)

		self.add_object(ContainersHandler(self))
		self.add_object(PygameEventHandler(self.pause, self.window))
		self.add_object(self.map)
		self.add_object(self.state)
		self.add_object(self.interface)
		for player in self.players:
			self.add_object(player)

		self.current_player = self.players[0]

		self.add_object(GameScript(self))

	def _parse_game(self, path):
		config = utils.json_to_dict(path)
		self.map = Map(config.get('map', ''), self.clock)
		for hexagon in self.map.hexes:
			hexagon.get_adjacent_hexagons(self.map)
		for i in range(config.get('players')):
			self.players.append(Player(config.get('player_' + str(i + 1), ''), self.map, self.clock))
		self.name = config.get('name', 'corrupted_name')
		self.wining_conditions = config.get('wining_conditions', '')
		self.combat_table = combat_table.CombatTable(config.get('combat_table', ''))
		self.interface = Interface(
			config.get('interface_image', ''),
			[Button(
				'End Turn',
				(int(14 * Sizes.RATIO), int(5 * Sizes.RATIO)),
				(Sizes.RATIO * 13.1, Sizes.HEIGHT_RATIO * 85),
				(140, 30, 30),
				pygame.K_e,
				self.end_turn
			)],
			self.window.size
		)

	def end_turn(self):
		if self.state.__class__.__name__ == 'Combat' or self.state.__class__.__name__ == 'Choice':
			sounds.SOUNDS.wrong.play()
			return
		self._wining_condition_checker()
		for player in self.players:
			player.restore()
		self.turn += 1
		self.current_player = self.get_opposite_player()
		self.state.unselect_unit()

	def pause(self):
		if self.state.__class__.__name__ == 'Choice':
			return
		pause_menu = Choice(
			self,
			None,
			'Pause',
			{
				'Resume': [self.change_state, [self.state]],
				'Settings': [utils.plug, None],
				'Save Game': [utils.plug, None],
				'Load Game': [utils.plug, None],
				'Exit': [self.quit, None]
			}
		)
		self.change_state(pause_menu)

	def change_state(self, state):
		self.remove_object(self.state)
		self.state = state
		self.add_object(state)

	def get_opposite_player(self) -> Player:
		return self.players[self.players.index(self.current_player) - 1]

	def _wining_condition_checker(self):
		if self.wining_conditions == 'deathmatch':
			for player in self.players:
				if not player.army.sprites():
					ind = self.players.index(player)
					self.change_state(Choice(
						self,
						None,
						f'Player {abs(ind - 1) + 1}\nwin!',
						{
							'Exit': [self.quit, None],
							'Restart': [self.restart_game, None],
							'Load Game': [utils.plug, None],
						}
					))

	def create_container(self) -> list:
		info = []
		font = Fonts.PIXEL_3
		color = Colors.FILL
		info.append(Fonts.PIXEL_3_TITLE.render(self.name, False, Colors.SELECT))
		info.append(font.render(''.join('Turn   ' + str(self.turn)), False, color))
		info.append(font.render(''.join('Type   ' + str(self.wining_conditions)), False, color))
		info.append(font.render(''.join('State   ' + str(self.state.__class__.__name__)), False, color))
		return info

	def restart_game(self):
		game_window = self.window
		path = self.path
		new_game = HexagonalWarGame(path, game_window)
		new_game.turn = 1
		new_game.start()


class PygameEventHandler:
	def __init__(self, function, window):
		self.function = function
		self.window = window

	def update(self):
		for event in pygame.fastevent.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				self.function()
			if event.type == pygame.VIDEORESIZE:
				self.window.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
				self.window.fullscreen = not self.window.fullscreen
				if self.window.fullscreen:
					self.window.surface = pygame.display.set_mode((self.window.width, self.window.height), pygame.FULLSCREEN)
				else:
					self.window.surface = pygame.display.set_mode((self.window.__class__.W, self.window.__class__.H), pygame.RESIZABLE)

	def draw(self, surface):
		pass


class ContainersHandler:
	def __init__(self, game: HexagonalWarGame):
		self.hud = game.interface.hud
		self.unit_info = None
		self.hexagon_info = None
		self.game = game

	def update(self):
		self.game.game_info = self.game.create_container()
		self.unit_info = self.game.state.selected_unit.info if self.game.state.selected_unit else None
		self.hexagon_info = self.game.state.current_hex.info if self.game.state.current_hex else None
		container = {}
		top_content = self.unit_info if self.unit_info else self.game.game_info
		mid_content = self.hexagon_info if self.hexagon_info else constants.HOTKEYS
		container.update({'top': top_content})
		container.update({'mid': mid_content})
		self.hud.set_container(container)

	def draw(self, surface):
		pass
