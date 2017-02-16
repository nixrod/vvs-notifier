#VVS Notifier

*Note that this project is a work in progress, the documentation will be enhanced as the project grows*

This project runs on a raspberry pi.
It connects to the vvs twitter and checks for current service outages.
Also it connects to the vvs web api to fetch the departure times for a specific station
This information is displayed on a HD44780 display.
The script is triggered through a motion sensor.

run background script with `sudo /etc/init.d/vvs_notifier.sh start | stop | status`

##Python Script Installation
Add a config.ini file to the root of the project with the following twitter info: (configure your app at https://apps.twitter.com/)
```
[twitter]
ConsumerKey = <your_consumer_key>
ConsumerSecret = <your_consumer_secret>
AccessTokenKey = <your_access_token_key>
AccessTokenConfig = <your_access_token_config>
```
##Used GPIO Pins (mode=GPIO.BOARD)

PIR:

color | function | GPIO Pin
--- | --- | ---
red   |  VCC 5V   |   4
brown |  Out 3.3V |   14
black |  Ground   |   18


DISPLAY:

color | function | GPIO Pin
--- | --- | ---
brown | vss, Ground | 25
orange | vdd, 5V | Breadboard
red | v0, Ground | 30
orange | rs | 26
yellow | rw | 38
green | e | 29
blue | d4 | 31
violet | d5 | 32
grey | d6 | 33
white | d7 | 35
yellow | a 5V | Breadboard
black | k Gnd | Breadboard
orange | bgcrtl | 36

### Optional LED support (start & join LED thread in app.py)
LED:

color | function | GPIO Pin
--- | --- | ---
orange  |S1         | 7
yellow  |S2         | 11
brown   |S3         | 12
grey    |S4         | 13
blue    |S5         | 15
white   |S6         | 16
red     |VCC 5V     | 2
black   |Ground     | 9