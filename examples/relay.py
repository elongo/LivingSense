#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO

while True:
    # Use BCM GPIO references
    # instead of physical pin numbers
    GPIO.setmode(GPIO.BCM)

    # Define GPIO to use on Pi
    GPIO_RELAY_1 = 16
    GPIO_RELAY_2 = 5
    GPIO_RELAY_3 = 6
    GPIO_RELAY_4 = 9
    GPIO_RELAY_5 = 10

    # Set pins as output and input
    GPIO.setup(GPIO_RELAY_1,GPIO.OUT)  # RELAY_1
    GPIO.setup(GPIO_RELAY_2,GPIO.OUT)  # RELAY_2
    GPIO.setup(GPIO_RELAY_3,GPIO.OUT)  # RELAY_3
    GPIO.setup(GPIO_RELAY_4,GPIO.OUT)  # RELAY_4
    GPIO.setup(GPIO_RELAY_5,GPIO.OUT)  # RELAY_5

    # Set trigger to False (Low)
    GPIO.output(GPIO_RELAY_1, True)
    GPIO.output(GPIO_RELAY_2, True)
    GPIO.output(GPIO_RELAY_3, True)
    GPIO.output(GPIO_RELAY_4, True)
    GPIO.output(GPIO_RELAY_5, False)

    # Allow module to settle
    time.sleep(0.5)

    # Send 10us pulse to trigger
    GPIO.output(GPIO_RELAY_1, False)
    print "RELAY_2 ON"
    time.sleep(3)
    GPIO.output(GPIO_RELAY_1, True)
    print "RELAY_2 OFF"
    time.sleep(5)

    GPIO.output(GPIO_RELAY_2, False)
    print "RELAY_2 ON"
    time.sleep(3)
    GPIO.output(GPIO_RELAY_2, True)
    print "RELAY_2 OFF"
    time.sleep(5)

    GPIO.output(GPIO_RELAY_3, False)
    print "RELAY_3 ON"
    time.sleep(3)
    GPIO.output(GPIO_RELAY_3, True)
    print "RELAY_3 OFF"
    time.sleep(5)

    GPIO.output(GPIO_RELAY_4, False)
    print "RELAY_4 ON"
    time.sleep(3)
    GPIO.output(GPIO_RELAY_4, True)
    print "RELAY_4 OFF"
    time.sleep(5)

    GPIO.output(GPIO_RELAY_5, True)
    print "RELAY_4 ON"
    time.sleep(3)
    GPIO.output(GPIO_RELAY_5, False)
    print "RELAY_4 OFF"
    time.sleep(5)

    # Reset GPIO settings
    GPIO.cleanup()
