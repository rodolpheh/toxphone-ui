import pygame
import math
 
 
def draw_rounded_rectangle(surface, color, rect, filled, radius=0.4):
	if radius == 0:
		print("Error drawing rounded rectangle : radius should be different than 0")
		return False
	rect = pygame.Rect(rect)
	border = 0 if filled else 1
	
	color = pygame.Color(*color)
	pos = rect.topleft
	alpha = color.a
	rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

	circle_diameter = round(min(rect.size) * radius) if round(min(rect.size) * radius) % 2 == 0 else round(min(rect.size) * radius) + 1
	circle_radius = int(circle_diameter / 2)
	if True:
		circle = pygame.Surface([circle_diameter] * 2, pygame.SRCALPHA)
		pygame.draw.circle(circle, color, circle.get_rect().center, circle_radius, border)
	else:
		circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
		pygame.draw.ellipse(circle, color, circle.get_rect(), border * int(min(rect.size) * 3 / circle_radius))
		circle = pygame.transform.smoothscale(circle, [circle_diameter] * 2)
		
	pygame.draw.line(surface, color, (rect.left, rect.top + circle_radius), (rect.left, rect.bottom - circle_radius), border)
	pygame.draw.line(surface, color, (rect.right - 1, rect.top + circle_radius), (rect.right - 1, rect.bottom - circle_radius), border)
	pygame.draw.line(surface, color, (rect.left + circle_radius, rect.top), (rect.right - circle_radius, rect.top), border) 
	pygame.draw.line(surface, color, (rect.left + circle_radius, rect.bottom - 1), (rect.right - circle_radius, rect.bottom - 1), border)
	
	rect.topleft = 0,0
	radius = rectangle.blit(circle, (0,0), (0, 0, circle_radius, circle_radius))
	radius.bottomright = rect.bottomright
	rectangle.blit(circle, radius, (circle_radius, circle_radius, circle_radius, circle_radius))
	radius.topright = rect.topright
	rectangle.blit(circle, radius, (circle_radius, 0, circle_radius, circle_radius))
	radius.bottomleft = rect.bottomleft
	rectangle.blit(circle, radius, (0, circle_radius, circle_radius, circle_radius))
	
	if filled:
		color.a = 0
		rectangle.fill((0,0,0), rect.inflate(-radius.w - 1, 0))
		rectangle.fill((0,0,0), rect.inflate(0, -radius.h - 1))
		rectangle.fill(color, special_flags = pygame.BLEND_RGBA_MAX)
		rectangle.fill((255, 255, 255, 255), special_flags = pygame.BLEND_RGBA_MIN)
	
	surface.blit(rectangle,pos)
