# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 16:52:38 2019

@author: Colin
"""

"""
    WARNING : in python 2, 5/2 = 2    =>   float(5)/2 = 2.5
"""

from turtle import *
from math   import cos, sin, pi, atan
from time   import sleep

# window config
reset()
setup(800, 0.3, 0, 0)


# setup turtle speed
hideturtle()
speed(0)
delay(0)

# config snake
n_period  = 1
n_servo   = 12
mvt_speed = 0.05    ## C'EST LA RESOLUTION EN FAIT ?????
amplitude = 400
turnOffset = 50

# config draw
len_servo = 200 *(float(n_period)/n_servo)


for i in range(200):

    # create angle goal vector
    l_angle = [turnOffset+amplitude * float(n_period)/n_servo * cos( 2*pi*(id_servo*n_period)/float(n_servo) + i*mvt_speed )     for id_servo in range(n_servo)]
    #          |             amplitude               |
    # print l_angle
    ############ find start_angle #############
    penup()

    setheading(0)
    start = pos()
    for angle in l_angle:
        forward(len_servo)
        right(angle)
    forward(len_servo)
    stop = pos()
    start_angle = atan( float(stop[1]-start[1])/(stop[0]-start[0]) )
    ############## end find #################

    # setup new draw
    clear()
    goto( -300, 0 )
    pendown()
    setheading( - 180/pi * start_angle )

    # drawing
    for angle in l_angle:
        forward(len_servo)
        right(angle)
        dot()
    forward(len_servo)


    sleep(0.1)

    """ NOTE 2 solution :

        1) tout les temps T:    ici dépend princ. de sleep(x)
            set goal pos de chaque servo (avec formule l_angle)
            send_action (à vitesse max ou opti pour non de vibration)

            => problème vibration ! MAIS si T très petit, peut etre que ça passe


        2) tout les temps T:
            get pos
            calculer next_wanted_pos (avec formule l_angle)
            => set velocity ( v = angle_à_parcourir/T)  SERVO_SPEED

            => if (pos < next_wanted_pos) set goal_pos to MAX_ANGLE
               else   set goal_pos to MIN_ANGLE

    """


print("OK")

mainloop()
