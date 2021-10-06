import json


class CombatTable:
	def __init__(self, path):
		file = open(path, 'r')
		json_string = ''.join(file)
		self.content = dict(json.loads(json_string))

	def get_result(self, diff, die_roll):
		if diff < -7:
			return 'AD'
		elif diff > 7:
			return 'DD'
		column = self.content.get(str(diff))
		return column.get(str(die_roll))
