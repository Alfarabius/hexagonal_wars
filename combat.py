import json


class CombatTable:
	def __init__(self, path):
		file = open(path, 'r')
		json_string = ''.join(file)
		self.content = dict(json.loads(json_string))

	def return_result(self, ratio, die_roll):
		return self.content.get(str(ratio)).get(str(die_roll))
