import pygame

from MenuItem import MenuItem, MenuItemNormal, MenuItemContact, MenuItemContactInfo
from MenuCursor import MenuCursor

class MenuPage:
	""" Parent class for other MenuPages.
	Draw the MenuItems, manage the cursor and the key events
	
	:param mitems: a list of MenuItem objects
	:type mitems: list
	:param opts: a dictionary of options
	:type opts: dict
	"""
	
	def __init__(self, mitems=None, opts=None):
		if opts is None:
			opts = {}
		if not 'type' in opts:
			opts['type'] = 'normal'
		if not 'key_event' in opts:
			opts['key_event'] = self.key_event
		if mitems is None:
			mitems = [MenuItemLabel({'size': 3})]
		self.mitems = mitems
		self.opts = opts
		self.cursor = MenuCursor(self)
		
	def get_opt(self, index):
		""" Get an option
		
		:param index: index of the option
		:type index: str
		:returns: The option asked for
		"""
		return self.opts[index]
	
	def set_opt(self, index, new_opt):
		""" Set an option
		
		:param index: index of the options
		:type index: str
		:param new_opt: the new value for the option
		"""
		self.opts[index] = new_opt
		
	def get_opts(self):
		""" Get all the options
		
		:returns: all the options
		:rtype: dict
		"""
		return self.opts
		
	def set_opts(self, new_opts):
		""" Set all the options
		
		:param new_opts: new options
		:type new_opts: dict
		"""
		self.opts = new_opts
		
	def get_menu_item(self, pos):
		""" Get a menu item
		
		:param pos: position in the list
		:type pos: int
		:returns: a MenuItem object
		:rtype: MenuItem object
		"""
		return self.mitems[pos]
	
	def set_menu_item(self, pos, new_item):
		""" Set a menu item
		
		:param pos: position in the list
		:type pos: int
		:param new_item: new MenuItem
		:type new_item: MenuItem object
		"""
		self.mitems[pos] = new_item
		
	def get_menu_items(self):
		""" Get all the menu items
		
		:returns: all the menu items
		:rtype: list
		"""
		return self.mitems
	
	def set_menu_items(self, new_items):
		""" Set all the menu items
		
		:param new_items: list of new items
		:type new_items: list
		"""
		self.mitems = new_items
		
	def display(self, surface):
		""" Display the MenuPage
		
		:param surface: the Surface where we draw the MenuPage
		:type surface: pygame.Surface object
		"""
		self.populate()
		y_offset = 20
		x_offset = 0
		for x in range(self.cursor.get_offset(), self.cursor.get_offset() + 3):
			try:
				if self.mitems is not None:
					self.mitems[x].draw(surface, x_offset, y_offset)
			except IndexError:
				break
			y_offset = y_offset + (36 * self.mitems[x].get_size())
		self.cursor.display(surface)
			
	def populate(self):
		""" Populate.
		Does nothing, used for children classes
		"""
		pass
	
	def key_event(self, event, ui):
		""" Key event.
		Does nothing, used for children classes
		"""
		pass
	
	def on_return(self):
		""" On return callback.
		Does nothing, used for children classes
		"""
		pass
	
	def on_go_to(self):
		""" On go to callback. Called when the UI returns to a previous page.
		"""
		if 'reset_cursor' in self.opts:
			if self.opts['reset_cursor']:
				self.cursor_pos = 0
				self.menu_offset = 0
	
	def on_quit(self):
		""" On quit callback.
		Does nothing, used for children classes
		"""
		print("Quitting ", self)
		pass
		
		
		
class MenuPageList(MenuPage):
	""" MenuPage displaying a list
	
	:param mitems: a list of MenuItem objects
	:type mitems: list
	:param opts: a dictionary of options
	:type opts: dict
	"""
	
	def __init__(self, mitems, opts=None):
		super().__init__(mitems, opts)
	
	def display(self, surface):
		""" Display the MenuPage
		
		:param surface: the Surface where we draw the MenuPage
		:type surface: pygame.Surface object
		"""
		super().display(surface)
			
	def key_event(self, event, ui):
		""" Key event
		
		:param event: the event triggered
		:type event: pygame.event
		:param ui: reference to the UI
		:type ui: MenuUI object
		"""
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_KP8:
				self.cursor.next()
            
			if event.key == pygame.K_KP2:
				self.cursor.previous()
                    
			if event.key == pygame.K_KP5:
				action = self.mitems[self.cursor.get_absolute_pos()].get_opt('action')
				action(ui)
                    
			if event.key == pygame.K_r:
				ui.return_page()
		
		
		
class MenuPageContactList(MenuPageList):
	""" MenuPage displaying a contact list
	
	:param tox: a tox object
	:type tox: Tox object
	"""
	def __init__(self, tox):
		self.tox = tox
		self.mitems = []
		for contact in self.tox.list_friends():
			self.mitems.append(MenuItemContact({'label': contact[1], 'connection_status': contact[2], 'status': contact[3]}))
			self.mitems[-1].opts['goto'] = MenuPageContact(self.tox, contact[0])
		super().__init__(self.mitems)
		
	def populate(self):
		""" Update the contact name, connection status and status
		"""
		friend_list = self.tox.list_friends()
		if len(friend_list) != len(self.mitems):
			new_items = []
			for index, contact in enumerate(friend_list):
				new_items.append(MenuItemContact({'label': contact[1], 'connection_status': contact[2], 'status': contact[3]}))
				self.set_menu_items(new_items)
		else:
			for index, contact in enumerate(friend_list):
				self.mitems[index].set_label(contact[1])
				self.mitems[index].set_connection_status(contact[2])
				self.mitems[index].set_status(contact[3])
		
		
		
