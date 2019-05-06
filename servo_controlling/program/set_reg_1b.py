# -*- coding: utf-8 -*-
"""
Programme pour changer la valeur d'un registre sur 1 octet
"""


from pydynamixel import dynamixel, registers


# You'll need to change this to the serial port of your USB2Dynamixel
serial_port = '/dev/ttyUSB0'

# ID of the servo to change (old ID if you change ID)
servo_id = 254  #254 = broadcast

########################################################################################
# DOC : http://emanual.robotis.com/docs/en/dxl/ax/ax-12a/#control-table-of-eeprom-area #
########################################################################################


# registre value to set (cf DOC)
reg_value = registers.LED_STATE.OFF

# registre address to set (cf registers.py ou la DOC juste au-dessus)
reg_addr = registers.LED     # /!\ /!\ WARNING marche uniquement sur 1 bytes !!!
                             # goal position est sur 2 bytes !!!!

ser = dynamixel.get_serial_for_url(serial_port)
dynamixel.set_reg_1b(ser, servo_id, reg_addr, reg_value)
print('Reg set successfully at {} !'.format(reg_value) )
