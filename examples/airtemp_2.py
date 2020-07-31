import time
from tentacle_pi.AM2315 import AM2315
am = AM2315(0x5c,"/dev/i2c-3")
temperature = []
humidity = []

for x in range(0,10):
    data = am.sense() # (am.sense() = (temperature, humidty, crc_check))
    print 'iteration ', x
    print 'data =', data
    temperature.append(data[0])
    humidity.append(data[1])
    time.sleep(0.05)
print 'temperature = ', temperature 
print 'humidty = ', humidity
temp_final = max(temperature)
print 'temp_final = ', temp_final
hum_final = max(humidity)
print 'hum_final = ', hum_final
del temperature[:]
del humidty[:]

