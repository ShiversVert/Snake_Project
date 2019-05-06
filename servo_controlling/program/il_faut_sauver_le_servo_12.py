# -*- coding: utf-8 -*-
"""
Programme utilisé pour rétablir le contact avec le servo 12 qui a subi un
changement invololontaire de valeurs de registres. Son Baudrate et son Id
avait été changés.
"""
from pydynamixel import dynamixel, registers, packets


# You'll need to change this to the serial port of your USB2Dynamixel
serial_port = '/dev/ttyUSB0'

# ID of the servo to change (old ID if you change ID)
servo_id = 12

########################################################################################
# DOC : http://emanual.robotis.com/docs/en/dxl/ax/ax-12a/#control-table-of-eeprom-area #
########################################################################################

#packet_bytes = [ servo_id, 0x02, 0x01 ]


# registre value to set (cf DOC)
reg_value = 512

# registre address to set (cf registers.py ou la DOC juste au-dessus)
reg_addr = registers.  # /!\ /!\ WARNING marche uniquement sur 1 bytes !!!
                         # goal position est sur 2 bytes !!!!

# try:
ser = dynamixel.get_serial_for_url(serial_port)

# dynamixel.send_action_packet( ser )



# packet = packets.get_packet(packet_bytes)
# dynamixel.write_and_no_get_response(ser , packet)

# dynamixel.get_position( ser )
dynamixel.set_reg_1b(ser, servo_id, reg_addr, reg_value)
print('Reg set successfully at {} !'.format(reg_value) )
# except Exception as e:
#     print('Unable to set ID.')
#     print(e)

print "success"