class MenuPageContact(MenuPage):
	""" MenuPage displaying the contacts info. Include a button to call the contact.
	
	:param tox: a tox object
	:type tox: Tox object
	:param friend_number: the number of the friend to call
	:type friend_number: int
	"""
	
	def __init__(self, tox, friend_number):
		self.tox = tox
		self.friend_name = tox.friend_get_name(friend_number)
		self.friend_status_message = tox.friend_get_status_message(friend_number)
		self.friend_number = friend_number
		super().__init__([MenuItemContactInfo({'label': self.friend_name}),
						MenuItemNormal({
							'label': 'Call',
							'action': lambda ui: ui.call(self.friend_number),
							'icon': 'img/call.png',
							'filled': True,
							'fill_color': (0, 120, 0)
						})
		])
		self.cursor.set_pos(1)
		self.cursor.set_lock(True)
	
	def populate(self):
		""" Update the contact name, status, connection_status and last seen online
		"""
		self.mitems[0].set_label(self.tox.friend_get_name(self.friend_number))
		self.mitems[0].set_status_message(self.tox.friend_get_status_message(self.friend_number))
		self.mitems[0].set_status(self.tox.friend_get_status(self.friend_number))
		self.mitems[0].set_connection_status(self.tox.friend_get_connection_status(self.friend_number))
		self.mitems[0].set_last_seen(self.tox.friend_get_last_online(self.friend_number))
		
	def key_event(self, event, ui):
		""" Key event
		
		:param event: the event triggered
		:type event: pygame.event
		:param ui: reference to the UI
		:type ui: MenuUI object
		"""
		if event.type == pygame.KEYDOWN:
			
			if event.key == pygame.K_KP5:
				if self.tox.friend_get_connection_status(self.friend_number) and self.tox.self_get_connection_status():
					action = self.mitems[self.cursor.get_absolute_pos()].get_opt('action')
					action(ui)
					
			if event.key == pygame.K_r:
				ui.return_page()
			
			
			
class MenuPageCall(MenuPage):
	""" MenuPage displaying the call status and information. Include a button to hangup.
	
	:param tox: a tox object
	:type tox: Tox object
	:param friend_number: the number of the friend to call
	:type friend_number: int
	"""
	
	def __init__(self, tox, friend_number):
		self.tox = tox
		self.friend_name = tox.friend_get_name(friend_number)
		self.friend_number = friend_number
		super().__init__([MenuItemNormal({'label': 'Calling ' + self.friend_name, 'size': 2}),
						MenuItemNormal({
							'label': 'Hangup',
							'action': lambda ui: ui.hangup(self.friend_number),
							'icon': 'img/hangup.png',
							'filled': True,
							'fill_color': (120, 0, 0)
						})
		])
		self.cursor_pos = 1
		self.menu_offset = 0
		#self.tox.call(self.friend_number)
	
	def populate(self):
		""" Update the label
		"""
		self.mitems[0].set_label('Calling ' + self.tox.friend_get_name(self.friend_number))
		
	def key_event(self, event, ui):
		""" Key event
		
		:param event: the event triggered
		:type event: pygame.event
		:param ui: reference to the UI
		:type ui: MenuUI object
		"""
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN or event.key == pygame.K_KP5:
				action = self.mitems[self.cursor_pos + self.menu_offset].get_opt('action')
				action(ui)
			
			
			
class MenuPageIncomingCall(MenuPage):
	""" Called when there is an incoming call.
	
	Displays the call status and information. Include a button to take the call.
	
	:param tox: a tox object
	:type tox: Tox object
	:param friend_number: the number of the friend to call
	:type friend_number: int
	"""
	
	def __init__(self, tox, friend_number):
		self.tox = tox
		self.friend_name = tox.friend_get_name(friend_number)
		self.friend_number = friend_number
		super().__init__([MenuItemNormal({'label': 'Incoming call: ' + self.friend_name, 'size': 2}),
						MenuItemNormal({
							'label': 'Answer',
							'action': lambda ui: ui.answer(self.friend_number),
							'icon': 'img/call.png',
							'filled': True,
							'fill_color': (0, 120, 0)
						})
		])
		self.cursor_pos = 1
		self.menu_offset = 0
		#self.tox.call(self.friend_number)
	
	def populate(self):
		""" Update the label
		"""
		self.mitems[0].set_label('Incoming call: ' + self.tox.friend_get_name(self.friend_number))
		
	def on_return(self):
		""" Called when the UI return one page back
		"""
		self.tox.av.call_control(self.friend_number, self.tox.av.CALL_CONTROL_CANCEL)
		
	def key_event(self, event, ui):
		""" Key event
		
		:param event: the event triggered
		:type event: pygame.event
		:param ui: reference to the UI
		:type ui: MenuUI object
		"""
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RETURN or event.key == pygame.K_KP5:
				action = self.mitems[self.cursor_pos + self.menu_offset].get_opt('action')
				action(ui)
				
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_KP5:
				action = self.mitems[self.cursor_pos + self.menu_offset].get_opt('action')
				action(ui)
			
			if event.key == pygame.K_r:
				ui.stop_ring()
				ui.return_page()
			
			
			
class MenuPageAbout(MenuPage):
	""" An "About" page
	"""
	
	def __init__(self):
		super().__init__([MenuItemNormal({'size': 3})])
		self.cursor.set_visibility(False)
		
	def key_event(self, event, ui):
		""" Key event. Always get back to the previous page.
		
		:param event: the event triggered
		:type event: pygame.event
		:param ui: reference to the UI
		:type ui: MenuUI object
		"""
		if event.type == pygame.KEYDOWN:
			ui.return_page()
