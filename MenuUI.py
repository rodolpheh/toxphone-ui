from TopBar import ToxPhoneTopBar

class MenuUi:
	"""
	Act as a controller for the whole UI
	Manage the breadcrumb (tracking of the navigation) and the current page
		
	:param surface: a pygame.Surface object where we will be drawing the UI
	:type surface: pygame.Surface object
	:param start_page: a MenuPage object representing the tree of the UI
	:type start_page: MenuPage object
	"""
	
	def __init__(self, surface, start_page):
		self.breadcrumb = []
		self.surface = surface
		self.current_page = start_page
		self.alive = True
		self.topbar = ToxPhoneTopBar()
		
	def kill(self):
		""" Kill the loop by setting alive False
		"""
		self.alive = False
	
	def set_current_page(self, new_page):
		""" Set current page
		
		:param new_page: the new page.
		:type new_page: MenuPage object
		"""
		self.current_page = new_page
	
	def get_current_page(self):
		""" Get current page
		
		:returns: Current page
		:rtype: MenuPage object
		"""
		return self.current_page
		
	def get_breadcrumb(self):
		""" Get breadcrumb
		
		:returns: List of MenuPage objects
		:rtype: list
		"""
		return self.breadcrumb
	
	def set_breadcrumb(self, new_breadcrumb):
		""" Set breadcrumb
		
		:param new_breadcrumb: a list of MenuPage objects.
		:type new_breadcrumb: list
		"""
		self.breadcrumb = new_breadcrumb
		
	def append_breadcrumb(self, appended):
		""" Append a MenuPage object to the breadcrumb
		
		:param appended: a MenuPage object to append
		:type appended: MenuPage object
		"""
		self.breadcrumb.append(appended)
		
	def return_page(self):
		""" Return (get one step back in the breadcrumb)
		"""
		self.current_page.on_return()
		if self.breadcrumb:
			self.set_current_page(self.breadcrumb.pop())

	def cursor_action(self):
		""" Cursor action
		Not sure it's going to stay
		"""
		menu_item = self.current_page.get_menu_item(self.current_page.get_cursor_pos() + self.current_page.get_menu_offset())
		menu_action = menu_item.get_opt('action')
		menu_action(self)
		
	def go_to_page(self, page):
		""" Go to page
		
		:param page: the page the UI should display
		:type page: MenuPage object
		"""
		self.current_page.on_quit()
		self.append_breadcrumb(self.current_page)
		self.set_current_page(page)
		self.current_page.on_go_to()
	
	def display(self):
		""" Update the current page display
		"""
		self.current_page.display(self.surface)
		self.topbar.display(self.surface)
		
	def key_event(self, event):
		""" Key event
		
		:param event: a key event
		:type event: pygame.event
		"""
		page_key_event = self.current_page.get_opt('key_event')
		page_key_event(event, self)
		
		'''
		if event.type == pygame.KEYDOWN:
			
			if event.key == pygame.K_KP8:
				self.cursor_next()
            
			if event.key == pygame.K_KP2:
				self.cursor_previous()
                    
			if event.key == pygame.K_KP5:
				self.cursor_action()
                    
			if event.key == pygame.K_r:
				self.return_page()
		'''