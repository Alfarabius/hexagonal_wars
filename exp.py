import os

PATH = 'assets/tank_red/'
animations = {}
try:
	keys = os.listdir(PATH)
except FileNotFoundError:
	print('assets/ directory are corrupted or does not exist')
	raise SystemExit()
for key in keys:
	new = {key: os.listdir(PATH + key)}
	print(new)
	animations.update(new)
print(animations)
content = []
print(bool(content))
print(any(content))
content.append('ss')
print(bool(content))
print(any(content))
print('i`m here')
