#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO
# Use BCM GPIO references
# instead of physical pin numbers
#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
# Channel list for setting up all GPIO at the same time
#chan_list = (16, 5, 6, 18, 14, 17, 27, 22, 25) #BCM numbering
#chan_list = (36, 29, 31, 12, 8, 11, 13, 15) #BOARD numbering for 8X relays
chan_list = (36, 29, 31, 12, 15) #BOARD numbering for 4X relays
#Set pins as output and input
GPIO.setup(chan_list, GPIO.OUT)  # 4 Relays
# Set trigger to False (Low)
GPIO.output(chan_list, True)

#Looping through 4 relays
try:
    while True:
        for i in chan_list:
            GPIO.output(i, False)
            print "Relay ", i, "ON"
            time.sleep(0.2)
            GPIO.output(i, True)
            time.sleep(0.2)
        print "END OF LOOP"
        time.sleep(0.5)        
except KeyboardInterrupt:
    print "Program Interrupted from Keyboard"
except: 
    print "Something has failed. Sniff around!"
finally:
    GPIO.cleanup() # clean gpios
    print "GPIO.cleanup() executed"
