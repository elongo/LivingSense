from datetime import datetime, time
#import time

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

# Original test case from OP
while True:
    if is_time_between(time(13,30), time(16,30)) == True:
        print "YES"
    else:
        print "NO"
    time.sleep(3)