#An example to brighten/dim an LED:
import time
import RPi.GPIO as GPIO
import sys
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
frequency = (15, 7, 5) #List for testing different frequencies (the lower the frequency, the higher the speed)
dc = (70, 90, 100) #List for testing different duty cycles (the higher the duty cycle, the higher the speed)
interval = 10
timer_steps = interval/4

try:
    while 1:
        for i in range(3):
            p = GPIO.PWM(32, frequency[i])  # GPIO.PWM(channel, frequency (in Hz)
            p.start(0)
            p.ChangeDutyCycle(dc[i])
            print "SPEED ", i+1, " --> ","frequency =", frequency[i], "// dc =", dc[i]
            # TIMER
            for remaining in range(interval, 0, -(timer_steps)):
                sys.stdout.write("\r")
                sys.stdout.write("{:2d} seconds remaining for next speed.  \n".format(remaining))
                sys.stdout.flush()
                time.sleep(timer_steps)

except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()