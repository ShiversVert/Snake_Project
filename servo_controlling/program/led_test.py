"""
Test d'allumage/extinction de la LED d'un servomoteur
"""

from pydynamixel import dynamixel, registers

# You'll need to change this to the serial port of your USB2Dynamixel
serial_port = '/dev/ttyUSB0'

# You'll need to change this to the ID of your servo
servo_id = 3

# Turn the LED on or off (choose by commmenting)
led_value = registers.LED_STATE.ON
#led_value = registers.LED_STATE.OFF

try:
    ser = dynamixel.get_serial_for_url(serial_port)
    dynamixel.set_led(ser, servo_id, led_value)
    print('LED set successfully!')
except Exception as e:
    print('Unable to set LED.')
    print(e)
