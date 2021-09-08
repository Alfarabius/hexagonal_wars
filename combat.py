import json

import global_vars
import interface
import utils


class CombatTable:
	def __init__(self, path):
		file = open(path, 'r')
		json_string = ''.join(file)
		self.content = dict(json.loads(json_string))

	def return_result(self, ratio, die_roll):
		if ratio < 3 or 3 < ratio < 5:
			ratio = 3
		elif 5 < ratio < 10:
			ratio = 5
		elif ratio > 60:
			ratio = 60
		elif ratio > 10:
			ratio = (ratio // 10) * 10
			print(ratio)
		column = self.content.get(str(ratio))
		return column.get(str(die_roll))


class Combat:
	def __init__(self, attacking_player, defending_units, combat_table, target_hex):
		self.target_hexagon = target_hex
		self.attacking_player = attacking_player
		self.attacking_units = list()
		self.attacking_units.extend(self.selecting_attacking_units())
		self.attacking_units_power = self.calculate_units_power(self.attacking_units)
		self.defending_units = defending_units
		self.defending_units_power = self.calculate_units_power(self.defending_units)
		self.combat_table = combat_table
		self.ratio = self.calculate_powers_ratio()

	def __del__(self):
		print(self.__dict__)
		print('combat is done')

	def selecting_attacking_units(self):
		units_possible_to_attack = []
		for unit in self.attacking_player.army:
			if unit.occupied_hex.is_adjacent(self.target_hexagon) and unit.is_possible_to_move(self.target_hexagon):
				units_possible_to_attack.append(unit)
		modal = interface.ObjectChoiceWindow(
			['Attack!'],
			'Choose units for attack',
			global_vars.ATTACK_WINDOW_SIZE,
			units_possible_to_attack
		)
		return modal.modal_window_process()

	def calculate_powers_ratio(self):
		ratio = int((self.attacking_units_power / self.defending_units_power) * 10)
		return ratio

	def resolve_combat(self):
		def_length = len(self.defending_units)
		att_length = len(self.attacking_units)
		combat_result = self.combat_table.return_result(self.ratio, int(utils.roll_2d6() / 2))
		if combat_result == 'AE':
			self._combat_result_resolve(self.attacking_units, False)
		if combat_result == 'Ax':
			self._combat_result_resolve(self.attacking_units, True, def_length)
		if combat_result == 'Ex':
			if self.attacking_units_power > self.defending_units_power:
				self._combat_result_resolve(self.defending_units, False)
				self._combat_result_resolve(self.attacking_units, True, def_length)
			else:
				self._combat_result_resolve(self.attacking_units, False)
				self._combat_result_resolve(self.defending_units, True, att_length)
		if combat_result == 'DE':
			self._combat_result_resolve(self.defending_units, False)

	@staticmethod
	def _combat_result_resolve(units, is_reduce, length=None):
		count = 0
		for unit in units:
			if is_reduce:
				unit.reduce()
			else:
				unit.eliminate()
			if length is not None:
				count += 1
				if count >= length:
					break

	@staticmethod
	def calculate_units_power(units):
		return sum((unit.power for unit in units))
