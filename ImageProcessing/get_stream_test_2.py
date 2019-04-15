# -*- coding: utf-8 -*-

import pygame
import pygame.camera
import pygame.camera.Capture

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
