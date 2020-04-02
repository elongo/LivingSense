# This script turns on and off the lights, controlled by the timing_loop of sip.py, or sip_2.py

import RPi.GPIO as GPIO
import time
import atexit

""" Lights and fan GPIO setup """
GPIO.setmode(GPIO.BOARD)
GPIO_LIGHT = 19
GPIO.setup(GPIO_LIGHT,GPIO.OUT)
#GPIO.output(GPIO_LIGHT, True)

""" *** SAYS GOOD BYE WHEN PROGRAM STOPS *** """
"""
def exit_handler():
    print 'LivingSense stopped TRANSMITTING DATA. See you soon!'
    #light_status = 0
    lights_off()
    print "quitting script"
    GPIO.cleanup()
    return
atexit.register(exit_handler)
    # END OF GOOD BYE
"""

def lights_on():
    GPIO.setmode(GPIO.BOARD)
    GPIO_LIGHT = 19
    GPIO.output(GPIO_LIGHT, False)
    print "setting GPIO_LIGHT.FALSE -> on"
    print "lights_ON"
    time.sleep(0.5)
    print "lights_on ending"
    return

def lights_off():
    GPIO.setmode(GPIO.BOARD)
    GPIO_LIGHT = 19
    GPIO.setup(GPIO_LIGHT,GPIO.OUT)  # Light pin
    GPIO.output(GPIO_LIGHT, True)
    print "setting GPIO_LIGHT.TRUE -> off"
    print "lights_OFF"
    time.sleep(5)
    return
