# This script turns on and off the lights every 5 seconds.

import RPi.GPIO as GPIO
import time
import atexit

GPIO.setmode(GPIO.BOARD)
light_status = 0
# Define GPIO to use on Pi
GPIO_LIGHT = 19
GPIO.setup(GPIO_LIGHT,GPIO.OUT)  # Light pin
# Set light to True (High)
GPIO.output(GPIO_LIGHT, True)

""" *** SAYS GOOD BYE WHEN PROGRAM STOPS *** """
def exit_handler():
    print 'LivingSense stopped TRANSMITTING DATA. See you soon!'
    light_status = 1
    illumination()
    GPIO.cleanup()
    return
atexit.register(exit_handler)
    # END OF GOOD BYE

def illumination():
    GPIO.setmode(GPIO.BOARD)
    time.sleep(0.5)
    if light_status == 1:
        GPIO.output(GPIO_LIGHT, False)
    elif light_status == 0:
        GPIO.output(GPIO_LIGHT, True)

while True:
    illumination()
    if light_status == 1:
        light_status = 0
    else:
        light_status = 1
    time.sleep(5)
