#!/usr/bin/env python
# -*- coding: utf-8 -*-

activate_this_file = "/home/pi/LS05/venv_LS05/bin/activate_this.py"
execfile(activate_this_file, dict(__file__=activate_this_file))

""" *** LivingSense Libraries *** """
import os
import urllib, urllib2, time
from datetime import datetime
import sys
import Adafruit_ADS1x15
import atexit
import RPi.GPIO as GPIO
import glob
from tentacle_pi.AM2315 import AM2315
import threading
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
    #END of Libraries

""" *** VARIABLES *** """
# FIXED PARAMETERS FOR GAUGES IN POWER BI
VWC = {}
tank_empty = 0
tank_full = 125
#Timing variables
sensors_interval = 5.0
flow_rate_interval = 5.0

#Rockwool temperature
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# AIR TEMPERATURE AND HUMIDITY
am = AM2315(0x5c,"/dev/i2c-1")

    # END OF GLOBAL VARIABLES

""" *** AWS *** """
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("123afhlss456")
myMQTTClient.configureEndpoint("a2wl9vn89c13do.iot.eu-west-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/LS05/Libraries/AWS/deviceSDK/CA.pem", "/home/pi/LS05/Libraries/AWS/deviceSDK/0f7d7e8487-private.pem.key", "/home/pi/LS05/Libraries/AWS/deviceSDK/0f7d7e8487-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("ls05/info", "connected", 0)

""" *** SAYS GOOD BYE WHEN PROGRAM STOPS *** """
def exit_handler():
    print 'LivingSense stopped TRANSMITTING DATA. See you soon!'
    GPIO.cleanup()
    return
atexit.register(exit_handler)
    # END OF GOOD BYE

""" ***  CPU TEMPERATURE *** """
def get_cpu_temp():
  res = os.popen("vcgencmd measure_temp").readline()
  t = float(res.replace("temp=","").replace("'C\n",""))
  return t

""" *** VWC *** """
def vwc():
    adc = Adafruit_ADS1x15.ADS1115()
    GAIN = 1

    # Read all the ADC channel values in a list.
    values = [0]*4
    for i in range(4):
          # Read the specified ADC channel using the previously set gain value.
          values[i] = adc.read_adc(i, gain=GAIN)
          VWC[i+1] =  (-0.0083*values[i]) + 167.81 # Old valibration made by EL
          #VWC[i+1] =  (-0.00908*values[i]) + 187 # Calibratio made by Théo
    return VWC
    # END OF VWC

""" *** WATER LEVEL - ULTRASOUND *** """
def level():
    try:
        # Use BCM GPIO references
        # instead of physical pin numbers
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # Define GPIO to use on Pi
        GPIO_TRIGGER = 13
        GPIO_ECHO    = 26

        # Set pins as output and input
        GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
        GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

        # Set trigger to False (Low)
        GPIO.output(GPIO_TRIGGER, False)

        # Allow module to settle
        time.sleep(1)

        # Send 10us pulse to trigger
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        start = time.time()

        while GPIO.input(GPIO_ECHO)==0:
          start = time.time()

        while GPIO.input(GPIO_ECHO)==1:
          stop = time.time()

        # Calculate pulse length
        elapsed = stop-start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = elapsed * 34300

        # total distance travelled by sound, divided by 2 (due to sound return), minus 3 cm (gap betwen sensor and water)
        distance = (distance -3.0)/ 2.0
        v_total = 125
        v_empty = (distance * 5.06)
        v_in_tank = v_total - v_empty

        # Reset GPIO settings
        return v_in_tank
        # END OF WATER LEVEL SENSOR
    except:
        print "WE HAVE PROBLEMS WITH ULTRASOUND SENSOR"

""" *** ROCKWOOLL TEMPERATURE AND HUMIDTY *** """

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        rock_temp = temp_c
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return rock_temp
        # END OF ROCKWOOLL TEMP AND HUMIDTY

""" *** AIR TEMPERATURE AND HUMIDTY *** """
def air():
    temperature, humidity, crc_check = am.sense()
    return temperature, humidity
    time.sleep(0.05)

while True:
    try:
        now = datetime.utcnow()
        from FLOW import w_flow
        w_flow = w_flow
        now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
        t = get_cpu_temp() # returns t
        VWC = vwc() #returns Sensor 0, Sensor 1, Sensor 2, Sensor 3
        w_lev = level() #returns distance
        read_temp_raw()
        rock_t = read_temp() # returns temp_c (temperature in rockwool)
        air_temp_hum = air() # returns temperature, humidty
        air_t = air_temp_hum[0]
        air_h = air_temp_hum[1]

        # Fitting VWC in the range 0-100 %
        for i in VWC:
            if VWC[i] < 0:
                VWC[i] = 0
            elif VWC[i] > 100:
                VWC[i] = 100
        WC1 = VWC[1]
        print WC1
        WC2 = VWC[2]
        print WC2
        WC3 = VWC[3]
        print WC3
        WC4 = VWC[4]
        print WC4

        # Fitting water_level in the range 0-125 L
        if w_lev < 0:
            w_lev = 0
        elif w_lev > 125:
            w_lev = 125

        """FULL PAYLOAD"""
        payload = '{"dateTime":"'+now_str +'","cpu":'+str(round(t,0))+',"w_flow":'+str(round(w_flow,1))+',"w_lev":'+str(round(w_lev, 0))+',"rock_t":'+str(round(rock_t,0))+',"VWC1":'+str(round(WC1,0))+',"VWC2":'+str(round(WC2,0))+',"VWC3":'+str(round(WC3,0))+',"VWC_4":'+str(round(WC4,0))+',"air_t":'+str(round(air_t,0))+',"air_h":'+ str(round(air_h,0))+'}'

        print "payload= ",payload
        myMQTTClient.publish("ls05-2030-24092017/data", payload, 0)
        time.sleep(15)
    except:
        print ("ACHTUNG: ---> ISSUE WHILE STREAMING TO AWS")
        time.sleep(5)
