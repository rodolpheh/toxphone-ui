import pygame
import utils

from pytox import Tox

pygame.init()

class MenuItem:
	""" MenuItem class.
	
	Define a widget style class with icon, label and all...
	
	:param opts: options for the MenuItem
	:type opts: dict
	"""

	def __init__(self, opts=None):
		if opts is None:
			opts = {}
		if not 'action' in opts:
			opts['action'] = self.action
		self.opts = opts
		
    
	def set_opts(self, new_opts):
		""" Set new options
		
		:param new_opts: new options
		:type new_opts: dict
		"""
		self.opts = new_opts
    
	def get_opts(self):
		""" Get all the options
		
		:returns: all the options
		:rtype: dict
		"""
		return self.opts
	
	def set_opt(self, index, new_opt):
		""" Set one option
		
		:param index: index of the option
		:type index: str
		:param new_opt: new option
		"""
		self.opts[index] = new_opt
		
	def get_opt(self, index):
		""" Get one options
		
		:param index: index of the option
		:type index: str
		:returns: the option
		"""
		return self.opts[index]
	
	def action(self, ui):
		""" Action of the MenuItem. Default implementation does nothing.
		
		:param ui: the MenuUi object with which to interact
		:type ui: MenuUi object
		"""
		print(self)
		pass
		
		
		
class MenuItemNormal(MenuItem):
	
	def __init__(self, opts=None):
		super().__init__(opts)
		
		# Set default options
		if not 'label' in self.opts:
			self.opts['label'] = 'MenuItem'
		if not 'filled' in self.opts:
			self.opts['filled'] = False
		if not 'enabled' in self.opts:
			self.opts['enabled'] = True
		if not 'size' in self.opts:
			self.opts['size'] = 1
		if self.opts['filled']:
			if not 'fill_color' in self.opts:
				self.opts['fill_color'] = (65, 65, 65)
		
		# Create font renderer and colors
		self.font = pygame.font.Font(None, 20)
		self.font_color = (255, 255, 255)
		self.disabled_font_color = (190, 190, 190)
		self.border_color = (0, 0, 0)
		self.selected_color = (255, 255, 255)
		
		# Load icon if indicated
		if 'icon' in opts:
			self.icon = pygame.image.load(self.opts['icon'])
		
	def set_label(self, new_label):
		""" Set a new label for the MenuItem.
		
		:param new_label: the new label
		:type new_label: str
		"""
		self.opts['label'] = new_label
        
	def get_label(self):
		""" Get the label of the MenuItem
		
		:returns: the label
		:rtype: str
		"""
		return self.opts['label']
	
	def set_size(self, new_size):
		""" Set the size of the MenuItem (1, 2 or 3 rows)
		
		:param new_size: new size
		:type new_size: int
		"""
		self.opts['size'] = new_size
		
	def get_size(self):
		""" Get the size of the MenuItem
		
		:returns: the size
		:rtype: int
		"""
		return self.opts['size']
		
	def draw(self, surface, x, y):
		""" Draw the item
		
		:param surface: the pygame.Surface on which to draw
		:type surface: pygame.Surface object
		:param x: X coordinate to draw on
		:type x: int
		:param y: Y coordinate to draw on
		:type y: int
		:param selected: True if the MenuItem is selected
		:type selected: bool
		"""
		if self.opts['filled']:
			utils.draw_rounded_rectangle(surface, self.opts['fill_color'], ((x + 5), (y + 5), (160 - 10), ((36 * self.get_size()) - 10)), True)
		self.default_font_placement(surface, x, y)
		self.place_icon(surface, x, y)
		
	def default_font_placement(self, surface, x, y):
		""" Place the font at a default location.
		
		:param surface: the pygame.Surface on which to draw
		:type surface: pygame.Surface object
		:param x: X coordinate to draw on
		:type x: int
		:param y: Y coordinate to draw on
		:type y: int
		"""
		x_offset = 10
		if 'icon' in self.opts:
			x_offset += 24
		label = self.font.render(self.opts['label'], True, self.font_color if self.opts['enabled'] else self.disabled_font_color)
		
		label_pos = label.get_rect()
		label_pos.centery = y + (36/2)
		label_pos.left = x + x_offset

		surface.blit(label, label_pos)
		
	def place_icon(self, surface, x, y):
		""" Place the icon if `icon` is defined
		
		:param surface: the pygame.Surface on which to draw
		:type surface: pygame.Surface object
		:param x: X coordinate to draw on
		:type x: int
		:param y: Y coordinate to draw on
		:type y: int
		"""
		if 'icon' in self.opts:
			icon_pos = self.icon.get_rect()
			icon_pos.centery = y + (36/2)
			icon_pos.left = x + 10
			surface.blit(self.icon, icon_pos)
		
	def action(self, ui):
		""" Override of the parent function
		PUT A LINK TO THE PARENT FUNCTION HERE
		"""
		if 'goto' in self.opts:
			ui.go_to_page(self.opts['goto'])
		
		
		
