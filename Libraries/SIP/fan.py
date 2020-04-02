# This script turns on and off the fan, controlled by the timing_loop of sip.py, or sip_2.py
import RPi.GPIO as GPIO
import time
import atexit

""" Lights and fan GPIO setup """
GPIO.setmode(GPIO.BOARD)
GPIO_FAN = 21
GPIO.setup(GPIO_FAN,GPIO.OUT)
GPIO.output(GPIO_FAN, True)

""" *** SAYS GOOD BYE WHEN PROGRAM STOPS *** """
def exit_handler():
    print 'LivingSense stopped TRANSMITTING DATA. See you soon!'
    #fan_status = 1
    fan_off()
    GPIO.cleanup()
    return
atexit.register(exit_handler)
    # END OF GOOD BYE

def fan_on():
    GPIO.output(GPIO_FAN, False)
    print "fan_ON"
    time.sleep(0.5)
    return

def fan_off():
    GPIO.output(GPIO_FAN, True)
    print "fan_OFF"
    time.sleep(0.5)
    return
