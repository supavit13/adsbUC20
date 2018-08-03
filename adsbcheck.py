import urllib.request, json # for http request and json en/decoder
import sys #for argument
import requests # request response
import os # files management
from subprocess import call 
from time import sleep, time
from datetime import datetime
import logging
try:

    o = requests.get('127.0.0.1:8080/data.json')
    print(o.json())
except:
    print("failed")
    os.popen('sudo systemctl restart dump1090.service')

# if o.find("fail") == -1:
#     print("running")
# else:
#     print(fail)
#     os.popen('sudo systemctl restart dump1090.service')
    