class MenuItemToggable(MenuItemNormal):
	
	def __init__(self, opts=None):
		super().__init__(opts)
		
		# Set default options
		if not 'status' in self.opts:
			self.opts['status'] = False
			
		# Load on and off states icons
		self.on = pygame.image.load("img/on.png")
		self.off = pygame.image.load("img/off.png")
		
	def get_status(self):
		""" Get the status of the item
		
		:returns: the status
		:rtype: bool
		"""
		return self.opts['status']
		
	def set_status(self, new_status):
		""" Set the status of the item
		
		:param new_status: new status
		:type new_size: bool
		"""
		self.opts['status'] = new_status
		
	def toggle_status(self):
		""" Toggle the status
		"""
		self.opts['status'] = False if self.opts['status'] else True
	
	def draw(self, surface, x, y):
		""" Draw the item. Based on its parent function
		PUT A LINK TO THE PARENT FUNCTION HERE
		"""
		super().draw(surface, x, y)
		image = self.on if self.opts['status'] else self.off
		image_pos = image.get_rect()
		image_pos.centery = y + (36/2)
		image_pos.right = 160 - 18
		surface.blit(image, image_pos)
			
	def action(self, ui):
		""" Override of the parent function
		PUT A LINK TO THE PARENT FUNCTION HERE
		"""
		self.toggle_status()
			
			
			
class MenuItemContact(MenuItemNormal):
	
	def __init__(self, opts=None):
		super().__init__(opts)
		
		# Setting the default parameters
		if not 'type' in self.opts:
			self.opts['type'] = 'contact'
		if not 'connection_status' in self.opts:
			self.opts['connection_status'] = False
		if not 'status' in self.opts:
			self.opts['status'] = 0
		
		self.online = pygame.image.load("img/online.png")
		self.offline = pygame.image.load("img/offline.png")
		self.away = pygame.image.load("img/away.png")
		self.busy = pygame.image.load("img/busy.png")
		
	def get_status(self):
		""" Get the status of the contact
		
		:returns: the status (0: NONE, 1: AWAY, 2: BUSY)
		:rtype: int
		"""
		return self.opts['status']
		
	def set_status(self, new_status):
		""" Set the status of the contact
		
		:param new_status: new status
		:type new_status: int
		"""
		self.opts['status'] = new_status
		
	def get_connection_status(self):
		""" Get the connection status of the contact
		
		:returns: the status (0: OFFLINE, 1: ONLINE)
		:rtype: bool
		"""
		return self.opts['connection_status']
	
	def set_connection_status(self, new_connection_status):
		""" Set the connection status of the contact
		
		:param new_connection_status: new connection status
		:type new_connection_status: bool
		"""
		self.opts['connection_status'] = new_connection_status
	
	def draw(self, surface, x, y):
		""" Override of the parent function
		PUT A LINK TO THE PARENT FUNCTION HERE
		"""
		super().draw(surface, x, y)
		self.draw_status(surface, x, y)
	
	def draw_status(self, surface, x, y):
		""" Place the appropriate status icon
		
		:param surface: the pygame.Surface on which to draw
		:type surface: pygame.Surface object
		:param x: X coordinate to draw on
		:type x: int
		:param y: Y coordinate to draw on
		:type y: int
		"""
		if not self.opts['connection_status']:
			image = self.offline
		else:
			if self.opts['status'] is Tox.USER_STATUS_NONE:
				image = self.online
			elif self.opts['status'] is Tox.USER_STATUS_AWAY:
				image = self.away
			elif self.opts['status'] is Tox.USER_STATUS_BUSY:
				image = self.busy
				
		image_pos = image.get_rect()
		image_pos.centery = y + (36/2)
		image_pos.right = 160 - 15
		surface.blit(image, image_pos)
		
		
		
class MenuItemContactInfo(MenuItemContact):
	
	def __init__(self, opts=None):
		super().__init__(opts)
		
		# Set the default parameters
		if not 'status_message' in opts:
			opts['status_message'] = ''
		if not 'last_seen' in opts:
			opts['last_seen'] = None
			
		self.opts['size'] = 2
		self.status_font = pygame.font.Font(None, 18)
		self.last_seen_font = pygame.font.Font(None, 14)
		self.status_font.set_italic(True)
		
	def get_status_message(self):
		return self.opts['status_message']
	
	def set_status_message(self, new_message):
		self.opts['status_message'] = new_message
		
	def get_last_seen(self):
		return self.opts['last_seen']
	
	def set_last_seen(self, seen_time):
		self.opts['last_seen'] = seen_time
		
	def draw(self, surface, x, y):
		super().draw(surface, x, y)
		self.draw_status_message(surface, x, y)
		self.draw_last_seen(surface, x, y)
				
	def draw_status_message(self, surface, x, y):
		label = self.status_font.render(self.opts['status_message'], True, self.font_color)
		label2 = self.status_font.render(self.opts['status_message'], True, self.border_color)
		surface.blit(label2, ((x + 10), (y + 21 + (30 - 20))))
		surface.blit(label, ((x + 10), (y + 20 + (30 - 20))))
		
	def draw_last_seen(self, surface, x, y):
		label = self.last_seen_font.render("Last seen " + (self.opts['last_seen'].strftime('the %d %b at %H:%M') if self.opts['last_seen'] is not None else ': never'), True, self.font_color)
		surface.blit(label, ((x + 10), (y + 40 + (30 - 20))))
		
		