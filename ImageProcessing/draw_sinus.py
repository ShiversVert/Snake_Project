# -*- coding: utf-8 -*-

import time
import pygame
#import pygame.camera
import pygame.transform
import numpy as np
import pygame.surfarray
from random import *

"""
	nb_points 	Nombre de points de la sinus
	nb_periode	Nombre de periode du sinus a afficher
	duree		Nombre pixel sur lequel le sinus est affiche
	amplitude	Amplitude du sinus en pixel
	surface		Surface ou afficher le sinus
	x 			Coordonee x ou afficher le sinus dans la surface
	y      		Coordonee y ou afficher le sinus dans la surface
"""
def generate_sinus(nb_points, nb_periode, duree, amplitude, surface, x, y, angle = 0):
	points=[]
	pas_x = duree/nb_points;

	for i in range(nb_points):
		x_sin = x + i * pas_x
		y_sin = y + amplitude * np.sin(duree/nb_periode *  x_sin)
		points.append((x_sin, y_sin))


	for i in range(nb_points - 1):
		pygame.draw.line(display_window, black, points[i], points[i+1])


	pygame.display.flip()
	return 0

## Init
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)
sensibility = (15,15,15)

display_width = 900
display_height = 600

display_window = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('window')
display_window.fill(white)


generate_sinus(40, 1, 400, 200, display_window, 200, 300)
time.sleep(2)

pygame.quit()
