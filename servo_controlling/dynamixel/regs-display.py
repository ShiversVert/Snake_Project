#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Displays current settings of a Dynamixel servo registers.'''

import dynamixel
import argparse

__author__ = 'Eric Pascual (POBOT)'

encoded_regs = [
        'BaudRate',
        'StatusReturnLevel',
        'AlarmLED',
        'AlarmShutdown',
        'RegisteredInstruction'
        ]

def decode_reg_value(regid, regvalue):
    if regid == 'BaudRate':
        return dynamixel.defs.BAUD_RATE.key(regvalue)
    if regid == 'StatusReturnLevel':
        return dynamixel.defs.STATUS_RETURN_LEVEL.key(regvalue)
    if regid == 'AlarmLED' or regid == 'AlarmShutdown':
        if regvalue == 0:
            return ''
        s = []
        for mask in [1 << i for i in range(0, 8)]:
            if regvalue & mask:
                s.append(dynamixel.defs.ERROR_STATUS.key(mask))
        return ','.join(s)
    if regid == 'RegisteredInstruction':
        return dynamixel.defs.INSTRUCTION.key(regvalue) if regvalue != 0 else '-none-'

    return ''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-p', '--port', dest='port',
            help='the serial port of the bus interface [default=%(default)s]',
            default='/dev/ttyUSB0')
    parser.add_argument('-i', '--id', dest='id', type=int,
            help='the AX12 id [default=%(default)s]',
            default=1)
    parser.add_argument('-b', '--baudrate', dest='baudrate', type=int,
            help='the bus speed [default=%(default)s]',
            default=1000000)

    args = parser.parse_args()

    serial = dynamixel.SerialStream(port=args.port, baudrate=args.baudrate, timeout=1)
    net = dynamixel.DynamixelNetwork(serial)

    net.scan(args.id, args.id)
    ax12 = net[args.id]
    if ax12:
        ax12.read_all()

        # list the registers sorted by their num
        for regid, regnum, regdesc in sorted(dynamixel.defs.REGISTER.items(), key=lambda x : x[1]):
            regvalue = ax12.cache[regnum]
            if regid in encoded_regs:
                s = decode_reg_value(regid, regvalue)
            else:
                s = '0x%02x' % regvalue
            print('[%2d] %-25s : %5d (%s)' % (regnum, regdesc, regvalue, s))

    else:
        print('[ERROR] no AX12 found with id=%d' % args.id)
