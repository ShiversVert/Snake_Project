import time
import pygame 
import pygame.camera
import pygame.transform
import numpy as np
import pygame.surfarray
from random import *
from statistics import mean
from termcolor import colored

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

white = (255,255,255)
white_array = np.array([255,255,255])
red = 0xbd4b62
green = 0xb2c631
black = (0,0,0)
sensibility = (30,30,30)
exit = False

display_width = 640
display_height = 480

pygame.init()
pygame.camera.init()

display_window = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('window')

## Code

## Recuperation de l'image 


camlist = pygame.camera.list_cameras()
if camlist:
    cam = pygame.camera.Camera(camlist[2],(640,480))
else :
	cam = pygame.camera.Camera("/dev/video0",(640,480))

cam.start()
img = cam.get_image()
pygame.image.save(img,"image.jpg")
display_window.blit(img, (0,0))
pygame.display.flip()

mask_red = pygame.mask.from_threshold(display_window, red, sensibility)
mask_green = pygame.mask.from_threshold(display_window, green, sensibility)

pos_red = mask_red.centroid()
pos_green = mask_green.centroid()

if(pos_red == (0,0)):
	print("Impossible de trouver des pixels", colored("rouges","red"))
	exit = True
else:
	print("Centre des pixels", colored("rouges","red"), " : ", str(pos_red))

if(pos_green == (0,0)):
	print("Impossible de trouver des pixels", colored("verts","green"))
	exit = True
else : 
	print("Centre des pixels ", colored("verts","green"), " : " , str(pos_green))

if exit == False : 

	#Evaluation de la droite entre les 2 points : y = ax + b
	a = (pos_green[1] - pos_red[1]) / (pos_green[0]-pos_red[0])
	b = 0.5 * (pos_red[1] - a*pos_red[0] + pos_green[1]- a*pos_green[0])

	points = [(0, f_linear(0,a,b)), (display_width, f_linear(display_width,a,b))]

	pygame.draw.line(display_window, black, points[0], points[1])
	pygame.display.flip()

time.sleep(2)

pygame.quit()