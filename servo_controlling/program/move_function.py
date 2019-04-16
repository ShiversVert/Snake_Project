# -*- coding: utf-8 -*-

from time        import time, sleep
from math        import cos, sin, pi, atan
from pydynamixel import dynamixel, chain, registers


import pygame
from pygame.locals import *
"""
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 30)
fenetre = pygame.display.set_mode((640, 480))
"""

global ANGLE_MAX
ANGLE_MAX = 120


def multi_set_status_return(ser, servo_id, reg_value, t_init_sleep=0.1, t_sleep=0.05):
    """
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
        #print('Reg @{} set successfully at {} !'.format(reg_addr, reg_value) )
        sleep(t_sleep)

def multi_set_velocity(ser, servo_id, v, t_init_sleep=0.1, t_sleep=0.05):
    """
    need status return enable

    v can be a value or a list
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


def init_snake(serial_port   = '/dev/ttyUSB0',
               servo_id      = [1,2,3,4,5,6,7,8,9,10,11,12],
               n_period      = 1,

               id_bloque     = 0,   # pas de servo bloqué par défaut
               angle_bloque  = 512,

               amplitude     = 300,
               turnOffset    = 0,

               t_final_sleep = 2,
               t_sleep       = 0.05):

    ser = dynamixel.get_serial_for_url(serial_port)

    offset = 512 + turnOffset
    n_servo = len(servo_id)

    # pré-calculs
    amplitude_norm = amplitude * (float(n_period)/n_servo) * 1024./300.
    omega          = 2 * pi * n_period/float(n_servo)

    # enable write response for all instructions ()# gestion servo bloqué
    multi_set_status_return(ser, servo_id, registers.STATUS_RETURN.RETURN_FOR_ALL_PACKETS)

    # Set velocity for init
    multi_set_velocity(ser,servo_id, 200)


    goal_pos_vect = [ int( round( offset + amplitude_norm * sin( omega*n ) ) )    for n in range(n_servo) ]
    # gestion servo bloqué
    if ( id_bloque != 0):
        goal_pos_vect[servo_id.index(id_bloque)] = angle_bloque


    # Angle safe check (can slow execution)
    assert abs(max(goal_pos_vect)-512) < 1024./300.*ANGLE_MAX , "Angle max (={}°) dépassé".format(ANGLE_MAX)
    for n in range(n_servo):
        sum = 0
        for z in range(n,n_servo):
            sum += (goal_pos_vect[z]-512)
            assert sum < 1024./300.*200. , "Le serpent allait se mordre la queue"
    # Move the snake in init position
    for n in range(n_servo):
        sleep(t_sleep)
        dynamixel.set_position( ser, servo_id[n], goal_pos_vect[n] )

    sleep(t_final_sleep)

    # Set velocity for movement
    multi_set_velocity(ser,servo_id, 400)

    # disable write response for read instructions
    multi_set_status_return(ser, servo_id, registers.STATUS_RETURN.RETURN_ONLY_FOR_READ)




def move_snake(serial_port = '/dev/ttyUSB0',
               servo_id    = [1,2,3,4,5,6,7,8,9,10,11,12],
               tick_period = 0.01,
               nb_tick     = 1200,
               resolution  = 300,
               n_period    = 1,
               id_bloque   = 0,   # pas de servo bloqué par défaut

               amplitude   = 300,
               turnOffset  = 0):

    ser = dynamixel.get_serial_for_url(serial_port)

    move    = -1
    offset  = 512+turnOffset
    n_servo = len(servo_id)
    goal_pos_vect = []

    # pré-calculs
    mvt_speed      = 2 * pi * 1./resolution
    amplitude_norm = amplitude * (float(n_period)/n_servo) * 1024./300.
    omega          = 2 * pi * n_period/float(n_servo)



    t = time()
    tick = 0
    for i in range(1,nb_tick):
        tick += move
        if (goal_pos_vect != []):
            for n in range(n_servo):

                # gestion servo bloqué
                if ( servo_id[n] == id_bloque):
                    continue

                dynamixel.set_position_no_response( ser, servo_id[n], goal_pos_vect[n] )

                #print "    ", time()-t  # DEBUG
        #print "  ", time()-t        # DEBUG

        # compute next goal position vector
        goal_pos_vect = [ int( round( offset + amplitude_norm * sin( omega*n + tick*mvt_speed ) ) )    for n in range(n_servo) ]
        # ne pas recréer la liste mais réécrire dedans pour opti ???

        # Angle safe check (can slow execution)
        assert abs(max(goal_pos_vect)-offset) < 1024./300.*ANGLE_MAX , "Angle max (={}°) dépassé".format(ANGLE_MAX)
        for n in range(n_servo):
            sum = 0
            for z in range(n,n_servo):
                sum += (goal_pos_vect[z]-512)
                assert sum < 1024./300.*200. , "Le serpent allait se mordre la queue"

        # Gestion control serpent
        """
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
        """

        # Wait next tick
        while( time() < t+i*tick_period ):    # tick => i
            pass
            #if ( tick%10 == 0 ):    #



            #sleep(sleep_time)   # utile si tick_period>0.001 ?
        # print( time()-t )  # DEBUG

    print('Success!')
