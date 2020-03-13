import time
import sys
import RPi.GPIO as GPIO

#FIRST SET OF REMOTE OUTLETS (IA, IB, IC)
a1_on = '1111111111111010101011101'
a1_off = '1111111111111010101010111'
b1_on = '1111111111101110101011101'
b1_off = '1111111111101110101010111'
c1_on = '1111111111101011101011101'
c1_off = '1111111111101011101010111'
#SECOND SET OF REMOTE OUTLETS (IIA, IIB, IIC)
a2_on = '1011111111111010101011101'
a2_off = '1011111111111010101010111'
b2_on = '1011111111101110101011101'
b2_off = '1011111111101110101010111'
c2_on = '1011111111101011101011101'
c2_off = '1011111111101011101010111'

short_delay = 0.000291
long_delay = 0.000933
extended_delay = 0.009552

NUM_ATTEMPTS = 10
TRANSMIT_PIN = 23

def transmit_code(code):
    '''Transmit a chosen code string using the GPIO transmitter'''
    GPIO.setmode(GPIO.BCM)
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
    GPIO.cleanup()

if __name__ == '__main__':
    for argument in sys.argv[1:]:
        exec('transmit_code(' + str(argument) + ')')
