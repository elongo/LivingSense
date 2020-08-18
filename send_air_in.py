#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

import socket
from tentacle_pi.AM2315 import AM2315
from datetime import datetime
import time

# AIR TEMPERATURE AND HUMIDITY 2X AM2315
am_in = AM2315(0x5c,"/dev/i2c-1") # default I2C bus
temperature_in = []
humidity_in = []

UDP_IP = "172.18.2.183"
UDP_PORT = 5005

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

def air_in(): #in default I2C bus 1
    try:
        for x in range(0,10): #iterative loop to be sure that data is acquired, insted of crc = -1
            temp_hum_in_data = am_in.sense() # (am.sense() = (temperature, humidty, crc_check))
            #print 'temp_hum_data =', temp_hum_in_data
            temperature_in.append(temp_hum_in_data[0])
            humidity_in.append(temp_hum_in_data[1])
            time.sleep(0.05)
        #print 'temperature_in = ', temperature_in
        #print 'humidty_in = ', humidity_in
        temp_in = max(temperature_in)
        #print 'temp_in = ', temp_in
        hum_in = max(humidity_in)
        #print 'hum_in = ', hum_in
        del temperature_in[:]
        del humidity_in[:]
        return temp_in, hum_in
    except:
        print 'ISSUE WITH air_in()'

sock = socket.socket(socket.AF_INET, # Internet
socket.SOCK_DGRAM) # UDP

while True:
    air_t_h_in_st2 = air_in() # returns temperature, humidty
    now = time.time()
    print "NOW =", now
    data = [now, air_t_h_in_st2[0], air_t_h_in_st2[1]]
    for i in range(3):
        MESSAGE =  str(data[i])
        print MESSAGE
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    print "data sent to", UDP_IP
    time.sleep(60)
