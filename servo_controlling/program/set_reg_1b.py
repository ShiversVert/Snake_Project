# -*- coding: utf-8 -*-

from pydynamixel import dynamixel, registers



# You'll need to change this to the serial port of your USB2Dynamixel
serial_port = '/dev/ttyUSB0'

# ID of the servo to change (old ID if you change ID)
servo_id = 254  #broadcast

########################################################################################
# DOC : http://emanual.robotis.com/docs/en/dxl/ax/ax-12a/#control-table-of-eeprom-area #
########################################################################################


# registre value to set (cf DOC)
reg_value = registers.LED_STATE.OFF

# registre address to set (cf registers.py ou la DOC juste au-dessus)
reg_addr = registers.LED  # /!\ /!\ WARNING marche uniquement sur 1 bytes !!!
                         # goal position est sur 2 bytes !!!!

# try:
ser = dynamixel.get_serial_for_url(serial_port)
#dynamixel.send_action_packet( ser )
dynamixel.set_reg_1b(ser, servo_id, reg_addr, reg_value)
print('Reg set successfully at {} !'.format(reg_value) )
# except Exception as e:
#     print('Unable to set ID.')
#     print(e)
