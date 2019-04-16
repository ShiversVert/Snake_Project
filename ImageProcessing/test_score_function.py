# -*- coding: utf-8 -*-

"""
Ce programme permet de recuperer une image grace a la webcam.
Recuperre ensuite les references de rouge et de vert dans le coins superieurs droits et gauche.
Trouve les points correspondant au meme rouge et au meme vert.
Determine la droite passant par ces points.
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import *


# Functions

def getScore(target, a_ref, b_ref, x_head, y_head):
	maxint = 1000
	pos_head = (x_head, y_head)

	#Coefficent of ponderation of the ellipsis
	alpha = 1.5

	if(pos_head == (0,0)):
		return(sys.maxint) #If head is not detected

	if((a == 0) and (b == 0)):
		return(sys.maxint) #If head is on tail
	else:
		if(a == 0):
			if(b<0):
				theta = -(math.pi)/2
			else:
				theta = math.pi/2
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

		score = np.sqrt(float( (T0*C-T1*S-P0*C+P1*S)**2 + alpha*((T0*S+T1*C-P0*S-P1*C)**2) ))

        #distance_to_go = np.sqrt(float( (target[0]-pos_head[0])**2 + (target[1]-pos_head[1])**2) )
        #score = np.sqrt(float( (pos_head[0]*cos(theta) + pos_head[1]*sin(theta) - distance_to_go)**2 + alpha*(-pos_head[0]*sin(theta) + pos_head[1]*cos(theta)**2) ))
        #Check le - devant le x dans la deuxie partie

		print("Valeur du score : ", score)
		return(score)

	return(maxint)

## Init

sensibility = (20, 20, 20)
exit = False;get_color = False
display_width = 1000; display_height = 1000

a = display_width/display_height; b = 0;
target_pos = (display_width/2, display_height/2)
score = np.zeros((display_width, display_height))

x = np.linspace(0, display_width-1, display_width)
y = np.linspace(0, display_height-1, display_height)
X,Y = np.meshgrid(x,y)
for i in range(display_width):
	for j in range(display_height):
		score[i][j] = getScore(target_pos, a, b, i, j)

print("calcul ok")
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_wireframe(X, Y, score)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('Score');
plt.show()
