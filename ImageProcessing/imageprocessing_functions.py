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
white = 0xffffff; red = 0xff5f5f; green = 0x4eb7a6; blue = 0x0000ff; black = 0x000000

# Functions

def f_linear(x, a, b):
    return (int(a * x + b))

def draw_linear(a, b,color, display_width, display_window):
	points = [(0, f_linear(0, a, b)), (display_width, f_linear(display_width, a, b))]

	pygame.draw.line(display_window, color, points[0], points[1])
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
	    cam = pygame.camera.Camera(camlist[1], (1280, 720))
	else:
	    cam = pygame.camera.Camera("/dev/video0", (640, 480))

	cam.start()

	return(display_window, display_width, display_height)


def getTargetLocation(display_window, sensibility, pixel_distance_to_go = 300, head_color=green, green = green, red = red):
	#Get image and displays it
	img = cam.get_image();
	img = pygame.transform.scale(img, (display_width, display_height))
	display_window.blit(img, (0, 0))
	pygame.display.flip()


	#Detect green and red on the image
	mask_red = pygame.mask.from_threshold(display_window, red, sensibility)
	mask_green = pygame.mask.from_threshold(display_window, green, sensibility)

	#Get their center of mass
	pos_red = mask_red.centroid()
	pos_green = mask_green.centroid()

	while (pos_red == (0,0)){
		print("Impossible de detecter des pixels rouges\n Replacez le serpent et appuyez sur entrée")
		input()
		pos_red = mask_red.centroid()
	}
	while (pos_green == (0,0)){
		print("Impossible de detecter des pixels rouges\n Replacez le serpent et appuyez sur entrée")
		intput()
		pos_green = mask_green.centroid()
	}

	a = (pos_green[1] - pos_red[1]) / (pos_green[0] - pos_red[0])
	b = 0.5 * (pos_red[1] - a * pos_red[0] + pos_green[1] - a * pos_green[0])

	if head_color == green :
		vect_directeur = np.subtract(green_pos, red_pos)
	elif head_color == red:
		vect_directeur = np.subtract(red_pos, green_pos)
	else :
		return(0,0)

	norm = np.sqrt(float(vect_directeur[0]*vect_directeur[0] + vect_directeur[1] * vect_directeur[1]))

	target_coordinates = vect_directeur/ norm * distance_to_go + green_pos
	target_coordinates = center.astype(int)

	return(a, b, center)

def getScore(target, a, b, display_window, head_color = green):
	img = cam.get_image();
	img = pygame.transform.scale(img, (display_width, display_height))
	display_window.blit(img, (0, 0))
	pygame.display.flip()

	mask_head = pygame.mask.from_threshold(display_window, head_color, sensibility)
	#Get the center of mass of the head
	pos_head = mask_head.centroid()

    #Coefficent of ponderation of the ellipsis
    alpha = 1.5

	if(pos_head == (0,0)):
		return(sys.maxint) #If head is not detected
	else
	   if(a == 0):
           if(b<0):
                theta = -(math.pi)/2
           else
                theta = math.pi/2
        else
            theta = atan(b/a) #Keep it in radian
        #a and b are normalized for the calculus
        a_norm = a/(np.sqrt(float (a**2 + b**2)))
        b_norm = b/(np.sqrt(float (a**2 + b**2)))

        distance_to_go = np.sqrt(float( (target[0]-a_norm)**2 + (target[1]-b_norm)**2) )
        score = np.sqrt(float( (pos_head[0]*cos(theta) + pos_head[1]*sin(theta) - distance_to_go)**2 + alpha*(-pos_head[0]*sin(theta) + pos_head[1]*cos(theta)**2) ))
        #Check le - devant le x dans la deuxie partie

        print("Valeur du score : ", score)
        return(score)

    return(sys.maxint) #Security return : does not consider this try
