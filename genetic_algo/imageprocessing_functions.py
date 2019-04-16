# -*- coding: utf-8 -*-

"""
Ce programme permet de recuperer une image grace a la webcam.
Recuperre ensuite les references de rouge et de vert dans le coins superieurs droits et gauche.
Trouve les points correspondant au meme rouge et au meme vert.
Determine la droite passant par ces points.
"""

import time
import sys
import pygame
import pygame.camera
import pygame.transform
import numpy as np
import pygame.surfarray
import matplotlib.pyplot as plt
from random import *
from math import *

DEBUG = True
white = 0xffffff; red = 0xff5f5f; green = 0x42ecec; blue = 0x0000ff; black = 0x000000

# Functions

def f_linear(x, a, b):
    return (int(a * x + b))

def draw_linear(a, b,color, display_width, display_window):
	points = [(0, f_linear(0, a, b)), (display_width, f_linear(display_width, a, b))]

	pygame.draw.line(display_window, color, points[0], points[1])
	pygame.display.flip()

def draw_target(target_coordinates, display_window, head_color=green, radius=10, color = blue, width = 1):
	print(target_coordinates)
	print(display_window.get_width)
	print(display_window.get_height)
	pygame.draw.circle(display_window, color, target_coordinates, radius, width)
	pygame.draw.circle(display_window, color, target_coordinates, radius+20, width)
	pygame.draw.circle(display_window, color, target_coordinates, radius+40, width)
	pygame.display.flip()

"""
Initiate image processing and return the display window
"""

def initImage():
	pygame.init()
	pygame.camera.init()

	display_width, display_height = 1280, 720
	display_window = pygame.display.set_mode((display_width, display_height))
	pygame.display.set_caption('Genetic algorithm v1')

	camlist = pygame.camera.list_cameras()

	if camlist:
	    cam = pygame.camera.Camera(camlist[0], (1280, 720))
	else:
	    cam = pygame.camera.Camera("/dev/video0", (640, 480))

	cam.start()

	return(display_window, display_width, display_height, cam)


def getTargetLocation(display_window, sensibility, cam,display_width, display_height, pixel_distance_to_go = 850, head_color=green, green = green, red = red):
	#Get image and displays it
	target_of_sight = True
	
	while(target_of_sight):
		img = cam.get_image()
		img = pygame.transform.scale(img, (display_width, display_height))
		display_window.blit(img, (0, 0))
		pygame.display.flip()


		#Detect green and red on the image
		mask_red = pygame.mask.from_threshold(display_window, red, sensibility)
		mask_green = pygame.mask.from_threshold(display_window, green, sensibility)

		#Get their center of mass
		pos_red = mask_red.centroid()
		pos_green = mask_green.centroid()
	
		while (pos_red == (0,0)):
			print("Impossible de detecter des pixels rouges\n Replacez le serpent et appuyez sur entrée")
			raw_input()	
			img = cam.get_image()
			img = pygame.transform.scale(img, (display_width, display_height))
			display_window.blit(img, (0, 0))
			pygame.display.flip()

			mask_red = pygame.mask.from_threshold(display_window, red, sensibility)
			pos_red = mask_red.centroid()

		while (pos_green == (0,0)):
			print("Impossible de detecter des pixels verts\n Replacez le serpent et appuyez sur entrée")
			raw_input()	
			img = cam.get_image()
			img = pygame.transform.scale(img, (display_width, display_height))
			display_window.blit(img, (0, 0))
			pygame.display.flip()

			mask_green = pygame.mask.from_threshold(display_window, green, sensibility)
			pos_green = mask_green.centroid()

		#CAlcul of target
		if(pos_green[0] == pos_red[0]):
			a = pos_green[1] - pos_red[1]
		else:
			a = (pos_green[1] - pos_red[1]) / (pos_green[0] - pos_red[0])
		
		b = 0.5 * (pos_red[1] - a * pos_red[0] + pos_green[1] - a * pos_green[0])

		if head_color == green :
			vect_directeur = np.subtract(pos_green, pos_red)
		elif head_color == red:
			vect_directeur = np.subtract(pos_red, pos_green)
		else :
			return(0,0)

		norm = np.sqrt(float(vect_directeur[0]*vect_directeur[0] + vect_directeur[1] * vect_directeur[1]))

		target_coordinates = vect_directeur/ norm * pixel_distance_to_go + pos_green
		target_coordinates = target_coordinates.astype(int)

		if (target_coordinates[0]>display_width or target_coordinates[0] < 0 or target_coordinates[1]>display_height or target_coordinates[1] < 0):
			print("La cible est hors de l'ecran, repositionnez le serpent et appuyez sur entrée")
			raw_input()
		else:
			target_of_sight = False

		draw_linear(a, b, 0xffffff, display_width, display_window)
		draw_target(target_coordinates, display_window)
	return(a, b, target_coordinates)

def getScore(target, a, b,sensibility, display_window, cam,display_width, display_height, head_color = green):
	
	img = cam.get_image()
	img = pygame.transform.scale(img, (display_width, display_height))
	display_window.blit(img, (0, 0))
	pygame.display.flip()

	mask_head = pygame.mask.from_threshold(display_window, head_color, sensibility)
	#Get the center of mass of the head
	pos_head = mask_head.centroid()

	#Coefficent of ponderation of the ellipsis
	alpha = 1.5

	if(pos_head == (0,0)):
		return(maxint) #If head is not detected

	if((a == 0) and (b == 0)):
		return(maxint) #If head is on tail
	else:
		if(a == 0):
			if(b<0):
				theta = -(pi)/2
			else:
				theta = pi/2
		else:
			theta = atan(b/a) #Keep it in radian

		#a and b are normalized for the calculus
		a_norm = a/(np.sqrt(float (a**2 + b**2)))
		b_norm = b/(np.sqrt(float (a**2 + b**2)))

		S = sin(theta)
		C = cos(theta)
		T0 = target[0]
		T1 = target[1]
		P0 = pos_head[0]
		P1 = pos_head[1]
		alpha = 10

		score = np.sqrt(float( ((P0-T0)*C+(P1-T1)*S)**2 + alpha*((P0-T0)*S-(P1-T1)*C)**2))

        #distance_to_go = np.sqrt(float( (target[0]-pos_head[0])**2 + (target[1]-pos_head[1])**2) )
        #score = np.sqrt(float( (pos_head[0]*cos(theta) + pos_head[1]*sin(theta) - distance_to_go)**2 + alpha*(-pos_head[0]*sin(theta) + pos_head[1]*cos(theta)**2) ))
        #Check le - devant le x dans la deuxie partie

		#print("Valeur du score : ", score)
		return(score)

	return(maxint)
