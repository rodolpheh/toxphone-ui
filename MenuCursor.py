import pygame
import utils

class MenuCursor:
	""" Manage and display a cursor object
	
	:param page: the MenuPage calling the cursor
	:type mitems: MenuPage object
	"""
	
	def __init__(self, page):
		self.pos = 0
		self.offset = 0
		self.ypos = 20
		self.visible = True
		self.lock = False
		self.color = (255, 255, 255)
		self.page = page
		
	def get_offset(self):
		""" Get menu offset
		
		:returns: menu offset
		:rtype: int
		"""
		return self.offset
	
	def set_offset(self, new_offset):
		""" Set menu offset
		
		:param new_offset: new offset
		:type new_offset: int
		"""
		self.offset = new_offset
		
	def get_pos(self):
		""" Get cursor position
		
		:returns: cursor position
		:rtype: int
		"""
		return self.pos
		
	def set_pos(self, new_pos):
		""" Set cursor position
		
		:param new_pos: new position
		:type new_pos: int
		"""
		if new_pos in range(0, 3):
			self.ypos = 20 + (new_pos * 36 * self.page.mitems[self.pos + self.offset].get_size())
			self.pos = new_pos
		else:
			print("Error, new_pos should be set between 0 and 2")
			
	def get_visibility(self):
		""" Get cursor visibility
		
		:returns: cursor visibility bit
		:rtype: bool
		"""
		return self.visible
	
	def set_visibility(self, visibility):
		""" Set cursor visibility
		
		:param visibility: set True for a visible cursor
		:type visibility: bool
		"""
		self.visible = visibility
		
	def get_lock(self):
		""" Get cursor lock
		
		:returns: cursor lock bit
		:rtype: bool
		"""
		return self.lock
	
	def set_lock(self, new_lock):
		""" Set cursor lock
		
		:param new_lock: set True for a locked cursor
		:type new_lock: bool
		"""
		self.lock = new_lock
		
	def get_absolute_pos(self):
		""" Get absolute cursor position
		
		:returns: the sum of the cursor position and the menu offset
		:rtype: int
		"""
		return (self.pos + self.offset)
		
	def display(self, surface):
		""" Display the MenuCursor
		
		:param surface: the Surface where we draw the MenuCursor
		:type surface: pygame.Surface object
		"""
		if self.visible:
			rect = (5, (self.ypos + 5), (160 - 10), ((36 * self.page.mitems[self.pos + self.offset].get_size() - 10)))
			utils.draw_rounded_rectangle(surface, self.color, rect, False)
		
	def next(self):
		""" Move the cursor to the next position
		"""
		if not self.lock:
			if self.pos == 2 and self.offset + self.pos == len(self.page.mitems) - 1:
				pass
			elif self.pos < 2:
				self.set_pos(self.get_pos() + 1)
			else:
				self.offset +=1
		
	def previous(self):
		""" Move the cursor to the previous position
		"""
		if not self.lock:
			if self.pos == 0 and self.offset == 0: 
				pass
			elif self.pos > 0:
				self.set_pos(self.get_pos() - 1)
			else:
				self.offset -= 1
