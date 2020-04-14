#An example to brighten/dim an LED:
import time
import RPi.GPIO as GPIO
import sys
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
frequency = 5
frequency = (15, 7, 5) #List for testing different frequencies (the lower the frequency, the higher the speed)
dc = (70, 90, 90) #List for testing different duty cycles (the higher the duty cycle, the higher the speed)
#frequency = (15, 15, 15) #List for testing different frequencies (the lower the frequency, the higher the speed)
#dc = (60, 60, 60) #List for testing different duty cycles (the higher the duty cycle, the higher the speed)
interval = 60

try:
    while 1:
        for i in range(3):
            p = GPIO.PWM(12, frequency[i])  # GPIO.PWM(channel, frequency (in Hz)
            p.start(0)
            p.ChangeDutyCycle(dc[i])
            print "SPEED ", i+1, " --> ","frequency =", frequency[i], "// dc =", dc[i]
            # TIMER
            for remaining in range(interval, -1, -10):
                sys.stdout.write("\r")
                sys.stdout.write("{:2d} seconds remaining for next speed.  \n".format(remaining))
                sys.stdout.flush()
                time.sleep(10)

except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()
