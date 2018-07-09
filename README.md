# adsbUC20

## requirement
- python
- dump1090 K2DLS
- 3G Hat expansion for raspberry pi
- raspberry pi
- Sakis3G
- umtskeeper
## installation
- connect RTL-SDR usb and 3G hat on RPi
- install python , dump1090 , Sakis3G and umtskeeper
- config umtskeeper , dump1090 and reboot pi
## run on startup
- sudo crontab -e
add command to run script

  @reboot python3 file.py [IP] [PORT] [NODE_NUMBER] &
  
- sudo nano /etc/rc.local
add command between fi and exit 0

  /home/pi/Download/modem/umtskeeper --sakisoperators "OTHER='CUSTOM_TTY' CUSTOM_TTY='/dev/ttyUSB3' APN='CUSTOM_APN' CUSTOM_APN='internet' APN_USER='0' APN_PASS='0'" --sakisswitches "--sudo --console" --devicename 'Quectel' --log --silent --monthstart 8 --nat 'no' --httpserver &>> /home/pi/Downloads/modem/err.log &
  
  
