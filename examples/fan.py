# This script turns on and off the fan every 5 seconds.

import RPi.GPIO as GPIO
import time
import atexit

GPIO.setmode(GPIO.BOARD)
fan_status = 0
# Define GPIO to use on Pi
GPIO_FAN = 21
GPIO.setup(GPIO_FAN,GPIO.OUT)  # Light pin
# Set light to True (High)
GPIO.output(GPIO_FAN, True)

""" *** SAYS GOOD BYE WHEN PROGRAM STOPS *** """
def exit_handler():
    print 'LivingSense stopped TRANSMITTING DATA. See you soon!'
    fan_status = 1
    fan()
    GPIO.cleanup()
    return
atexit.register(exit_handler)
    # END OF GOOD BYE

def fan():
    GPIO.setmode(GPIO.BOARD)
    time.sleep(0.5)
    if fan_status == 1:
        GPIO.output(GPIO_FAN, False)
    elif fan_status == 0:
        GPIO.output(GPIO_FAN, True)

while True:
    fan()
    if fan_status == 1:
        fan_status = 0
    else:
        fan_status = 1
    time.sleep(5)
