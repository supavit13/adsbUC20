import urllib.request, json # for http request and json en/decoder
import sys #for argument
import requests # request response
import os # files management
from subprocess import call 
from time import sleep, time
from datetime import datetime
import logging
if os.path.isfile('/home/pi/checking.log') and os.path.getsize("/home/pi/checking.log") >= 10000000:
    open("/home/pi/checking.log", "w").close()
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/home/pi/checking.log',
                    filemode='w')
if os.path.isfile('/home/pi/checking.log'):
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/home/pi/checking.log',
                    filemode='a')
    logging.info('ADS-B Checker starting...')
else:
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/home/pi/checking.log',
                     filemode='w')
    logging.debug('ADS-B Checker starting...')
    logging.info('Create file checking.log')
try:
    o = requests.get('http://127.0.0.1:8080/data.json')
    logging.debug('ADS-B Checker : Not error...')
    print(o.json())
except:
    logging.debug('ADS-B Checker : dump1090.service error restart now')
    os.popen('sudo systemctl restart dump1090.service')
    os.popen('sudo systemctl start dump1090.service')
try:
    urllib.request.urlopen("https://www.google.com/")
except urllib.error.URLError:
    logging.warning("Network down")
    logging.warning("reboot now")
    os.popen('sudo reboot')
else:
    logging.info("Up and running")

# if o.find("fail") == -1:
#     print("running")
# else:
#     print(fail)
#     os.popen('sudo systemctl restart dump1090.service')
    