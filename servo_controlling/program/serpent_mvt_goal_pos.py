# -*- coding: utf-8 -*-

"""
Programme démonstrateur permmettant de déplacer le robot serpent (avancer,
reculer et tourner).
Controle interactif par les flèches directionnelles du clavier.
"""

from time        import time, sleep
from math        import cos, sin, pi, atan
from pydynamixel import dynamixel, chain, registers

import pygame
from pygame.locals import *
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 30)
fenetre = pygame.display.set_mode((640, 480))

def multi_set_status_return(ser, servo_id, reg_value, t_init_sleep=0.1, t_sleep=0.05):
    """
    Set status_return mode of the servos.

    :param ser: The ``serial`` port to use.
    :param servo_id: the list of servo IDs.
    :param reg_value: value to write in STATUS_RETURN_LEVEL register (cf registers.py).
    :param t_init_sleep: pause time before start change reg values.
    :param t_sleep: pause time between settings in each servo.

    If status_return disable => return nothing when new set
    If status_return enable  => return status packet when new set
    """
    n_servo  = len(servo_id)
    reg_addr = registers.STATUS_RETURN_LEVEL
    if   (reg_value == registers.STATUS_RETURN.RETURN_FOR_ALL_PACKETS):
        wait_response = False
    elif (reg_value == registers.STATUS_RETURN.RETURN_ONLY_FOR_READ):
        wait_response = True
    else:
        raise ValueError("Incorrect value for reg_value")

    sleep(t_init_sleep)
    for n in range(n_servo):
        dynamixel.set_reg_1b( ser, servo_id[n], reg_addr, reg_value, wait_response )
        print('Reg @{} set successfully at {} !'.format(reg_addr, reg_value) )
        sleep(t_sleep)

def multi_set_velocity(ser, servo_id, v, t_init_sleep=0.1, t_sleep=0.05):
    """
    Set velocity of the servos. Need status return enable

    :param ser: The ``serial`` port to use.
    :param servo_id: the list of servo IDs.
    :param v: value of velocity to set.
              v can be a value or a list.
    :param t_init_sleep: pause time before start change reg values.
    :param t_sleep: pause time between settings in each servo.
    """
    n_servo = len(servo_id)

    if   (type(v) == int):
        velocity = [ v for i in range(n_servo) ]
    elif (type(v) == list):
        if (len(v) == n_servo):
            raise ValueError("lenght servo_id and lenght v are not equal")
        velocity = v
    else:
        raise TypeError("v need to be an int or a list")

    sleep(t_init_sleep)
    for n in range(n_servo):
        dynamixel.set_velocity(ser, servo_id[n] , velocity[n])
        sleep(t_sleep)

def multi_init_pos(t_final_sleep=2, t_sleep=0.05):
    """
    Initialize snake position

    :param t_init_sleep: pause time before start change goal position values.
    :param t_sleep: pause time between goal position settings in each servo.
    """
    # init goal position vector
    global goal_pos_vect
    goal_pos_vect = [ int( round( offset + amplitude_norm * sin( omega*n ) ) )    for n in range(n_servo) ]
    # Angle safe check (can slow execution)
    assert abs(max(goal_pos_vect)-offset) < 1024./300.*ANGLE_MAX , "Angle max (={}°) dépassé".format(ANGLE_MAX)

    for n in range(n_servo):
        sleep(t_sleep)
        dynamixel.set_position( ser, servo_id[n], goal_pos_vect[n] )

    sleep(t_final_sleep)


############################

# You'll need to change this to the serial port of your USB2Dynamixel
serial_port = '/dev/ttyUSB0'
ser         = dynamixel.get_serial_for_url(serial_port)
# ser = dynamixel.get_serial_for_com(serial_port)    # DEBUG DEBUG


servo_id    = [1,2,3,4,5,6,7,8,9,10,11,12]

## Config servos movement ##
tick_period = 0.01              # Prediode de chaque instruction
sleep_time  = tick_period/10    # si utilisé, permet de réduire l'utilisation des
                                # ressources de la machine, mais ticks moins précis
