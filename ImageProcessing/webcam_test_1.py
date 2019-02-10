import pygame
import pygame.camera

pygame.init()
pygame.camera.init()

## Init

display_width = 640
display_height = 480

black = (0,0,0)
white = (255,255,255)

## Recuperation de l'image 

camlist = pygame.camera.list_cameras()
if camlist:
    cam = pygame.camera.Camera(camlist[0],(640,480))
else :
	cam = pygame.camera.Camera("/dev/video0",(640,480))

cam.start()
img = cam.get_image()
pygame.image.save(img,"image.jpg")

## Affichage

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Capture')

clock = pygame.time.Clock()
crashed = False

image_loaded = pygame.image.load('image.jpg')
#gameDisplay.blit(image_loaded, (0,0))
gameDisplay.blit(img, (0,0))

while not crashed:
    img = cam.get_image()

    pygame.display.update()
    clock.tick(100)

pygame.quit()
quit()


