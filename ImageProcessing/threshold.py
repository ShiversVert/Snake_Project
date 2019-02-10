import pygame, time
import pygame.camera
import pygame.transform

#init

pygame.init()
pygame.camera.init()

display_width = 640
display_height = 480

red = (255,0,0)
dark_red = (177, 45, 41)
white = (255,255,255)
sensibility = (40,20,20)

going = True

display_window = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('window')

## Code

camlist = pygame.camera.list_cameras()
cam = pygame.camera.Camera(camlist[len(camlist)-1],(640,480))
cam.start()

image = cam.get_image()
pygame.image.save(image,"image.jpg")
display_window.blit(image, (0,0))
pygame.display.flip()


print(pygame.transform.threshold(display_window, display_window, dark_red, sensibility, set_color = white, inverse_set = False) )

pygame.image.save(display_window,"image_transformed.jpg")
time.sleep(2)
pygame.display.flip()


time.sleep(2)
"""
while True:
	image = cam.get_image()
	display_window.blit(image, (0,0))
	pygame.image.save(img,"image.jpg")

	display_window.flip()
	pygame.transform.threshold(display_window, display_window,red)
"""