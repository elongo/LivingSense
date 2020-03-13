#!/usr/bin/env python

#Activate virtual environment
activate_this_file = "/home/pi/LS05/venv_LS05/bin/activate_this.py"
execfile(activate_this_file, dict(__file__=activate_this_file))

import RPi.GPIO as GPIO
import time, sys
import urllib, urllib2, time
from datetime import datetime
import threading

#FLOW SENSOR SETUP
FLOW_SENSOR = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

global count
count = 0
global start
start = 0
global w_flow
w_flow = 0

def countPulse(channel):
   global count
   count = count+1
   global end
   end = time.time()
   elapsed = end - start
   global w_flow
   w_flow = count/(7.5*elapsed)
   return w_flow

GPIO.add_event_detect(FLOW_SENSOR, GPIO.FALLING, callback=countPulse)

def no_flow():
    try:
        global start
        start = time.time()
        print "START IN LOOP = ", start
        global w_flow
        w_flow = 0.0
        print "w_flow in FALSE event_detected", round(w_flow, 2)
    except:
        print "Couldn't set w_flow to 0"
    return w_flow

#while True:
def water_flow():
    threading.Timer(40.0, water_flow).start() # sets how often w_flow is sent to AWS
    try:
        if GPIO.event_detected(FLOW_SENSOR) == False:
            no_flow()
            print "w_flow in if GPIO.event_detected(FLOW_SENSOR=", w_flow
            time.sleep(0.1)
        time.sleep(0.1)
    except KeyboardInterrupt:
        print '\ncaught keyboard interrupt!, bye'
        GPIO.cleanup()
        sys.exit()

water_flow()
