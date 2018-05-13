# version_2.0 in progress (did it upload?)
# 15 x 9 LED art

## Goals for v2.0
- Error handling
  - No audio - broken
   - Lack of sound then display something cool
  -  No wifi - loading pattern
  - No OSC
- HTML wifi set up - auto scan then broadcast if not connected
  - Physica button??
- Better start up pattern / test pattern
- HomeKit- bridge to many local scripts
  - MQTT --> Migrate to something more vanila...get and post with json?
  - Secondary control….physical? (prolly naw)
    - Google Assistant
- More/better audio effects
- Update github
- Cool MOTD ssh banner
- More secure?


## Reminders:
- Upload remote file from TouchOSC app!!
- Add pictures and videos
- Add type of LEDs
- add power info 
- Add links to all software
- Upload FadeCandy config
- Spell check this document

## Description:
### Software:
This is the software for my 15 x 9 LED wall. Anyone is welcome to use this software, however, I am creating this GitHub page as a repository for me to work out of for this project and to come back to the software should my Raspberry Pi have a major malfunction. Over time I hope to add some pictures and videos, as well as clean up the code. I have adapted bits and pieces of the code from other people and I have tried to give credit as best I can remember. If you see some of your code here please let me know because I would love to give you credit for it. 

The project is centered around the main.py python script. It uses the Open Pixel Connection (OPC) library to talk to the FadeCandy server. The main.py also calls up an Open Sound Control (OSC) server to listen to commands sent from the TouchOSC iPhone app.

### Hardware:
This matrix is composed of three strings of 45 LEDs each, each zigzagged into 3 rows of 15. The each pixel was hand soldered to create a 4-inch space between each LED. The three strings are connected to a FadeCandy board, and then to a Raspberry Pi. There is also a USB mic for capturing audio for live music interaction. 


## How To:
Remember how to do this in the case of a Pi failure or you have to reproduce this in the future. 


### Create bootable SD for the Pi:
I used the minimal image as it doesn't have a Graphical User Interface (GUI) or extras and I figured it should be faster. 

This is on a mac: 

Use `df -h` or `diskutil list` to see mounted paths. The disk may show up as something like "/disk2s1" you can ignore the "s1" You will need to unmount the drive, I can't remember the command off the top of my head, you can just use the disk utility.

`sudo dd if=[/path/to/image] of=/dev/rdisk[n] bs=512k`
 
Ctrl + t to check the status

"rdisk" is much faster than just "disk" - it doesn’t buffer

### Change Raspberry Pi configuration:
`sudo raspi-config`
- Enable autologin
- Change password
- Change hostname (piledwall)
- Enable SSH (if you don't know how to secure SSH, you should google a tutorial)

### Set up wifi via command line:
`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

Add the following to the bottom of the file replacing "testing" and "password" with your SSID and WIFI password. (keep the quotes e.g. ssid="myNetwork"
```
network={
    ssid="testing"
    psk="Password"
}
```
Then `sudo reboot`

### Instal tools:
- `sudo apt-get install git`
- `sudo apt-get install Pure-FTPd` (This will work as is, but you probably should google how to secure it)


### Install Everything for HomeKit

#### HAP-nodeJS
- https://github.com/KhaosT/HAP-NodeJS

.service file for HAP-NodeJS
```
#
#Place this file in /etc/systemd/system/name_of_file.service
#
#
#Here are some example commands 
#	sudo systemctl status -l name_of_file.service
#	sudo systemctl enable name_of_file.service
#	sudo systemctl stop name_of_file.service
#   	sudo systemctl start name_of_file.service
#   	journalctl -u name_of_file.service

[Unit] 
Description=HAP-NodejS 

[Service] 
Type=simple

#Everything must use absolute path
WorkingDirectory=/home/pi/HAP-NodeJS 
ExecStartPre=/bin/echo "hap-nodejs.service started" 
ExecStart=/usr/bin/node /home/pi/HAP-NodeJS/BridgedCore.js 
ExecStop=/bin/echo "hap-nodejs.services stopped" 

[Install]
WantedBy=multi-user.target
```

#### MQTT
- Mosquitto (maybe not needed? def good for testing)
  - https://mosquitto.org/2013/01/mosquitto-debian-repository/
  - if you need an updated repo
    - 	sudo wget http://repo.mosquitto.org/debian/mosquitto-stretch.list
- MQTT for node or npm or something? Needed for HAP-NodeJS
  - sudo npm install node
- Local client for testing
  - apt-get install mosquitto mosquitto-clients 
- To test open two terminals and enter the following:
  - mosquitto_sub -t "/test/topic"
  - mosquitto_pub -t "/test/topic" -m "HELLO"



### Install FadeCandy server:
`git clone https://github.com/scanlime/fadecandy.git`
- We should put this into the same folder as the rest of our project so that it will work with the launch scripts later
- Also, don't forget to add the fcserver15x9.json to the bin folder

### Install Python libraries:
##### Tools:
```
sudo apt-get install python-setuptools
sudo apt-get install python-pip
sudo apt-get install python-dev
```
#### Modules:
```
sudo apt-get install python-pyaudio
```
```
sudo apt-get install aubio-tools libaubio-dev libaubio-doc
```
```
python -m pip install aubio
```
    
    
```
git clone https://github.com/ptone/pyosc.git
sudo ./setup.py install
```

**If installing on a Mac use these instead:**
```
sudo easy_install aubio
sudo easy_install pyaudio
```

### Audio:
Change the following two lines in /usr/share/alsa/alsa.conf
```        
defaults.ctl.card 0
defaults.pcm.card 0
```    
use `sudo nano /usr/share/alsa/alsa.conf`
```  
defaults.ctl.card 1
defaults.pcm.card 1
```        

Create or edit the file `/etc/modprobe.d/alsa-base.conf` and add the following 
```        
pcm.!default {
    type hw
    card 1
}
ctl.!default {
    type hw
    card 1
}
```

### Create systemd service:
I am no expert here, but this is what I pulled together and it works great. It starts up on boot, and can easily be killed.(Using ctrl-c doesn't work here because the program starts a few threads.  
`pi@piledwall:~ $ sudo nano /etc/systemd/system/ledwall.service`
```
    [Unit]
    Description=Power-On-LEDwall
    
    [Service]
    Type=forking
    ExecStart=/usr/bin/ledwall.sh
    
    
    [Install]
    WantedBy=multi-user.target
```
The ExecStart path will point to the script that will start the FadeCandy server and main.py
- Here are some example commands 
```
    sudo systemctl status -l ledwall
    sudo systemctl enable ledwall
    sudo systemctl stop ledwall
    sudo systemctl start ledwall
```
Then create the scrip. Note that there a few file pathes that may need to be updated to fit your situation.
`pi@piledwall:~ $ sudo nano /usr/bin/ledwall.sh`
```
#!/bin/sh
sleep 10
echo "Starting Fadecandy Server..."
sudo /home/pi/project/fadecandy/bin/fcserver-rpi /home/pi/project/fadecandy/bin/fcserver_config.json &
#&>> /home/pi/project/log.txt &
echo "Fadecandy started"
echo ""
echo "Starting python..."
echo "changing directory to ...projects"
cd /home/pi/project/
sudo /usr/bin/python /home/pi/project/main.py --layout=/home/pi/project/ledwall15x9.json &
#&>> /home/pi/project/log.txt &
echo "Python started"
```












