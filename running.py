import urllib.request, json # for http request and json en/decoder 
import sys #for argument
import requests # request response 
import os # files management from subprocess  
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
    logging.info('Script Checker starting...')
else:
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/home/pi/checking.log',
                     filemode='w')
    logging.debug('Script Checker starting...')
    logging.info('Create file checking.log')

o =os.popen("ps ax | grep By").read()
print(o.find("adsbUC20"))
err = o.find("adsbUC20")
if err == -1:
	logging.warning("not found script")
	# os.popen("sudo pkill -f By3G.py")
	# sleep(0.1)
	os.popen("sudo python3 /home/pi/adsbUC20/By3G/By3G.py 164.115.43.87 8080 1 Vimt29H2p9 5b45b88c96f2234c3b3a8151 &")
else:
	logging.info("script running")
#sudo python3 /home/pi/adsbUC20/By3G/By3G.py 164.115.43.87 80
#80 1 Vimt29H2p9 5b45b88c96f2234c3b3a8151
