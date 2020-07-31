#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

from datetime import datetime
from pymodbus.client.sync import ModbusTcpClient
from struct import *
import math
import time

con_cube_ip = '172.18.0.186'
now = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S%Z")

def convert_bytes_to_float(int1, int2):
    hex1 = (int1).to_bytes(2,byteorder='little')
    hex2 = (int2).to_bytes(2,byteorder='little')
    return 0 if math.isnan(float(unpack("<f",hex2 + hex1)[0])) else unpack("<f",hex2 + hex1)[0]

for i in range(1,2):
    client = ModbusTcpClient(con_cube_ip)
    r = client.read_input_registers(0x0000, 116)
    #r = client.read_input_registers(0x00, 116)
    print('REGISTERS =',  (r.registers))
    print ('')
    print ('')
    response = client.read_holding_registers(0x0000,116)
    print ("response.resgisters = ", response.registers)
    print("r = ", r)
    print ('')
    print ('')
    line = 'xP1Value=' + str(convert_bytes_to_float(r.registers[0], r.registers[1])) + \
            ',xP2Value=' + str(convert_bytes_to_float(r.registers[2], r.registers[3])) + \
            ',xP3Value=' + str(convert_bytes_to_float(r.registers[4], r.registers[5])) + \
            ',xP4Value=' + str(convert_bytes_to_float(r.registers[26], r.registers[27])) + \
            ',xP5Value=' + str(convert_bytes_to_float(r.registers[34], r.registers[35])) + \
            ',xP6Value=' + str(convert_bytes_to_float(r.registers[42], r.registers[43])) + \
            ',xP7Value=' + str(convert_bytes_to_float(r.registers[50], r.registers[51])) + \
            ',xP8Value=' + str(convert_bytes_to_float(r.registers[58], r.registers[59])) + \
            ',xP9Value=' + str(convert_bytes_to_float(r.registers[66], r.registers[67])) + \
            ',xP10Value=' + str(convert_bytes_to_float(r.registers[74], r.registers[75])) + \
            ',xP11Value=' + str(convert_bytes_to_float(r.registers[82], r.registers[83])) + \
            ',xP12Value=' + str(convert_bytes_to_float(r.registers[90], r.registers[91])) + \
            ',xP13Value=' + str(convert_bytes_to_float(r.registers[98], r.registers[99])) + \
            ',xP14Value=' + str(convert_bytes_to_float(r.registers[106], r.registers[107])) + \
            ',xP15Value=' + str(convert_bytes_to_float(r.registers[114], r.registers[115])) + \
            ' ' + str(now) + '\n'
    print('line = ', line)
    for i in range(0,115):
        registers_i = convert_bytes_to_float(r.registers[i], r.registers[i+1] )
        print ("register_", i, " = ", registers_i)
    """
    line = 'xP1Value=' + str(convert_bytes_to_float(r.registers[2], r.registers[3])) + \
            ',xP2Value=' + str(convert_bytes_to_float(r.registers[10], r.registers[11])) + \
            ',xP3Value=' + str(convert_bytes_to_float(r.registers[18], r.registers[19])) + \
            ',xP4Value=' + str(convert_bytes_to_float(r.registers[26], r.registers[27])) + \
            ',xP5Value=' + str(convert_bytes_to_float(r.registers[34], r.registers[35])) + \
            ',xP6Value=' + str(convert_bytes_to_float(r.registers[42], r.registers[43])) + \
            ',xP7Value=' + str(convert_bytes_to_float(r.registers[50], r.registers[51])) + \
            ',xP8Value=' + str(convert_bytes_to_float(r.registers[58], r.registers[59])) + \
            ',xP9Value=' + str(convert_bytes_to_float(r.registers[66], r.registers[67])) + \
            ',xP10Value=' + str(convert_bytes_to_float(r.registers[74], r.registers[75])) + \
            ',xP11Value=' + str(convert_bytes_to_float(r.registers[82], r.registers[83])) + \
            ',xP12Value=' + str(convert_bytes_to_float(r.registers[90], r.registers[91])) + \
            ',xP13Value=' + str(convert_bytes_to_float(r.registers[98], r.registers[99])) + \
            ',xP14Value=' + str(convert_bytes_to_float(r.registers[106], r.registers[107])) + \
            ',xP15Value=' + str(convert_bytes_to_float(r.registers[114], r.registers[115])) + \
            ' ' + str(now) + '\n'
    """
    
    client.close()
    time.sleep(1)
    

with open('/tmp/new/' + str(now), 'a') as file:
    file.write(line)