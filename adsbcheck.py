import urllib.request, json # for http request and json en/decoder
import sys #for argument
import requests # request response
import os # files management
from subprocess import call 
from time import sleep, time
from datetime import datetime
import logging
try:
    with urllib.request.urlopen("http://127.0.0.1:8080/data.json") as url:
        data = json.loads(url.read().decode())
        print(data)
except:
    print("dump1090.service failed.")
    os.popen('sudo systemctl restart dump1090.service')