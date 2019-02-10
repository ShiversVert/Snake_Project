import time
import pygame 
import pygame.camera
import pygame.transform
import numpy as np
import pygame.surfarray

## Init
white = (255,255,255)
white_array = np.array([255,255,255])
red = (255,0,0)
green = (0,255,0)
sensibility = (10,5,5)

pygame.init()
pygame.camera.init()

display_width = 640
display_height = 480

image = pygame.image.load("test_color_line.jpg")

display_window = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('window')

## Code

display_window.blit(image, (0,0))
pygame.display.flip()

## Traitement pour le rouge

print("Nombre de rouge : " + str(pygame.transform.threshold(display_window, display_window, red, sensibility, set_color = white, inverse_set = False) ))
pygame.display.flip()

image_array =  pygame.surfarray.array3d(display_window)
size_image_array = np.shape(image_array);

x_green = []; y_green = [];
x_red = []; y_red = [];

for x in range(size_image_array[0]):
	for y in range(size_image_array[1]):
		
		if (np.array_equal(image_array[x,y], white_array) == False) :
			x_red.append(x)
			y_red.append(y)
		

## Traitement pour le ver

display_window.blit(image, (0,0))
pygame.display.flip()

print("Nombre de vert : " + str(pygame.transform.threshold(display_window, display_window, green, sensibility, set_color = white, inverse_set = False) ))
pygame.display.flip()

for x in range(size_image_array[0]):
	for y in range(size_image_array[1]):
		if (np.array_equal(image_array[x,y], white_array) == False):
			x_green.append(x)
			y_green.append(y)

mean_x_green = mean(x_green)
mean_y_green = mean(y_green)
mean_x_red = mean(x_red)
mean_y_red = mean(y_red)

print("Vert : (" + mean_x_green)

"""
 , " , " mean_y_green , ") Rouge : " , mean_x_red , " , " mean_y_red , " ]"
"""


