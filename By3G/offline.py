import serial
import urllib.request, json
import sys
import requests
import os
from subprocess import call
from time import sleep, time
API_ENDPOINT = "http://"+sys.argv[1]+":"+sys.argv[2]+"/putdata"
API_KEY = sys.argv[4]+"@"+sys.argv[5];
headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
filenumber = 0

def check_internet():
    url=API_ENDPOINT
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("internet or webserver lost connection")
        return False
    except requests.exceptions.ReadTimeout:
        print("timeout")
        return False

while True:
    data = {}
    pre_time = time()
    adsb = []
    if check_internet():
        print("on")
        call(["python", "By3G.py", sys.argv[1], sys.argv[2] , sys.argv[3], sys.argv[4], sys.argv[5]])
        for i in range(0,120):
            if os.path.isfile('history_'+str(i)+'.json'):
                with open('history_'+str(i)+'.json') as f:
                    history = json.load(f) 
                    res = requests.post(url = API_ENDPOINT, json = { 'auth' : API_KEY, 'data' : history }, headers=headers)
            else:
                break
        sys.exit(1)

    for i in range(0,30):
        with urllib.request.urlopen("http://192.168.10.32:8080/data.json") as url:
            data = json.loads(url.read().decode())
            print("read json aircraft..")
            for aircraft in data:
                aircraft['unixtime'] = int(pre_time)
                aircraft['node_number'] = sys.argv[3]
                if all(x in aircraft for x in ("lat","lon","flight","altitude")):
                    if aircraft['validposition'] == 1 and aircraft['flight'] != "" and aircraft['flight'] != "????????":
                        adsb.append(aircraft)
        sleep(1)
    with open('history_'+str(filenumber)+'.json', 'w') as outfile:
        json.dump(adsb, outfile)
        print("created "+str(filenumber))
    filenumber = filenumber + 1
    if filenumber == 120:
        filenumber = 0
   