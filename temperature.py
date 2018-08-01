import sys #for argument
import os # files management
from time import sleep, time
from datetime import datetime
import logging
if os.path.isfile('/home/pi/temperature.log'):
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/home/pi/temperature.log',
                    filemode='a')
    logging.debug('Temperature log starting...')
    logging.info('Test log info')
    logging.warning('Test log warning')
else:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename='/home/pi/temperature.log',
                        filemode='w')
    logging.debug('Temperature log starting...')
    logging.info('Test log info')
    logging.warning('Test log warning')
err = ""
maxtemp = 0.0
while 1:
    if os.path.isfile('/home/pi/temperature.log') and os.path.getsize("/home/pi/temperature.log") >= 100000000: # if file size more than 50 MB then delete file log and create again
        open("/home/pi/temperature.log", "w").close()
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s',
                            filename='/home/pi/temperature.log',
                            filemode='w')
        logging.debug('Temperature log new file...')
        logging.info('Test log info')
        logging.warning('Test log warning')

    o=os.popen('vcgencmd measure_temp').read()
    temp=o.split('=')[1]
    temp=float(temp.split("'")[0])
    if temp > maxtemp:
        maxtemp = temp
        logging.warning("Max temperature : "+str(temp))
    logging.info(o)
    o=os.popen('dmesg | grep 0x00050005 | tail -1').read()
    if err == "":
        err = o
        logging.warning(err)
    elif err != "" and err != o:
        err = o
        logging.warning(err)
    sleep(1)