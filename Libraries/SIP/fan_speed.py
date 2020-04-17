#An example to brighten/dim an LED:
import time
import RPi.GPIO as GPIO
import sys
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
frequency = (10, 7, 5) #List for testing different frequencies (the lower the frequency, the higher the speed)
dc = (80, 90, 100) #List for testing different duty cycles (the higher the duty cycle, the higher the speed)
p = GPIO.PWM(32, 15)

def fan_speed():
    try:
        while 1:
            p = GPIO.PWM(32, frequency[0])  # GPIO.PWM(channel, frequency (in Hz)
            p.start(dc[0])
            p.ChangeDutyCycle(dc[0])
            print "SPEED ", 1, " --> ","frequency =", frequency[0], "// dc =", dc[0]
            time.sleep(10)
            #continue
    except KeyboardInterrupt:
        p.stop()
        print "STOPPING FAN"
        pass

fan_speed()
GPIO.cleanup()
