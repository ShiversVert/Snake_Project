# -*- coding: utf-8 -*-

from time        import time, sleep
from math        import cos, sin, pi, atan
from pydynamixel import dynamixel, chain, registers

# TODO opti float()

# t = time()    # DEBUG
# for i in range(1000):
#     print (time() - t, "coucou{}".format(i))
#####  0.00276 sec  #####
# assert 0


############################

# You'll need to change this to the serial port of your USB2Dynamixel
serial_port = '/dev/ttyUSB0'
ser         = dynamixel.get_serial_for_url(serial_port)
# ser = dynamixel.get_serial_for_com(serial_port)    # DEBUG DEBUG


servo_id    = [1,2,3,4,5,6,7,8,9,10,11,12]

## Config servos movement ##
tick_period = 0.01
sleep_time  = tick_period/10    # si utilisé, permet de réduire l'utilisation des
                                # ressources de la machine, mais ticks moins précis
resolution  = 300     # nombre de tick pour une période de la pos angu d'un servo

## Config snake waveform  ##
n_period    = 1     # nombre de "période" de l'ondulation du serpent
amplitude   = 300     # amplitude de l'ondulation du serpent
ANGLE_MAX   = 120     # angle crete crete max
turnOffset  = 40

############################


offset  = 512+turnOffset
n_servo = len(servo_id)

# pré-calculs
mvt_speed      = 2 * pi * 1./resolution
amplitude_norm = amplitude * (float(n_period)/n_servo) * 1024./300.
omega          = 2 * pi *n_period/float(n_servo)


# enable write response
for n in range(n_servo):
    reg_value = registers.STATUS_RETURN.RETURN_FOR_ALL_PACKETS
    reg_addr  = registers.STATUS_RETURN_LEVEL  # /!\ /!\ WARNING marche uniquement sur 1 bytes !!!
                                               # goal position est sur 2 bytes !!!!
    dynamixel.set_reg_1b_no_response(ser, servo_id[n], reg_addr, reg_value)  # revoie pas de reponse
    print('Reg @{} set successfully at {} !'.format(reg_addr, reg_value) )

### Velocity settings ###
v = 400
velocity = [ v for i in range(n_servo) ]
sleep(0.1)
for n in range(n_servo):
    dynamixel.set_velocity(ser, servo_id[n] , velocity[n])
    #sleep(0.1)

# disable write response
for n in range(n_servo):
    reg_value = registers.STATUS_RETURN.RETURN_ONLY_FOR_READ
    reg_addr  = registers.STATUS_RETURN_LEVEL  # /!\ /!\ WARNING marche uniquement sur 1 bytes !!!
                                               # goal position est sur 2 bytes !!!!
    dynamixel.set_reg_1b(ser, servo_id[n], reg_addr, reg_value)  # revoie une reponse
    print('Reg @{} set successfully at {} !'.format(reg_addr, reg_value) )


# init position
goal_pos_vect = [ int( round( offset + amplitude_norm * cos( omega*n ) ) )    for n in range(n_servo) ]
# Angle safe check (can slow execution)
assert abs(max(goal_pos_vect)-offset) < 1024./300.*ANGLE_MAX , "Angle max (={}°) dépassé".format(ANGLE_MAX)
for n in range(n_servo):
    dynamixel.set_position_no_response( ser, servo_id[n], goal_pos_vect[n] )
dynamixel.send_action_packet( ser )
sleep(2)

t = time()
for tick in range(1,100000):
    for n in range(n_servo):
        # dynamixel.set_position( ser, servo_id[n], goal_pos_vect[n] )
        dynamixel.set_position_no_response( ser, servo_id[n], goal_pos_vect[n] )

        print "    ", time()-t  # DEBUG
    dynamixel.send_action_packet( ser )
    print "  ", time()-t        # DEBUG

    # compute next goal position vector
    goal_pos_vect = [ int( round( offset + amplitude_norm * cos( omega*n + tick*mvt_speed ) ) )    for n in range(n_servo) ]
    # ne pas recréer la liste mais réécrire dedans pour opti ???

    # Angle safe check (can slow execution)
    assert abs(max(goal_pos_vect)-offset) < 1024./300.*ANGLE_MAX , "Angle max (={}°) dépassé".format(ANGLE_MAX)

    # Wait next tick
    while( time() < t+tick*tick_period ):
        pass
        #sleep(sleep_time)   # utile si tick_period>0.001 ?
    print( time()-t )  # DEBUG

print('Success!')


"""
OPTIMISATIO POSSIBLE :
° 2 modes : ne pas envoyer (et attendre) le status packet
          => set servo + modif PyDynamixel

° mode goal pos : réduction de temps de d'execution du protocole
                  (module serial ??)

° mode velocity :
    - wheel mode  => impossible car c'est le torque de l'on controle en wheel mode


with status packet
    goal pos         : n_servo WRITE/READ + ( 1 WRITE )
    wheel mode       : n_servo READ + n_servo WRITE/READ + ( 1 WRITE )

without status packet
    goal pos         : n_servo WRITE + ( 1 WRITE )
    wheel mode       : n_servo READ + n_servo WRITE + ( 1 WRITE )
    simple velo mode : n READ + n WRITE + ( 1 WRITE ) + max:n_servo WRITE


mega opti !!!!! =>  set different response dealy time
                    and send ONE get_value instruction in broadcast
                    => no car pas de status packet si broadcast
                =>  refaire la librairy ?
                    => autant le faire en C (plus rapide ?)

"""
