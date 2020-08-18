
from datetime import datetime
import time
from tentacle_pi.AM2315 import AM2315
import random

# AIR TEMPERATURE AND HUMIDITY 2X AM2315
am_in = AM2315(0x5c,"/dev/i2c-1") # default I2C bus
am_out = AM2315(0x5c,"/dev/i2c-3") # new I2C bus created on pins GPIO23 (SDA) and GPIO24 (SCL)
temperature_in = []
humidity_in = []
temperature_out = []
humidity_out = []

def air_in(): #in default I2C bus 1
    try:
        for x in range(0,2): #iterative loop to be sure that data is acquired, insted of crc = -1
            temp_hum_in_data = am_in.sense() # (am.sense() = (temperature, humidty, crc_check))
            #print 'temp_hum_data =', temp_hum_in_data
            temperature_in.append(temp_hum_in_data[0])
            humidity_in.append(temp_hum_in_data[1])
            print "temp_hum_in_data =", temp_hum_in_data
            time.sleep(0.05)
        #print 'temperature_in = ', temperature_in
        #print 'humidty_in = ', humidity_in
        temp_in = max(temperature_in)
        print 'temp_in = ', temp_in
        hum_in = max(humidity_in)
        print 'hum_in = ', hum_in
        del temperature_in[:]
        del humidity_in[:]
        air_in_final_data = [temp_in, hum_in]
        #return temp_in, hum_in
        return air_in_final_data

        
    except:
        print 'ISSUE WITH air_in()'

def air_out(): #in I2C bus 3
    try:
        for x in range(0,10): #iterative loop to be sure that data is acquired, insted of crc = -1
            temp_hum_out_data = am_out.sense() # (am.sense() = (temperature, humidty, crc_check))
            #print 'temp_hum_out_data =', temp_hum_out_data
            temperature_out.append(temp_hum_out_data[0])
            humidity_out.append(temp_hum_out_data[1])
            time.sleep(0.05)
        #print 'temperature_out = ', temperature_out
        #print 'humidty_out = ', humidity_out
        temp_out = max(temperature_out)
        #print 'temp_out = ', temp_out
        hum_out = max(humidity_out)
        #print 'hum_out = ', hum_out
        del temperature_out[:]
        del humidity_out[:]
        air_out_final_data = [temp_out, hum_out]
        return air_out_final_data
    except:
        print 'ISSUE WITH air_out()'

while True:
    # AIR_IN
    air_t_h_in = air_in() # returns temperature, humidty
    print "air_t_h_in =", air_t_h_in
    # AIR_OUT
    air_t_h_out = air_out() # returns temperature, humidty
    print "air_t_h_out =", air_t_h_out
    if air_t_h_in[0] < 5.0:
        print "yes, is below 5.0"
        air_t_h_in[1] = air_t_h_out[1] - random.randrange(5, 11, 1) #correction for Air_HUM_IN when there is a sensor failure
        print "NEW_air_t_h_in[1] = ", air_t_h_in[1]
        hour_now = datetime.now().hour
        print "hour_now", hour_now 
        if 6 <= hour_now <= 21:
            air_t_h_in[0] = air_t_h_out[0] + random.randrange(-1, 3, 1)
        else:
            air_t_h_in[0] = air_t_h_out[0] + random.randrange(4, 7, 1)
        print "NEWWWWW __ air_t_h_in[0], air_t_h_in[0] = ", air_t_h_in[0], air_t_h_in[1]
        print "AIR_T_IN_CORRECTION executed"
    time.sleep(5)
