#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import time
import urllib, urllib2, time
from datetime import datetime
import sys
import atexit
import RPi.GPIO as GPIO
import threading

""" *** POWER BI API's *** """
# REST API endpoint, given to you when you create an API streaming dataset
REST_API_URL = "https://api.powerbi.com/beta/ace026c8-7096-4d5d-ae54-48656360b58d/datasets/519b9b1d-173c-4f16-8d20-950a6501d713/rows?key=yT2ZCbH27ArVnczVRNgQNBVJG8yEi9PRpjCgc0qa2T5X9tqtD8VnkcknX0RuJ5%2F4GbYtXbC3JCj6W%2BK0acu83Q%3D%3D"

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir 	= '/sys/bus/w1/devices/'
device_folders  = glob.glob(base_dir + '28*')

""" LIST THAT WILL STORE TEMPERATURES """
temperatures = []

"""FIXED VARIABLES"""
max_temp = 50.0
min_temp = 0.0

""" *** SAYS GOOD BYE WHEN PROGRAM STOPS *** """
def exit_handler():
    print 'LivingSense stopped TRANSMITTING DATA. See you soon!'
    GPIO.cleanup()
    return
atexit.register(exit_handler)
    # END OF GOOD BYE

def read_temp_raw( filename ):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    return lines

def ReadSingleSensor( i, sensor_file ):
    device_name = sensor_file.replace( base_dir, '' ).replace( '/w1_slave', '' )
    print("SENSOR = ", device_name )

    lines = read_temp_raw( sensor_file )
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw( sensor_file )

    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        #print "SENSOR",i, " = ", temp_c
        temperatures.append(temp_c)
        print "temperatures LIST = ", temperatures
    time.sleep(0.5)

def ReadSensors():
    #for j in range(10):
    for (i, item) in enumerate(device_folders):
        sensor_file = item + '/w1_slave'
        print( sensor_file )
        ReadSingleSensor( i, sensor_file )

while True:
    try:
        ReadSensors()

        """ *** SENDING DATA TO POWER BI *** """
        # datetime
        now = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S%Z")

        # formatting data for POWER BI
        data = '[{{"timestamp": "{0}", "temperatura_fondo": "{1:0.1f}", "temperatura_medio": "{2:0.1f}", "temperatura_superficie": "{3:0.1f}", "max_temp": "{4:0.1f}", "min_temp":"{5:0.1f}"}}]'.format(now, temperatures[0], temperatures[1], temperatures[2], max_temp, min_temp)
        print ("data", data)
        #make HTTP POST request to Power BI REST API
        """
        req = urllib2.Request(REST_API_URL, data)
        response = urllib2.urlopen(req)
        #print("POST request to Power BI with data:{0}".format(data))
        print("Response: HTTP {0} {1}\n".format(response.getcode(), response.read()))
        print "DATA SENT TO POWER BI\n"
        """

        #clearing temperatures list values
        del temperatures[:]

    except:
        print "issue reading temps"
    """
    except urllib2.HTTPError as e:
        print("HTTP Error: {0} - {1}".format(e.code, e.reason))
    except urllib2.URLError as e:
        print("URL Error: {0}".format(e.reason))
    except Exception as e:
        print("POWER BI: General Exception: {0}".format(e))
    """

    print "WAITING 3 SEC FOR THE NEXT READING\n"
    time.sleep(10)
