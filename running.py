import urllib.request, json # for http request and json en/decoder 
import sys #for argument
import requests # request response 
import os # files management from subprocess  
from time import sleep, time 
from datetime import datetime 
import logging 

o =os.popen("ps ax | grep By").read()
print(o.find("adsbUC20"))
err = o.find("adsbUC20")
if err != -1:
	print("error")
	# os.popen("sudo pkill -f By3G.py")
	# sleep(0.1)
	# os.popen("sudo python3 /home/pi/adsbUC20/By3G/By3G.py 164.115.43.87 8080 1 Vimt29H2p9 5b45b88c96f2234c3b3a8151 &")
else:
	print("not error")
#sudo python3 /home/pi/adsbUC20/By3G/By3G.py 164.115.43.87 80
#80 1 Vimt29H2p9 5b45b88c96f2234c3b3a8151
