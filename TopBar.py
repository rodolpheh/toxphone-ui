import pygame
import time
import subprocess

class TopBar:
	def __init__(self):
		self.clock_font = pygame.font.Font(None, 16)
		self.wifi_on_icon = pygame.image.load("img/wifi_on.png")
		self.wifi_off_icon = pygame.image.load("img/wifi_off.png")
		self.left_widgets = []
		self.right_widgets = []
		
	def get_wifi_status(self):
		"""
		Get the Wi-Fi status

		:returns: The Wi-Fi status
		:rtype: bool
        """
		return self.wifi_on()
    
	def wifi_on(self):
		"""
		Test the connection by checking if the wireless interface has an assigned IP address
        
		:returns: True if connected, False if not
		:rtype: bool
		"""
		
		ip = subprocess.check_output(
				"echo `ifconfig \`ls /sys/class/net/ | grep wl\` | grep inet | cut -d: -f2 | awk '{print $2}' | head -1`",
				stderr=subprocess.STDOUT,
				shell=True)
		ip = ip[0:-2]
		if ip.decode("utf-8"):
			return True
		return False

	def display(self, surface):
		"""
		Display the TopBar
		
		:param surface: the Surface where we draw the TopBar
		:type surface: pygame.Surface object
		"""
		
		pygame.draw.rect(surface, (28, 28, 28), (0, 0, 160, 18), 0)
		fclock = self.clock_font.render(time.strftime('%H:%M'), True, (255,255,255))
		surface.blit(fclock, (60, 6))
		if self.get_wifi_status(): 
			icon = self.wifi_on_icon
		else:
			icon = self.wifi_off_icon
			
		icon_pos = icon.get_rect()
		icon_pos.centery = 18 / 2
		icon_pos.right = 155
		surface.blit(icon, icon_pos)
		
class ToxPhoneTopBar(TopBar):
	"""
	Child of TopBar
	"""
	
	def __init__(self):
		super().__init__()
		self.connection_status = False
		self.online_icon = pygame.image.load("img/online.png")
		self.offline_icon = pygame.image.load("img/offline.png")
	
	def on_self_connection_status(self, status):
		"""
		Set our connection status
		
		:returns: The connection status
		:rtype: bool
		"""
		if not status:
			self.connection_status = False
		else:
			self.connection_status = True
			
	def display(self, surface):
		"""
		Display our connection icon
		"""
		super().display(surface)
		
		if self.connection_status: 
			icon = self.online_icon
		else:
			icon = self.offline_icon
			
		icon_pos = icon.get_rect()
		icon_pos.centery = 18 / 2
		icon_pos.right = 160 - 20
		surface.blit(icon, icon_pos)
		
class TopBarWidget:
	
	def __init__(self, label=None, icon=None):
		self.label = label
		self.icon = icon
		
	def set_label(self, new_label):
		self.label = new_label
		
	def set_icon(self, new_icon):
		self.icon = new_icon
		
	def draw(self, surface, x):
		if self.icon is not None:
			pass