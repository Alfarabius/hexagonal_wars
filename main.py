import pygame

import global_vars
import unit

mouse_pos = (0, 0)
game_is_running = True
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption(global_vars.NAME)
global_vars.window.fill(global_vars.WHITE)
person = unit.Unit(6, 12, global_vars.RED_INFANTRY)
ai = unit.Unit(6, 12, global_vars.BLACK_INFANTRY)


def quit_procedure(sim):
	sim |= False
	pygame.quit()


def redraw_screen():
	global_vars.game_map.screen.draw()
	global_vars.game_map.draw_map()
	person.appear()
	ai.appear()


def key_handler():
	keys = pygame.key.get_pressed()
	ret = False
	if keys[pygame.K_LEFT] or keys[pygame.K_a]:
		ret = global_vars.game_map.scroll_direct((1, 0))
	elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		ret = global_vars.game_map.scroll_direct((-1, 0))
	if keys[pygame.K_DOWN] or keys[pygame.K_s]:
		ret = global_vars.game_map.scroll_direct((0, -1))
	elif keys[pygame.K_UP] or keys[pygame.K_w]:
		ret = global_vars.game_map.scroll_direct((0, 1))
	return ret


def mouse_handler():
	global mouse_pos
	ret = False
	current_hex = None
	new_mouse_pos = pygame.mouse.get_pos()
	mouse_pressed = pygame.mouse.get_pressed(5)
	if new_mouse_pos != mouse_pos:
		mouse_pos = tuple(new_mouse_pos)
	for that_hex in global_vars.game_map.hexes:
		if that_hex.is_point_inside_hexagon(mouse_pos[0], mouse_pos[1]):
			that_hex.fill_hex(global_vars.SELECT_COLOR, global_vars.SELECT_SIZE)
			that_hex.info_box.write_info()
			current_hex = that_hex
		else:
			that_hex.clear_hex()
	if current_hex and mouse_pressed[0]:
		current_hex.select()
		ret |= True
		global_vars.game_map.unselect_other_hexes(current_hex)
		if person.occupied_hex == current_hex:
			person.select()
		elif person.is_selected:
			person.move(current_hex)
			person.unselect()
	ret |= global_vars.game_map.scroll(mouse_pos)
	return ret


def main():
	while game_is_running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				quit_procedure(game_is_running)
		if person.is_selected:
			person.write_unit_info()
		if key_handler() or mouse_handler():
			redraw_screen()
		redraw_screen()
		pygame.display.update()
		clock.tick(global_vars.FPS)


if __name__ == '__main__':
	main()
