from os import listdir,rename, makedirs
import requests
from datetime import datetime, timezone
import pathlib

base = "/home/pi/get_gps_python/"
user = <nutzer>
pw = <password>

data_list = listdir('/home/pi/get_gps_python/new')
now = datetime.now(timezone.utc)

db = 'collected_data'
influx = <link_of_influx_api>

url = influx + '/write?db=' + db


for file in data_list:
    with open (base + "new/" + file, "r") as data_point:
        data=data_point.readlines()
    for line in data:
        r = requests.post(url, data=line, auth=(user,pw))
        if '204' == str(r.status_code):
            dt = datetime.fromtimestamp(int(file) // 1000000000)
            dt_s = dt.strftime('%Y-%m-%d')
            makedirs(base + "old" , exist_ok=True)
            rename(base + "new/" + file, base + "old/" + file)

