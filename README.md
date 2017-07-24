# 15 x 9 LED art

## Reminders:
- Upload remote file from touchOSC app!!
- Add pictures and videos
- Add type of leds
- add power info 
- Add links to all software
- Upload fadecandy config
- Spell check this document

## Description:
#### Software:
This is the software for my 15 x 9 LED wall. Anyone is welcome to use this software, however I am creating this github page as a repository for me to work out of for this project and to come back to the software should my Raspberry Pi have a major malfunction. Over time I hope to add some pictures and videos, as well as clean up the code. I have addapted bits and peices of the code from other people and I have tried to give credit as best I can remember, if you see some of your code here please let me know because I would love to give you credit for it. 

The project is centered around the main.py python script. It uses the Open Pixel Connection (OPC) library to talk to the fadecandy server. The main.py also calls up an Open Sound Control (OSC) server to listen to commands sent from the touchOSC iphone app.

#### Hardware:
This matrix is composed of three strings of 45 LEDs each, each zigzaged into 3 rows of 15. The each pixel was hand soldered to create a 4 inch space between each LED. The three strings are connected to a fadecandy board, and then to a Raspberry Pi. There is also a USB mic for capturing audo for live music interaction. 


## How To:
Remember how to do this in case of a pi faliure or you have to reproduce this in the future. 


#### Create bootable SD for the Pi
I used the minimal image as it doesn't have a Graphical User Interface (gui) or extras and I figured it should be faster. 

This is on a mac: 

Use `df -h` or `diskutil list` to see mounted paths. The disk may show up as something like "/disk2s1" you can ignore the "s1" You will need to unmount the drive, I can't remember the command off the top of my head, you can just use the disk utility.

`sudo dd if=[/path/to/image] of=/dev/rdisk[n] bs=512k`
 
Ctl + t to check the status

"rdisk" is much faster than just "disk" - it doesn’t buffer

#### Change Raspberry Pi configuration:
`sudo raspi-config`
- Enable autologin
- Change password
- Change hostname (piledwall)
- Enable SSH (if you don't know how to secure SSH, you should google a tutorial)

#### Set up wifi via command line:
`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

Add the following to the bottom of the file replacing "testing" and "password" with your SSID and WIFI password. (keep the quotes e.g. ssid="myNetwork"
```
network={
    ssid="testing"
    psk="Password"
}
```
Then `sudo reboot`

#### Instal tools:
- `sudo apt-get install git`
- `sudo apt-get install Pure-FTPd` (This will work as is, but you probably should google how to secure it)

#### Install fadecandy server:
`git clone https://github.com/scanlime/fadecandy.git`
- We should put this into the same folder as the rest of our project, so that it will work with the launch scripts later
- Also don't forget to add the fcserver15x9.json to the bin folder

#### Install Python libraries:
##### Tools:
```
sudo apt-get install python-setuptools
sudo apt-get install python-pip
sudo apt-get install python-dev
```
##### Modules:
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

#### Audio:
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
		













