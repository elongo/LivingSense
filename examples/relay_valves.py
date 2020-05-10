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
chan_list = (36, 29, 31, 12, 8, 11, 13, 15) #BOARD numbering

while True:
    # Set pins as output and input
    GPIO.setup(chan_list, GPIO.OUT)  # 4 Relays

    # Set trigger to False (Low)
    GPIO.output(chan_list, True)

    # Allow module to settle
    time.sleep(0.1)

    #Looping through 4 relays
    for i in chan_list:
		GPIO.output(i, False)
		print "Relay ", i, "ON"
		time.sleep(1)
		GPIO.output(i, True)
		time.sleep(1)
    # Reset GPIO settings
GPIO.cleanup()