resolution  = 300     # nombre de tick pour une période de la pos angu d'un servo
#Augmenter le resolution = ralentir

## Config snake waveform  ##
n_period    = 1     # nombre de "période" de l'ondulation du serpent
amplitude   = 300     # amplitude de l'ondulation du serpent  < 500
ANGLE_MAX   = 120     # angle crete crete max
turnOffset  = 0

############################

move    = 0
offset  = 512+turnOffset
n_servo = len(servo_id)

# pré-calculs
mvt_speed      = 2 * pi * 1./resolution
amplitude_norm = amplitude * (float(n_period)/n_servo) * 1024./300.
omega          = 2 * pi * n_period/float(n_servo)





# enable write response for all instructions ()
multi_set_status_return(ser, servo_id, registers.STATUS_RETURN.RETURN_FOR_ALL_PACKETS)

# Set velocity for init
multi_set_velocity(ser,servo_id, 200)

# Move the snake in init position
multi_init_pos()

# Set velocity for movement
multi_set_velocity(ser,servo_id, 400)

# disable write response for read instructions
multi_set_status_return(ser, servo_id, registers.STATUS_RETURN.RETURN_ONLY_FOR_READ)

# TEST BLOCAGE
servo_bloque = 3
angle_bloque = 300
sleep(0.5)
dynamixel.set_position_no_response( ser, servo_bloque , angle_bloque )
sleep(0.5)

t = time()
tick = 0
nb_tick = 10000
for i in range(1,nb_tick):
    tick += move
    for n in range(n_servo):

        # TEST BLOCAGE
        if ( servo_id[n] == servo_bloque):
            continue

        # dynamixel.set_position( ser, servo_id[n], goal_pos_vect[n] )
        dynamixel.set_position_no_response( ser, servo_id[n], goal_pos_vect[n] )

        print "    ", time()-t  # DEBUG
    #dynamixel.send_action_packet( ser )
    print "  ", time()-t        # DEBUG

    # compute next goal position vector
    goal_pos_vect = [ int( round( offset + amplitude_norm * sin( omega*n + tick*mvt_speed ) ) )    for n in range(n_servo) ]
    # ne pas recréer la liste mais réécrire dedans pour opti ???

    # Angle safe check (can slow execution)
    assert abs(max(goal_pos_vect)-offset) < 1024./300.*ANGLE_MAX , "Angle max (={}°) dépassé".format(ANGLE_MAX)

    # Gestion control serpent
    for event in pygame.event.get():    #Attente des événements
        # if event.type == QUIT:
        #     continuer = 0

        if (event.type == KEYDOWN):
            if   (event.key == K_UP   ):
                move = min( move+1, 1)
            elif (event.key == K_DOWN ):
                move = max( move-1, -1)
            elif (event.key == K_LEFT ):
                if (offset > 460):
                    offset -= 5
            elif (event.key == K_RIGHT):
                if (offset < 564):
                    offset += 5

    textsurface = myfont.render("OFFSET = {}          ".format(offset), False, (255, 255, 255), (0,0,0) )
    fenetre.blit(textsurface,(0,0))

    if   (move== 0):
        textsurface = myfont.render("DON'T MOVE           ", False, (255, 255, 255), (0,0,0) )
    elif (move== 1):
        textsurface = myfont.render("MOVE FORWARD         ", False, (255, 255, 255), (0,0,0) )
    elif (move==-1):
        textsurface = myfont.render("MOVE BACKWARD        ", False, (255, 255, 255), (0,0,0) )

    fenetre.blit(textsurface,(0,30))
    pygame.display.flip()


    # Wait next tick
    while( time() < t+i*tick_period ):    # tick => i
        pass
        #if ( tick%10 == 0 ):    #



        #sleep(sleep_time)   # utile si tick_period>0.001 ?
    print( time()-t )  # DEBUG

print('Success!')
