import serial
import urllib.request, json
import sys
import requests
from time import sleep, time
API_ENDPOINT = "http://"+sys.argv[1]+":"+sys.argv[2]+"/putdata"
API_KEY = sys.argv[4]+"@"+sys.argv[5];
headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
while True:
    data = {}
    pre_time = time()
    # print(pre_time)
    # r = requests.get(url="http://192.167.10.18:8080/data.json")
    # print(r.json())
    try:
        
        with urllib.request.urlopen("http://127.0.0.1:8080/data.json") as url:
            adsb = []
            data = json.loads(url.read().decode())
            print("read json aircraft..")
            print(data)
            for aircraft in data:
                aircraft['unixtime'] = int(pre_time)
                aircraft['node_number'] = sys.argv[3]
                if all(x in aircraft for x in ("lat","lon","flight","altitude")):
                    if aircraft['validposition'] == 1:
                        adsb.append(aircraft)
            
            res = requests.post(url = API_ENDPOINT, json = { 'auth' : API_KEY, 'data' : adsb }, headers=headers)
            print("status : "+str(res))
            print(str(aircraft['unixtime'])+" send "+str(time()))
        print("1 jps(json per second) file in " + str(time()-pre_time) +" seconds")
    except urllib.error.URLError:
        print("connection lost, try to connect")
    except requests.exceptions.ConnectionError:
        print("can't connect server")
    except:
        print("an error occured")
    else:
        print("running without error")
    sleep(1)
