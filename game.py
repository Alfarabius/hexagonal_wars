import sys

import pygame

import combat_table
import sounds
import utils
from game_map import Map
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
		self.is_running = False

		self.objects: list[GameObject] = []

		self.window = window
		self.add_object(self.window)

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

		super().__init__(window)
		self._parse_game(path)

		self.state = Maneuver(self)

		self.add_object(ContainersHandler(self))
		self.add_object(PygameEventHandler(self.quit))
		self.add_object(self.map)
		self.add_object(self.interface)
		self.add_object(self.state)
		for player in self.players:
			self.add_object(player)

		self.current_player = self.players[0]

	def _parse_game(self, path):
		config = utils.json_to_dict(path)
		self.map = Map(config.get('map', ''))
		for hexagon in self.map.hexes:
			hexagon.get_adjacent_hexagons(self.map)
		for i in range(config.get('players')):
			self.players.append(Player(config.get('player_' + str(i + 1), ''), self.map))
		self.name = config.get('name', 'corrupted_name')
		self.wining_conditions = config.get('wining_conditions', '')
		self.combat_table = combat_table.CombatTable(config.get('combat_table', ''))
		self.interface = Interface(
			config.get('interface_image', ''),
			[Button(
				'End Turn',
				(int(14 * Sizes.RATIO), int(5 * Sizes.RATIO)),
				(Sizes.RATIO * 13.1, Sizes.HEIGHT_RATIO * 85),
				(200, 100, 100),
				pygame.K_e,
				self.end_turn
			)],
			self.window.size
		)

	def end_turn(self):
		if self.state.__class__.__name__ == 'Combat':
			sounds.SOUNDS.wrong.play()
			return
		self._wining_condition_checker()
		for player in self.players:
			player.restore()
		self.turn += 1
		self.current_player = self.get_opposite_player()
		self.state.unselect_unit()

	def get_opposite_player(self) -> Player:
		return self.players[self.players.index(self.current_player) - 1]

	def _wining_condition_checker(self):
		if self.wining_conditions == 'deathmatch':
			for player in self.players:
				if not player.army.sprites():
					self.quit()


class PygameEventHandler:
	def __init__(self, quit_function):
		self.quit_function = quit_function

	def update(self):
		for event in pygame.fastevent.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				self.quit_function()

	def draw(self, surface):
		pass


class ContainersHandler:
	def __init__(self, game: HexagonalWarGame):
		self.hud = game.interface.hud
		self.unit_info = None
		self.hexagon_info = None
		self.game = game

	def update(self):
		self.unit_info = self.game.state.selected_unit.info if self.game.state.selected_unit else None
		self.hexagon_info = self.game.state.current_hex.info if self.game.state.current_hex else None
		container = {}
		container.update({'top': self.unit_info})
		container.update({'mid': self.hexagon_info})
		self.hud.set_container(container)

	def draw(self, surface):
		pass
