import urllib.request, json # for http request and json en/decoder
import sys #for argument
import requests # request response
import os # files management
from subprocess import call 
from time import sleep, time
from datetime import datetime
API_ENDPOINT = "http://"+sys.argv[1]+":"+sys.argv[2]+"/putdata" # ip webserver
API_KEY = sys.argv[4]+"@"+sys.argv[5]; # key and secret on webserver
headers = {'Content-Type': 'application/json', 'Accept':'application/json'} #set header for http request
sys.stdout = open('/home/pi/log.txt', 'w') # set file log

        
class Tee(object): # class about write log file
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj) # write file
            f.flush() #show content file realtime

f = open('/home/pi/log.txt', 'w')
backup = sys.stdout
sys.stdout = Tee(sys.stdout, f)

def check_internet(): # check internet connection
    url=API_ENDPOINT
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print(str(datetime.now())+" internet or webserver lost connection")
        return False
    except requests.exceptions.ReadTimeout:
        print(str(datetime.now())+" timeout")
        return False

def checklog():
    if os.path.isfile('/home/pi/log.txt') and os.path.getsize("/home/pi/log.txt") >= 50000000: # if file size more than 50 MB then delete file log and create again
        open("/home/pi/log.txt", "w").close()
        sys.stdout = open('/home/pi/log.txt', 'w') 
        f = open('/home/pi/log.txt', 'w')
        backup = sys.stdout
        sys.stdout = Tee(sys.stdout, f)
def when_lost(): # backup to file history_0 - history_119
    filenumber = 0
    while True:
        data = {}
        pre_time = time()
        adsb = []
        if check_internet():
            print(str(datetime.now())+" on")
            for i in range(0,120):
                if os.path.isfile('history_'+str(i)+'.json'):
                    with open('history_'+str(i)+'.json') as f:
                        history = json.load(f) 
                        res = requests.post(url = API_ENDPOINT, json = { 'auth' : API_KEY, 'data' : history }, headers=headers)
                else:
                    break
            return

        for i in range(0,30):
            checklog()
            with urllib.request.urlopen("http://127.0.0.1:8080/data.json") as url:
            # with urllib.request.urlopen("http://164.115.43.87:8080/api") as url:
                data = json.loads(url.read().decode())
                print(str(datetime.now())+" read json aircraft..")
                for aircraft in data:
                    aircraft['unixtime'] = int(time())
                    aircraft['node_number'] = sys.argv[3]
                    if all(x in aircraft for x in ("lat","lon","flight","altitude")):
                        if  aircraft['flight'] != "" and aircraft['flight'] != "????????" and aircraft['validposition'] == 1:
                            adsb.append(aircraft)
            sleep(1)
        with open('history_'+str(filenumber)+'.json', 'w') as outfile:
            json.dump(adsb, outfile)
            print(str(datetime.now())+" created "+str(filenumber))
        filenumber = filenumber + 1
        if filenumber == 120:
            filenumber = 0

while True:
    data = {}
    pre_time = time()
    print(os.path.getsize("/home/pi/log.txt"))
    checklog()
    if check_internet():
        print(str(datetime.now())+" on")
    else:
        print(str(datetime.now())+" off")
        when_lost()
        
    try:
        
        with urllib.request.urlopen("http://127.0.0.1:8080/data.json") as url:
        # with urllib.request.urlopen("http://164.115.43.87:8080/api") as url:
            adsb = []
            data = json.loads(url.read().decode())

            print(str(datetime.now())+" read json aircraft..")
            # print(str(datetime.now())+" data is")
            # print(data)
            for aircraft in data:
                aircraft['unixtime'] = int(pre_time)
                aircraft['node_number'] = sys.argv[3]
                if all(x in aircraft for x in ("lat","lon","flight","altitude")):
                    if aircraft['flight'] != "" and aircraft['flight'] != "????????" and aircraft['validposition'] == 1:
                        adsb.append(aircraft)
            
            res = requests.post(url = API_ENDPOINT, json = { 'auth' : API_KEY, 'data' : adsb }, headers=headers)
            print(str(datetime.now())+" status : "+str(res))
            print(str(datetime.now())+" "+str(aircraft['unixtime'])+" send "+str(time()))
        print(str(datetime.now())+" 1 jps(json per second) file in " + str(time()-pre_time) +" seconds")
    except urllib.error.URLError:
        print(str(datetime.now())+" adsb lost, try to connect") # adsb lost
    except requests.exceptions.ConnectionError:
        print(str(datetime.now())+" can't connect webserver") # internet lost
        
    except:
        print(str(datetime.now())+" an error occured")
    else:
        print(str(datetime.now())+" running without error")
    sleep(1)
