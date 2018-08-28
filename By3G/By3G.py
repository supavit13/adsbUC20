import urllib.request, json # for http request and json en/decoder
import sys #for argument
import requests # request response
import os # files management
from subprocess import call 
from time import sleep, time
from datetime import datetime
import logging
API_ENDPOINT = "http://"+sys.argv[1]+":"+sys.argv[2]+"/putdata" # ip webserver
API_KEY = sys.argv[4]+"@"+sys.argv[5]; # key and secret on webserver
headers = {'Content-Type': 'application/json', 'Accept':'application/json'} #set header for http request
if os.path.isfile('/home/pi/myapp.log'):
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/home/pi/myapp.log',
                    filemode='a')
    logging.debug('ADS-B Receiver starting...')
    logging.info('Test log info')
    logging.warning('Test log warning')
else:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename='/home/pi/myapp.log',
                        filemode='w')
    logging.debug('ADS-B Receiver starting...')
    logging.info('Test log info')
    logging.warning('Test log warning')
        


def check_internet(): # check internet connection
    url=API_ENDPOINT
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        logging.warning(" internet or webserver lost connection")
        return False
    except requests.exceptions.ReadTimeout:
        logging.warning(" timeout")
        return False

def checklog():
    if os.path.isfile('/home/pi/myapp.log') and os.path.getsize("/home/pi/myapp.log") >= 10000000:
        open("/home/pi/myapp.log", "w").close()
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s',
                            filename='/home/pi/myapp.log',
                            filemode='w')
        logging.debug('A debug message')
        logging.info('Some information')
        logging.warning('A shot across the bows')
def when_lost(): # backup to file history_0 - history_119
    filenumber = 0
    while True:
        data = {}
        pre_time = time()
        adsb = []
        if check_internet():
            logging.info(" on")
            for i in range(0,60):
                if os.path.isfile('history_'+str(i)+'.json'):
                    with open('history_'+str(i)+'.json') as f:
                        history = json.load(f) 
                        try:
                            res = requests.post(url = API_ENDPOINT, json = { 'auth' : API_KEY, 'data' : history }, headers=headers)
                        except:
                            logging.warning(" cannot post backup data to server")
                else:
                    break
            o=os.popen('rm -f /home/pi/history_*').read()
            return
        try:
            for i in range(0,10):
                checklog()
                with urllib.request.urlopen("http://127.0.0.1:8080/data.json") as url:
                # with urllib.request.urlopen("http://164.115.43.87:8080/data/aircraft.json") as url:
                    data = json.loads(url.read().decode())
                    logging.info(" read json aircraft.. for write file")
                    for aircraft in data:
                        aircraft['unixtime'] = int(time())
                        aircraft['node_number'] = sys.argv[3]
                        adsb.append(aircraft)
                        # if all(x in aircraft for x in ("lat","lon","flight","altitude")):
                        #     if aircraft['flight'] != "" and aircraft['flight'] != "????????" and aircraft['validposition'] == 1:
                        #     # if aircraft['flight'] != "" and aircraft['flight'] != "????????":
                        #         adsb.append(aircraft)
                sleep(1)
            with open('history_'+str(filenumber)+'.json', 'w') as outfile:
                json.dump(adsb, outfile)
                logging.info(" created "+str(filenumber))
            filenumber = filenumber + 1
            if filenumber == 60:
                filenumber = 0
        except:
            logging.warning(" cannot get data from adsb or cannot save file history")

while True:
    data = {}
    pre_time = time()
    logging.info(os.path.getsize("/home/pi/myapp.log"))
    checklog()
    if check_internet():
        logging.info(" on")
    else:
        logging.info(" off")
        # when_lost()
        
    try:
        
        with urllib.request.urlopen("http://127.0.0.1:8080/data.json") as url:
        # with urllib.request.urlopen("http://164.115.43.87:8080/data/aircraft.json") as url:
            adsb = []
            data = json.loads(url.read().decode())

            logging.info(" read json aircraft..")
            # print(" data is")
            # print(data)
            for aircraft in data:
                aircraft['unixtime'] = int(pre_time)
                aircraft['node_number'] = sys.argv[3]
                adsb.append(aircraft)
                # if all(x in aircraft for x in ("lat","lon","flight","altitude")):
                #     if aircraft['flight'] != "" and aircraft['flight'] != "????????" and aircraft['validposition'] == 1:
                #     # if aircraft['flight'] != "" and aircraft['flight'] != "????????":
                #         adsb.append(aircraft)
            
            res = requests.post(url = API_ENDPOINT, json = { 'auth' : API_KEY, 'data' : adsb }, headers=headers)
            logging.info(" status : "+str(res))
            logging.info(" "+str(aircraft['unixtime'])+" send "+str(time()))
        logging.info(" 1 jps(json per second) file in " + str(time()-pre_time) +" seconds")
    except urllib.error.URLError:
        logging.warning(" adsb lost, try to connect") # adsb lost
    except requests.exceptions.ConnectionError:
        logging.warning(" can't connect webserver") # internet lost
        
    except:
        logging.warning(" an error occured")
    else:
        logging.info(" running without error")
    sleep(1)
