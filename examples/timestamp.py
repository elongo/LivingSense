# This script turns on and off the fan every 5 seconds.

from datetime import datetime

now = datetime.now() 
now_str = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S%Z")
now_int = int(now.strftime('%Y%m%d'))

print "now = ", now
print "now_str = ", now_str
print "now_int = ", now_int