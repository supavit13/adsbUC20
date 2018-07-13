import serial
import urllib.request, json
import sys
import requests
import socket
import os
from subprocess import call
from time import sleep, time
API_ENDPOINT = "http://"+sys.argv[1]+":"+sys.argv[2]+"/putdata"
API_KEY = sys.argv[4]+"@"+sys.argv[5];
headers = {'Content-Type': 'application/json', 'Accept':'application/json'}

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

def when_lost():
    filenumber = 0
    while True:
        data = {}
        pre_time = time()
        adsb = []
        if check_internet():
            print("on")
            for i in range(0,120):
                if os.path.isfile('history_'+str(i)+'.json'):
                    with open('history_'+str(i)+'.json') as f:
                        history = json.load(f) 
                        res = requests.post(url = API_ENDPOINT, json = { 'auth' : API_KEY, 'data' : history }, headers=headers)
                else:
                    return

        for i in range(0,30):
            with urllib.request.urlopen("http://127.0.0.1:8080/data.json") as url:
            # with urllib.request.urlopen("http://164.115.43.87:8080/api") as url:
                data = json.loads(url.read().decode())
                print("read json aircraft..")
                for aircraft in data:
                    aircraft['unixtime'] = int(time())
                    aircraft['node_number'] = sys.argv[3]
                    if all(x in aircraft for x in ("lat","lon","flight","altitude")):
                        if  aircraft['flight'] != "" and aircraft['flight'] != "????????" and aircraft['validposition'] == 1:
                            adsb.append(aircraft)
            sleep(1)
        with open('history_'+str(filenumber)+'.json', 'w') as outfile:
            json.dump(adsb, outfile)
            print("created "+str(filenumber))
        filenumber = filenumber + 1
        if filenumber == 120:
            filenumber = 0
while True:
    data = {}
    pre_time = time()
    if check_internet():
        print("on")
    else:
        print("off")
        when_lost()
        
    try:
        
        with urllib.request.urlopen("http://127.0.0.1:8080/data.json") as url:
        # with urllib.request.urlopen("http://164.115.43.87:8080/api") as url:
            adsb = []
            data = json.loads(url.read().decode())

            print("read json aircraft..")
            print(data)
            for aircraft in data:
                aircraft['unixtime'] = int(pre_time)
                aircraft['node_number'] = sys.argv[3]
                if all(x in aircraft for x in ("lat","lon","flight","altitude")):
                    if aircraft['flight'] != "" and aircraft['flight'] != "????????" and aircraft['validposition'] == 1:
                        adsb.append(aircraft)
            
            res = requests.post(url = API_ENDPOINT, json = { 'auth' : API_KEY, 'data' : adsb }, headers=headers)
            print("status : "+str(res))
            print(str(aircraft['unixtime'])+" send "+str(time()))
        print("1 jps(json per second) file in " + str(time()-pre_time) +" seconds")
    except urllib.error.URLError:
        print("adsb lost, try to connect") # adsb lost
    except requests.exceptions.ConnectionError:
        print("can't connect webserver") # internet lost
        
    except:
        print("an error occured")
    else:
        print("running without error")
    sleep(1)
