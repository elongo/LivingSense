#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO

while True:
    # Use BCM GPIO references
    # instead of physical pin numbers
    GPIO.setmode(GPIO.BCM)

    # Define GPIO to use on Pi
    """
    GPIO_VALVE_1 = 17
	GPIO_VALVE_2 = 27
	GPIO_VALVE_3 = 22
	GPIO_VALVE_4 = 14
	"""
	
	# Channel list for setting up all GPIO at the same time
	chan_list = (17, 27, 22, 14)
	
    # Set pins as output and input
    GPIO.setup(chan_list, GPIO.OUT)  # 4 Relays

    # Set trigger to False (Low)
    GPIO.output(chan_list, True)

    # Allow module to settle
    time.sleep(3)

	"""
    # Send 10us pulse to trigger
    GPIO.output(GPIO_VALVE_1, False)
    print "RELAY_7 ON"
    time.sleep(3)
    GPIO.output(GPIO_VALVE_1, True)
    print "RELAY_7 OFF"
    time.sleep(5)
    GPIO.output(GPIO_VALVE_2, False)
    print "RELAY_8 ON"
    time.sleep(3)
    GPIO.output(GPIO_VALVE_2, True)
    print "RELAY_8 OFF"
    time.sleep(5)
    """
    
    #Looping through 4 relays
    for i in chan_list:
		GPIO.output(i, False)
		print "Relay ", i, "ON"
		time.sleep(1)
		GPIO.output(i, True)
		time.sleep(1)

	time.sleep(5)
	
    # Reset GPIO settings
    GPIO.cleanup()
