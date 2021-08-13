import pygame as pg

import globals as gb
import unit
import utils

if __name__ == '__main__':
	pass

mouse_pos = (0, 0)
simulation_is_running = True
pg.init()
clock = pg.time.Clock()
pg.display.set_caption(gb.NAME)
gb.window.fill(gb.WHITE)
person = unit.Unit(6, 12, gb.RED_INFANTRY)
ai = unit.Unit(6, 12, gb.BLACK_INFANTRY)
gb.game_map.screen.draw()
gb.game_map.draw_map_as_dots()
person.appear()
ai.appear()


def quit_procedure(sim):
	sim |= False
	pg.quit()


def redraw_screen():
	gb.game_map.screen.draw()
	gb.game_map.draw_map_as_dots()
	person.appear()
	ai.appear()


def key_handler():
	keys = pg.key.get_pressed()
	ret = False
	if keys[pg.K_LEFT] or keys[pg.K_a]:
		ret = gb.game_map.scroll_direct((1, 0))
	elif keys[pg.K_RIGHT] or keys[pg.K_d]:
		ret = gb.game_map.scroll_direct((-1, 0))
	if keys[pg.K_DOWN] or keys[pg.K_s]:
		ret = gb.game_map.scroll_direct((0, -1))
	elif keys[pg.K_UP] or keys[pg.K_w]:
		ret = gb.game_map.scroll_direct((0, 1))
	return ret


def mouse_handler():
	global mouse_pos
	ret = False
	current_hex = None
	new_mouse_pos = pg.mouse.get_pos()
	mouse_pressed = pg.mouse.get_pressed(5)
	if new_mouse_pos != mouse_pos:
		mouse_pos = tuple(new_mouse_pos)
	for that_hex in gb.game_map.hexes:
		if that_hex.is_point_inside_hexagon(mouse_pos[0], mouse_pos[1]):
			that_hex.fill_hex(gb.FILL_COLOR, gb.SELECT_SIZE)
			that_hex.info_box.write_info()
			current_hex = that_hex
		else:
			that_hex.clear_hex()
	if current_hex and mouse_pressed[0]:
		current_hex.select()
		ret |= True
		gb.game_map.unselect_other_hexes(current_hex)
		if person.occupied_hex == current_hex:
			person.select()
		elif person.is_selected:
			person.move(current_hex)
			person.unselect()
	ret |= gb.game_map.scroll(mouse_pos)
	return ret


while simulation_is_running:
	for event in pg.event.get():
		if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
			quit_procedure(simulation_is_running)
	if person.is_selected:
		person.write_unit_info()
	if key_handler() or mouse_handler():
		redraw_screen()
	redraw_screen()
	pg.display.update()
	clock.tick(gb.FPS)
