import combat_state
import sounds
import utils
from constants import Colors
from global_sizes import Sizes
from hexagon import Hexagon
from interface import MouseInput
from on_map_object import Unit
from typing import Optional
from state import State


class Maneuver(State):
	def __init__(self, game, selected_unit=None):
		super().__init__(game)
		self.mouse: MouseInput() = self.game.interface.mouse
		self.cursor = self.mouse.set_cursor('SELECT')
		self.cursor_name = 'SELECT'
		self.selected_unit: Optional[Unit] = selected_unit
		self.current_hex: Optional[Hexagon] = None
		self.current_hex_line: Optional[list[Hexagon, ...]] = None
		self.movement_ques: list[MovementQue, ...] = []

	def update(self):
		self.current_hex = self._get_current_hex()
		self.unit_select_handler()
		self.current_hex_line_handler()
		self._state_change_checker()
		self.cursor_handler()
		self.movement_handler()

		for que in self.movement_ques:
			que.update()

	def draw(self, surface):
		if not self.current_hex_line or not self.current_hex:
			return
		for hexagon in self.current_hex_line:
			if hexagon is not None and hexagon.container.unit is None:
				hexagon.draw_midpoint(self.game.map.surface,  Sizes.RATIO // 3, Colors.INFO)
		if self.current_hex is not None and self.current_hex.container.unit is None:
			self.current_hex.draw_midpoint(self.game.map.surface, Sizes.RATIO // 2, Colors.WHITE)

	def _get_current_hex(self):
		for hexagon in self.game.map.hexes:
			if hexagon.is_point_inside_hexagon(*self.mouse.position, Sizes.MAP_OFFSET):
				return hexagon

	def _select_unit(self, unit):
		sounds.SOUNDS.select.play()
		self.selected_unit = unit

	def unit_select_handler(self):
		for unit in self.game.current_player.army:
			if unit.is_unit_inside_hexagon(self.current_hex):
				self.mouse.lmb_reaction(self._select_unit, unit)

	def cursor_handler(self):
		if self.current_hex is not None:
			if self._attack_is_possible() and self.cursor_name != 'ATTACK':
				self.cursor = utils.ignore_exception(self.mouse.set_cursor)(['ATTACK'])
				self.cursor_name = 'ATTACK'
			elif self.selected_unit is not None \
				and self.current_hex.container.unit is None \
				and self.cursor_name != 'MOVE':
				self.cursor = utils.ignore_exception(self.mouse.set_cursor)(['MOVE'])
				self.cursor_name = 'MOVE'
			elif self.cursor_name != 'SELECT' \
				and not self._attack_is_possible() \
				and self.current_hex.container.unit is not None \
				or self.selected_unit is None:
				self.cursor = utils.ignore_exception(self.mouse.set_cursor)(['SELECT'])
				self.cursor_name = 'SELECT'

	def movement_handler(self):
		if self._movement_is_possible():
			self.mouse.lmb_reaction(self._movement_que_maker, None)
			return
		else:
			self.mouse.rmb_reaction(self.unselect_unit, None)

	def _state_change_checker(self):
		if self._attack_is_possible():
			self.mouse.lmb_reaction(
				self.change_state,
				combat_state.Combat(self.game, self.selected_unit, self.current_hex.container.unit)
			)

	def unselect_unit(self):
		sounds.SOUNDS.select.play()
		self.selected_unit = None

	def _attack_is_possible(self):
		enemy_unit = self.current_hex.container.unit if self.current_hex else None
		return self.selected_unit is not None \
			and self.selected_unit.attacks > 0 \
			and self.current_hex \
			and self.selected_unit.occupied_hexagon.is_adjacent(self.current_hex) \
			and enemy_unit is not None \
			and enemy_unit not in self.game.current_player.army

	def _movement_is_possible(self):
		if not self.selected_unit or not self.current_hex_line:
			return False
		hex_line = []
		for hexagon in self.current_hex_line:
			if hexagon is None:
				continue
			hex_line.append(
				hexagon.container.unit is None
				and hexagon.container.is_passable()
				and self.selected_unit.movement >= len(self.current_hex_line)
			)
		return all(hex_line)

	def current_hex_line_handler(self):
		if not self.selected_unit or not self.current_hex:
			self.current_hex_line = None
			return
		self.current_hex_line = list(self.game.map.hexagons_line(self.selected_unit.occupied_hexagon, self.current_hex))
		self.current_hex_line.append(self.current_hex)
		self.current_hex_line.remove(self.selected_unit.occupied_hexagon)

	def _movement_que_maker(self):
		self.movement_ques.append(MovementQue(self.selected_unit, self.current_hex_line, self))

	def kill_que(self, que):
		self.movement_ques.remove(que)


class MovementQue:
	def __init__(self, unit, hexagons: list, state):
		self.unit = unit
		self.hexagons = tuple(hexagons)
		self.index = 0
		self.state = state
		self.state.game.map.lock_scroll()
		self.unit.move(self.hexagons[self.index])

	def update(self):
		rounded_position = (
			int(self.hexagons[self.index].position[0]),
			int(self.hexagons[self.index].position[1])
		)

		if self.hexagons[self.index] == self.hexagons[-1] \
			and self.unit.rect.center == rounded_position:
			self.state.game.map.unlock_scroll()
			self.state.kill_que(self)
			return

		if self.unit.rect.center == rounded_position:
			self.index += 1
			self.unit.move(self.hexagons[self.index])
