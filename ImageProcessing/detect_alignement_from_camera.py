# -*- coding: utf-8 -*-

"""
Ce programme permet de recuperer une image grace a la webcam.
Recuperre ensuite les references de rouge et de vert dans le coins superieurs droits et gauche.
Trouve les points correspondant au meme rouge et au meme vert.
Determine la droite passant par ces points.
"""

import readchar
import time
import pygame
import pygame.camera
import pygame.transform
import numpy as np
import pygame.surfarray
import matplotlib.pyplot as plt
from random import *
from statistics import mean
from termcolor import colored

DEBUG = True
white = 0xffffff; red = 0xff5f5f; green = 0x4eb7a6; blue = 0x0000ff; black = 0x000000

# Functions

def f_linear(x, a, b):
    return (int(a * x + b))

def draw_linear(a, b,color, display_width, display_window):
	points = [(0, f_linear(0, a, b)), (display_width, f_linear(display_width, a, b))]

	pygame.draw.line(display_window, color, points[0], points[1])
	pygame.display.flip()

def random_color(max=255):
    return (randint(0, max), randint(0, max), randint(0, max))


def draw_target(distance_to_go, red_pos, green_pos, display_window, head_color=green, radius=10, color = blue, width = 1):
	if head_color == green :
		vect_directeur = np.subtract(green_pos, red_pos)
	elif head_color == red:
		vect_directeur = np.subtract(red_pos, green_pos)
	else :
		return(0,0)
	print(vect_directeur)

	norm = np.sqrt(float(vect_directeur[0]*vect_directeur[0] + vect_directeur[1] * vect_directeur[1]))

	center = vect_directeur/ norm * distance_to_go + green_pos
	center = center.astype(int)

	pygame.draw.circle(display_window, color, center, radius, width)
	pygame.draw.circle(display_window, color, center, radius+20, width)
	pygame.draw.circle(display_window, color, center, radius+40, width)
	pygame.display.flip()

	return (vect_directeur)


## Init

sensibility = (20, 20, 20)
exit = False;get_color = False
a = 0; b = 0;
target_pos = (0,0)

display_width = 1280; display_height = 720

pygame.init()
pygame.camera.init()

display_window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('window')

## Code

## Recuperation de l'image


camlist = pygame.camera.list_cameras()
# print(str(camlist));
if camlist:
    cam = pygame.camera.Camera(camlist[0], (1280, 720))
else:
    cam = pygame.camera.Camera("/dev/video0", (640, 480))

cam.start()
running = True; set_ref = True; display_target = False;
acquisition_time = []
process_time = []

while running:
	t1 = time.time();

	img = cam.get_image(); t2 = time.time(); acquisition_time.append(t2-t1);
	img = pygame.transform.scale(img, (display_width, display_height))
	#pygame.image.save(img, "image.jpg")
	display_window.blit(img, (0, 0))
	pygame.display.flip()

	"""Getting the red and green references"""
	if get_color == True:
		green = display_window.get_at((0, 0));
		red = display_window.get_at((0, display_height - 10));

		if(DEBUG): print(colored("green :", "green") + str(green) + colored(",red :", "red") + str(red))

		# Removing the references from the image
		# display_window.blit(img, (-30,0)) #Move image to the left
		pygame.draw.polygon(display_window, blue, [(0, 0), (30, 0), (30, 30), (0, 30)])
		pygame.draw.polygon(display_window, blue, [(0, display_height - 1), (30, display_height - 1), (30, display_height - 31),
(0, display_height - 31)])

	"""Getting the location of red and green pixels"""
	mask_red = pygame.mask.from_threshold(display_window, red, sensibility)
	mask_green = pygame.mask.from_threshold(display_window, green, sensibility)

	pos_red = mask_red.centroid()
	pos_green = mask_green.centroid()

	if (pos_red == (0, 0)):
		print("Impossible de trouver des pixels", colored("rouges", "red"))
		process_points = False

	else:
		if(DEBUG): print("Centre des pixels", colored("rouges", "red"), " : ", str(pos_red))
		pygame.draw.circle(display_window, red, pos_red, 10)
		process_points = True

	if (pos_green == (0, 0)):
		print("Impossible de trouver des pixels", colored("verts", "green"))
		process_points =False
	else:
		if(DEBUG): print("Centre des pixels ", colored("verts", "green"), " : ", str(pos_green))
		pygame.draw.circle(display_window, green, pos_green, 10)

	if process_points == True:
		# Evaluation de la droite entre les 2 points : y = ax + b
		a = (pos_green[1] - pos_red[1]) / (pos_green[0] - pos_red[0])
		b = 0.5 * (pos_red[1] - a * pos_red[0] + pos_green[1] - a * pos_green[0])

		draw_linear(a, b,black, display_width, display_window)

	#Draw the reference ine in white
	if set_ref == True :
		a_ref, b_ref = a , b
		green_ref, red_ref = pos_green, pos_red
		set_ref = False

	#Draw ref
	draw_linear(a_ref, b_ref, white, display_width, display_window)
	draw_target(850, red_ref, green_ref, display_window, head_color=green, radius=10)

	t2 = time.time();
	process_time.append(t2 - t1)
	if(DEBUG): print("Process time = " + str(t2 - t1))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_d:
				print(colored("Changement de ref", "blue"))
				set_ref = True
			"""
			if event.key == pygame.K_f:
				print(colored("Defining target position", "blue"))
				set_target
			"""

pygame.quit()

display_time_hist = ' '
while (display_time_hist != 'Y' and display_time_hist != 'N'):
	print("Voulez-vous afficher l'histogramme des temps de communication avec l'appareil photo? [Y/N]")
	display_time_hist = readchar.readchar()
	print(display_time_hist)
if display_time_hist == 'Y':
	fig = plt.figure()
	plt.hist(process_time,20)
	plt.hist(acquisition_time,20)
	plt.show()
