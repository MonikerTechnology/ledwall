# version_3.0 in progress
# 15 x 9 LED art

![alt text](v2/supporting_files/ledwall.gif "ledwall in action")

This project is under a major redevelopment. I no longer have a space for the LED board so I am donating it to a friend. The main goals for this version are to streamline and simplify. The main interface for changing patterns and settings will be the http server. Decisions need to be made regarding how this device can be controlled and maintained from a non-technical person. Physical controls are being considered. 

## Goals for v3
- [ ] Simplify 
- [ ] Increased error handling 
- [ ] Better maintenance of wifi
- [ ] Indicators
  - [ ] Wifi good
  - [ ] Wifi issue
  - [ ] Test all LEDs and Colors on boot
  - [ ] All LEDs on


## Goals for v2.0
- [x] Python3
- [ ] Error handling
  - [x] Auto restart of services
  - [ ] No audio - broken
   - [ ] Lack of sound then display something cool
  -  [ ] No wifi - loading pattern
  - [x] No OSC
- [ ] HTML wifi set up - auto scan then broadcast if not connected
  - [ ] Physica button??
- [x] Better start up pattern / test pattern
- [x] Mirate to http post for control
  - [ ] Add HTTPS
  - [ ] Add sha256 auth key
  - [x] HomeKit- HAP-Node.js to many local scripts
    - [ ] Homekit QR code for pairing
    - [ ] HAP-Node.js feedback so the buttons are active
  - [ ] Secondary control….physical? (prolly naw)
    - [x] Google Assistant
- [ ] More/better audio effects
- [x] Update github
- [ ] Cool MOTD ssh banner
- [ ] HTML status page...mayble with controls
- [ ] Linux auto updates (security)


## Reminders:
- [x] Add pictures and videos
- [ ] Add type of LEDs
- [ ] add power info 
- [ ] Add links to all software
- [x] Upload FadeCandy config
- [ ] Spell check this document

## Description:
### Software:
This is the software for my 15 x 9 LED wall. Anyone is welcome to use this software, however, I am creating this GitHub page as a repository for me to work out of for this project and to come back to the software should my Raspberry Pi have a major malfunction. Over time I hope to add some pictures and videos, as well as clean up the code. I have adapted bits and pieces of the code from other people and I have tried to give credit as best I can remember. If you see some of your code here please let me know because I would love to give you credit for it. 

The project is centered around the main.py python script. It uses the Open Pixel Connection (OPC) library to talk to the FadeCandy server. The main.py also calls up an Open Sound Control (OSC) server to listen to commands sent from the TouchOSC iPhone app.

### Hardware:
This matrix is composed of three strings of 45 LEDs each, each zigzagged into 3 rows of 15. The each pixel was hand soldered to create a 4-inch space between each LED. The three strings are connected to a FadeCandy board, and then to a Raspberry Pi. There is also a USB mic for capturing audio for live music interaction. 


## How To:
Remember how to do this in the case of a Pi failure or you have to reproduce this in the future. 



### Instal tools:
- `sudo apt-get install git`
- `sudo apt-get install Pure-FTPd` (This will work as is, but you probably should google how to secure it)



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

What you need to do:

Uninstall python-pyaudio with sudo apt-get purge --remove python-pyaudio if you have it (This is version 0.2.8)
Download the latest version (19) of PortAudio.
Untar and install PortAudio
./configure
make
make install
Get the dependencies for pyaudio
portaudio19-dev
python-all-dev (python3-all-dev for Python 3)
sudo pip install pyaudio
After that, I was able to use pyaudio.



Fory python3
```
sudo apt-get install python3-pip
```

#### Modules:

Python3 
```
sudo pip3 install aubio
sudo python3 -m pip install numpy
sudo apt-get install python3-pyaudio
sudo pip3 install dweepy
```
    
```
git clone https://github.com/ptone/pyosc.git
sudo ./setup.py install
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












