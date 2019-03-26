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


# Fucntions

def f_linear(x, a, b):
    return (int(a * x + b))

def draw_linear(a, b,color, display_width, display_window):
	points = [(0, f_linear(0, a, b)), (display_width, f_linear(display_width, a, b))]

	pygame.draw.line(display_window, color, points[0], points[1])
	pygame.display.flip()


def generate_random_point(surface, color, radius, min_radius=5):
	radius = randint(min_radius, radius)
	x = randint(0, surface.get_width())
	y = randint(0, surface.get_height())

	pygame.draw.circle(surface, color, (x, y), radius)
	pygame.display.flip()
	return (0)


def generate_random_polygon(surface, color, size=40, max_sides=15):
    side_number = randint(3, max_sides)
    # "center" of the polygon
    x = randint(0, surface.get_width())
    y = randint(0, surface.get_height())
    vertices = []

    for i in range(side_number):
        vertices.append(((x + randint(-size, size)), (y + randint(-size, size))))

    pygame.draw.polygon(surface, color, vertices)
    pygame.display.flip()
    return (0)


def random_color(max=255):
    return (randint(0, max), randint(0, max), randint(0, max))


def draw_target(distance_to_go, red_pos, green_pos, head_color="red", radius=10):
    return 0


## Init

white = 0xffffff
red = 0xff5f5f
green = 0x4eb7a6
blue = 0x0000ff
black = (0, 0, 0)
sensibility = (20, 20, 20)
exit = False

display_width = 1280
display_height = 720

get_color = False

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
running = True; set_ref = True;
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

		print(colored("green :", "green") + str(green) + colored(",red :", "red") + str(red))

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
		process_points = True
	else:
		print("Centre des pixels", colored("rouges", "red"), " : ", str(pos_red))
		pygame.draw.circle(display_window, red, pos_red, 10)
		process_points = False

	if (pos_green == (0, 0)):
		print("Impossible de trouver des pixels", colored("verts", "green"))
		process_points = True
	else:
		print("Centre des pixels ", colored("verts", "green"), " : ", str(pos_green))
		pygame.draw.circle(display_window, green, pos_green, 10)
		process_points = False

	if process_points == False:
		# Evaluation de la droite entre les 2 points : y = ax + b
		a = (pos_green[1] - pos_red[1]) / (pos_green[0] - pos_red[0])
		b = 0.5 * (pos_red[1] - a * pos_red[0] + pos_green[1] - a * pos_green[0])

		draw_linear(a, b,black, display_width, display_window)

	#Draw the reference ine in white
	if set_ref == True : 
		a_ref, b_ref = a , b
		set_ref = False
	#Draw ref
	draw_linear(a_ref, b_ref, white, display_width, display_window)	

	t2 = time.time();
	process_time.append(t2 - t1)
	print("Process time = " + str(t2 - t1))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_d:
				print(colored("Changement de ref", "blue"))
				set_ref = True


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
