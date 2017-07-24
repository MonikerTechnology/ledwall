# 15 x 9 LED art

## Reminders:
- Upload remote file from touchOSC app!!
- Add pictures and videos


## Description:
#### Software:
This is the software for my 15 x 9 LED wall. Anyone is welcome to use this software, however I am creating this github page as a repository for me to work out of for this project and to come back to the software should my Raspberry Pi have a major malfunction. Over time I hope to add some pictures and videos, as well as clean up the code. I have addapted bits and peices of the code from other people and I have tried to give credit as best I can remember, if you see some of your code here please let me know because I would love to give you credit for it. 

The project is centered around the main.py python script. It uses the Open Pixel Connection (OPC) library to talk to the fadecandy server. The main.py also calls up an Open Sound Control (OSC) server to listen to commands sent from the touchOSC iphone app.

#### Hardware:
This matrix is composed of three strings of 45 LEDs each, each zigzaged into 3 rows of 15. The each pixel was hand soldered to create a 4 inch space between each LED. The three strings are connected to a fadecandy board, and then to a Raspberry Pi. There is also a USB mic for capturing audo for live music interaction. 


## How To:
Remember how to do this in case of a pi faliure or you have to reproduce this in the future. 


#### Create bootable SD for the Pi
```
Use `df -h or diskutil list` to see mounted paths 
sudo dd if=[/path/to/image] of=/dev/rdisk[n] bs=512k
Example… sudo dd if=/Users/codymccomber/kali-2017.01-rpi2.img of=/dev/rdisk5 bs=512k
```
	Ctl + t to check the status
	"rdisk" is much faster than just "disk" - it doesn’t buffer
	
	sudo dd if=/Users/codymccomber/Downloads/2017-07-05-raspbian-jessie-lite.img of=/dev/rdisk2 bs=512k








