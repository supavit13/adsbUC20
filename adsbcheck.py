import urllib.request, json # for http request and json en/decoder
import sys #for argument
import requests # request response
import os # files management
from subprocess import call 
from time import sleep, time
from datetime import datetime
import logging
o = os.popen('curl 127.0.0.1:8080/data.json').read()
fail = "Failed"
print(o.find(fail))
if o.find(fail) == -1:
    print("running")
else:
    print(fail)
    os.popen('sudo systemctl restart dump1090.service')
    