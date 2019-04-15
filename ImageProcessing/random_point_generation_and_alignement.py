# -*- coding: utf-8 -*-

import time
import pygame
import pygame.camera
import pygame.transform
import numpy as np
import pygame.surfarray
from random import *
from statistics import mean

## Fucntions

def f_linear(x, a, b):
	return(int(a*x + b))

def generate_random_point(surface, color, radius, min_radius = 5):
	radius = randint(min_radius,radius)
	x = randint(0, surface.get_width())
	y = randint(0, surface.get_height())

	pygame.draw.circle(surface, color, (x,y), radius)
	pygame.display.flip()
	return(0)

def generate_random_polygon(surface, color, size = 40, max_sides = 15):
	side_number = randint(3, max_sides)
	# "center" of the polygon
	x = randint(0, surface.get_width())
	y = randint(0, surface.get_height())
	vertices = []

	for i in range(side_number):
		vertices.append(((x + randint(-size, size)), (y + randint(-size, size))) )

	pygame.draw.polygon(surface, color, vertices)
	pygame.display.flip()
	return(0)

def random_color(max = 255):
	return(randint(0,max), randint(0,max), randint(0,max))

## Init
polygon = False; circle = not(polygon)
white = (255,255,255)
white_array = np.array([255,255,255])
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)
sensibility = (15,15,15)

display_width = 900
display_height = 600

display_window = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('window')

## Code

for i in range(10):
	display_window.fill(random_color(200))
	polygon = randint(0,1); circle = not(polygon)
	if circle:
		generate_random_point(display_window, red, 40)
		generate_random_point(display_window, green, 40)
	elif polygon:
		generate_random_polygon(display_window, red, 40, 20)
		generate_random_polygon(display_window, green, 40, 20)

	mask_red = pygame.mask.from_threshold(display_window, red, sensibility)
	mask_green = pygame.mask.from_threshold(display_window, green, sensibility)

	pos_red = mask_red.centroid()
	pos_green = mask_green.centroid()


	print("---------------i = " + str(i) + "------------------------")
	print("Centre des pixels rouges : " + str(pos_red))
	print("Centre des pixels vert : " + str(pos_green))

	#Evaluation de la droite entre les 2 points : y = ax + b
	a = (pos_green[1] - pos_red[1]) / (pos_green[0]-pos_red[0])
	b = 0.5 * (pos_red[1] - a*pos_red[0] + pos_green[1]- a*pos_green[0])

	points = [(0, f_linear(0,a,b)), (display_width, f_linear(display_width,a,b))]

	pygame.draw.line(display_window, black, points[0], points[1])
	pygame.display.flip()

	time.sleep(2)

pygame.quit()
