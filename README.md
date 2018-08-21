# adsbUC20

## requirement
- python
- dump1090 K2DLS https://www.k2dls.net/blog/tag/dump1090/
- 3G Hat expansion for raspberry pi
- raspberry pi 
- Sakis3G
- umtskeeper
- watchdog
- remot3.it
## installation
- connect RTL-SDR usb and 3G hat on RPi
- install python , dump1090 , Sakis3G , remot3 and umtskeeper
- config umtskeeper , remot3 , dump1090 and reboot pi
## run on startup
```
sudo crontab -e
```
add command to run script

```
@reboot sudo python3 /home/pi/adsbUC20/By3G/By3G.py [IP] [PORT] [NO] [KEY] [SECRET] &
@reboot python3 /home/pi/adsbUC20/temperature.py &
59 23 * * * rm -f /home/pi/history_*
0 0 * * * sudo reboot
*/5 * * * * python3 /home/pi/adsbUC20/adsbcheck.py
* * * * * python3 /home/pi/adsbUC20/running.py
```
add command to run modem 3G
```
sudo nano /etc/rc.local
```

add command between fi and exit 0

```
/home/pi/Download/modem/umtskeeper --sakisoperators "OTHER='CUSTOM_TTY' CUSTOM_TTY='/dev/ttyUSB3' APN='CUSTOM_APN' CUSTOM_APN='internet' APN_USER='0' APN_PASS='0'" --sakisswitches "--sudo --console" --devicename 'Quectel' --log --silent --monthstart 8 --nat 'no' --httpserver &>> /home/pi/Downloads/modem/err.log &
```
  
  
