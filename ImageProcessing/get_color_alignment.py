import time
import pygame 
import pygame.camera
import pygame.transform
import numpy as np
import pygame.surfarray
from statistics import mean

## Fucntions

def f_linear(x, a, b):
	return(int(a*x + b))

## Init
white = (255,255,255)
white_array = np.array([255,255,255])
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)
sensibility = (15,15,15)

pygame.init()
pygame.camera.init()

display_width = 640
display_height = 400

image = pygame.image.load("test_color_line.jpg")

display_window = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('window')

## Code

display_window.blit(image, (0,0))
pygame.display.flip()

## Traitement pour le rouge

#print("Nombre de rouge : " + str(pygame.transform.threshold(display_window, display_window, red, sensibility, set_color = white, inverse_set = False) ))
#pygame.display.flip()

mask_red = pygame.mask.from_threshold(display_window, red, sensibility)
mask_green = pygame.mask.from_threshold(display_window, green, sensibility)

pos_red = mask_red.centroid()
pos_green = mask_green.centroid()

#print("taille du masque : " + str(mask.get_size()))
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