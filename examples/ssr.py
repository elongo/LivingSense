#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO



try:
    while True:
        # Use BCM GPIO references
        # instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)
        # Define GPIO to use on Pi
        GPIO_RELAY_1 = 12

        # Set pins as output and input
        GPIO.setup(GPIO_RELAY_1,GPIO.OUT)  # RELAY_1

        # Set trigger to False (Low)
        GPIO.output(GPIO_RELAY_1, False)

        # Allow module to settle
        time.sleep(0.1)

        # Send 10us pulse to trigger

        GPIO.output(GPIO_RELAY_1, True)
        print "RELAY_1 ON"
        time.sleep(0.5)
        GPIO.output(GPIO_RELAY_1, False)
        print "RELAY_1 OFF"
        time.sleep(0.2)

        # Reset GPIO settings
        GPIO.cleanup()

except KeyboardInterrupt:
    pass
GPIO.output(GPIO_RELAY_1, False)
print "Finito : OFF"
GPIO.cleanup()
