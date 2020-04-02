import time
import sys
import RPi.GPIO as GPIO

a_on = '1111111111111010101011101' #coming from pyplot
a_off = '1111111111111010101010111' #coming from pyplot
short_delay = 0.00032
long_delay = 0.00092
extended_delay = 0.00952

NUM_ATTEMPTS = 10
#TRANSMIT_PIN = 23
TRANSMIT_PIN = 16


def transmit_code(code):
    '''Transmit a chosen code string using the GPIO transmitter'''
    #GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    for t in range(NUM_ATTEMPTS):
        for i in code:
            if i == '1':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(short_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(long_delay)
            elif i == '0':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(long_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(short_delay)
            else:
                continue
        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(extended_delay)
    #GPIO.cleanup()

if __name__ == '__main__':
    for argument in sys.argv[1:]:
        exec('transmit_code(' + str(argument) + ')')
