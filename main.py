import sys
import pygame
import pyaudio
import os

from os.path import exists

from MenuItem import MenuItem, MenuItemToggable, MenuItemContact, MenuItemNormal
from MenuPage import MenuPage, MenuPageList, MenuPageContact, MenuPageAbout, MenuPageContactList
from MenuUI import MenuUi
from ToxPhone import ToxOptions, ToxAV, ToxPhone

# Window's color and size
window_height = 128
window_width = 160
bg_color = (65, 65, 65)

DATA = 'echo.data'

pygame.init()
toxphone_display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Toxphone GUI')

opts = ToxOptions()
opts.udp_enabled = True
if len(sys.argv) == 2:
    DATA = sys.argv[1]
if exists(DATA):
        opts.savedata_data = open(DATA, 'rb').read()
        opts.savedata_length = len(opts.savedata_data)
        opts.savedata_type = ToxPhone.SAVEDATA_TYPE_TOX_SAVE
        opts.savedata_path = DATA

# Menu items
main_menu = MenuPageList([])
menu_ui = ToxPhone(toxphone_display, main_menu, opts)
menu_ui.current_page.set_menu_items([
					MenuItemNormal({
						'label': 'Contacts',
						'goto': MenuPageContactList(menu_ui)
					}),
					MenuItemNormal({
						'label': 'Profile',
						'goto': MenuPageList([
							MenuItemNormal({
								'label': 'Name'
							}),
							MenuItemNormal({
								'label': 'Status'
							}),
							MenuItemNormal({
								'label': 'Status message'
							})
							], opts={'reset_cursor': True})
					}),
					MenuItemNormal({
						'label': 'Parameters',
						'goto': MenuPageList([
							MenuItemNormal({
								'label': 'Network',
								'enabled': False
							}),
							MenuItemNormal({
								'label': 'Tox',
								'goto': MenuPageList([
									MenuItemToggable({
										'label': 'UDP',
										'status': True
									}),
									MenuItemToggable({
										'label': 'IPv6',
										'status': False
									}),
									MenuItemNormal({
										'label': 'Proxy'
									})
								])
							}),
							MenuItemNormal({
								'label': 'Phone'
							})

							], opts={'reset_cursor': True})
					}),
					MenuItemNormal({
						'label': 'About',
						'goto': MenuPageAbout()
					}),
					MenuItemNormal({
						'label': 'Quit',
						'action': lambda ui: ui.kill()
					})
			])

clock = pygame.time.Clock()
toxphone_display.fill(bg_color)
pygame.mouse.set_visible(0)
pygame.event.set_blocked(pygame.MOUSEMOTION)
pygame.event.set_blocked(pygame.ACTIVEEVENT)
pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)

checked = False
menu_ui.save_tox_conf()

while menu_ui.alive:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			menu_ui.kill()
		menu_ui.key_event(event)

	status = menu_ui.self_get_connection_status()

	if not checked and status:
		print('Connected to DHT.')
		checked = True

	if checked and not status:
		print('Disconnected from DHT.')
		menu_ui.connect()
		checked = False

	menu_ui.av.iterate()
	menu_ui.iterate()
	if not menu_ui.call_status['status']:
		toxphone_display.fill(bg_color)
		menu_ui.display()
		pygame.display.flip()
	clock.tick(10)
	#print(clock.get_fps())

print("Gracefully exiting...\nSaving Tox datas.")
'''
menu_ui.av_iterate_thread_stop = True
if menu_ui.av_iterate_thread:
	menu_ui.av_iterate_thread.join()
menu_ui.core_iterate_thread_stop = True
if menu_ui.core_iterate_thread:
	menu_ui.core_iterate_thread.join()
'''
menu_ui.save_tox_conf()
print("Killing Tox instance.")
menu_ui.tox_kill()
print("Killing PyGame instance.")
pygame.quit()
print("Quitting.")
quit()
