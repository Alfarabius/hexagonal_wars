import pygame.key

import maneuver_state
import sounds
import utils
from global_sizes import Sizes
from state import State


class Combat(State):
	def __init__(self, game, selected_unit, target):

		self.pointer = utils.get_adopted_image('assets/pointer', (int(Sizes.RATIO), int(Sizes.RATIO)))
		self.mouse = game.interface.mouse

		self.selected_unit = selected_unit
		self.attackers = set()
		self.attackers.add(selected_unit)
		self.supporters_are_selected = False

		self.target = target
		super().__init__(game)
		self.possible_attackers_amount = self._count_possible_attackers()

	def update(self):
		self.current_hex = self._get_current_hex()
		self._select_supporters()
		if not self.supporters_are_selected:
			return 
		self._combat_resolve()
		self._change_to_maneuver_state()

	def draw(self, surface):
		for attacker in self.attackers:
			position = (
				attacker.occupied_hexagon.position[0] + Sizes.RATIO * 25,
				attacker.occupied_hexagon.position[1] - Sizes.RATIO * 2.2
			)
			surface.blit(self.pointer, position)

	def _combat_resolve(self):
		attacker_fp = 0
		for unit in self.attackers:
			attacker_fp += unit.attack(self.target.occupied_hexagon)
		defender_fp = self.target.attack(self.selected_unit.occupied_hexagon)
		self.target.restore()
		die_roll = utils.roll_d6()
		result = self.game.combat_table.get_result(attacker_fp - defender_fp, die_roll)

		target = [self.selected_unit]
		if result[0] == 'D':
			target = [self.target]
		elif result[0] == 'B':
			target = [self.selected_unit, self.target]

		if result[1] == 'D':
			for unit in target:
				unit.destroy()
				self.__unselect(unit)
		elif result[1] == 'R':
			unit = self.target
			opposite_unit = self.selected_unit
			if self.selected_unit in target:
				unit = self.selected_unit
				opposite_unit = self.target
			retreat_hexagons = unit.occupied_hexagon.adjacent_hexes
			for hexagon in retreat_hexagons:
				if hexagon not in opposite_unit.occupied_hexagon.adjacent_hexes \
					and self._retreat_is_possible(hexagon, unit):
					unit.retreat(hexagon)
					break
			else:
				self.__unselect(unit)

	def _change_to_maneuver_state(self):
		state = maneuver_state.Maneuver(self.game, self.selected_unit)
		self.game.state = state
		self.game.add_object(state)
		self.game.remove_object(self)

	@staticmethod
	def _retreat_is_possible(hexagon, unit):
		return unit \
			and hexagon \
			and unit.occupied_hexagon.is_adjacent(hexagon) \
			and hexagon.container.unit is None \
			and hexagon.container.is_passable() \
			and unit.movement > 0

	def __unselect(self, unit):
		if unit == self.selected_unit:
			self.selected_unit = None

	def _select_supporters(self):
		if pygame.key.get_pressed()[pygame.K_SPACE] or self.possible_attackers_amount == 1:
			self.supporters_are_selected = True
		self.cursor = utils.ignore_exception(self.mouse.set_cursor)(['MOVE'])
		for unit in self.game.current_player.army:
			if unit.occupied_hexagon.is_adjacent(self.target.occupied_hexagon) \
				and unit.attacks > 0 \
				and unit.is_unit_inside_hexagon(self.current_hex):
				self.cursor = utils.ignore_exception(self.mouse.set_cursor)(['SELECT'])
				self.mouse.lmb_reaction(self.add_attacker, unit)
				self.mouse.rmb_reaction(self.remove_attacker, unit)

	def _get_current_hex(self):
		for hexagon in self.game.map.hexes:
			if hexagon.is_point_inside_hexagon(*self.mouse.position, Sizes.MAP_OFFSET):
				return hexagon

	def unselect_unit(self):
		pass

	def add_attacker(self, unit):
		if unit == self.selected_unit:
			return
		sounds.SOUNDS.select.play()
		self.attackers.add(unit)

	def remove_attacker(self, unit):
		if unit == self.selected_unit:
			return
		sounds.SOUNDS.select.play()
		self.attackers.remove(unit)

	def _count_possible_attackers(self) -> int:
		count = 0
		for unit in self.game.current_player.army:
			if unit.occupied_hexagon.is_adjacent(self.target.occupied_hexagon) \
				and unit.attacks > 0:
				count += 1
		return count
