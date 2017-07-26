from OSC import OSCServer,OSCClient, OSCMessage
import sys
from time import sleep
import time
import types
import os
#import RPi.GPIO as GPIO

# credit to the this program goes to Grege0reo on instructables. I've just adapted it for my needs.

# these will get * by brightnessData in main.py
faderRedData = 1
faderGreenData = .5
faderBlueData = 1

# The main display modes modes (change to a list?)
mode11 = 0
mode21 = 0
mode31 = 0
mode41 = 0
mode51 = 0
mode61 = 0
mode71 = 0

kill = 0

# Buttons to perfor system functions
system11 = 0 # Kill python
system21 = 0 # Restart Pi
system31 = 0 # shutdown Pi
system41 = 0

brightnessData = 200
speedData = 50



control = 0

padXData = 0
padYData = 0

run = True # Used to kill the main loop, ending the program





server = OSCServer( ("10.0.0.234", 8000) )#This has to be the IP of the RaspberryPi on the network
client = OSCClient()

def handle_timeout(self):
	print ("I'm IDLE")
#This here is just to do something while the script recieves no information....
server.handle_timeout = types.MethodType(handle_timeout, server)

# FADERS
#################################################################################################################################################
def faderRed(path, tags, args, source):
	value=int(args[0])#Value is the variable that will transform the input from the faders into whole numbers(easier to deal with); it will also get the 'y' value of the XP pads
	global faderRedData
	faderRedData = value * .01 # * .01 so we can * by the brightness slider
	print "FaderRed Value:", value


def faderGreen(path, tags, args, source):
	value=int(args[0])#Value is the variable that will transform the input from the faders into whole numbers(easier to deal with); it will also get the 'y' value of the XP pads
	global faderGreenData
	faderGreenData = value * .01 # * .01 so we can * by the brightness slider
	print "FaderGreen Value:", value

def faderBlue(path, tags, args, source):
	value=int(args[0])#Value is the variable that will transform the input from the faders into whole numbers(easier to deal with); it will also get the 'y' value of the XP pads
	global faderBlueData
	faderBlueData = value * .01 # * .01 so we can * by the brightness slider
	print "FaderBlue Value:", value

def speed(path, tags, args, source):
	value=int(args[0])#Value is the variable that will transform the input from the faders into whole numbers(easier to deal with); it will also get the 'y' value of the XP pads
	global speedData
 	speedData = value
	print "speed Value:", value

def brightness(path, tags, args, source):
	value=int(args[0])#Value is the variable that will transform the input from the faders into whole numbers(easier to deal with); it will also get the 'y' value of the XP pads
	global brightnessData
 	brightnessData = value
	print "brightness Value:", value


# XY PADS
###############################################################################################################################################
def xypad(path, tags, args, source):
	 yy=int(args[0])
	 xx=int(args[1])#Value 2 is used with XP pads, it will get the 'x' value
	 print "Value of Y:", yy,  "    Value of X:", xx

def pad(path, tags, args, source):
	 yy=int(args[0])
	 xx=int(args[1])#Value 2 is used with XP pads, it will get the 'x' value
	 global padXData
	 global padYData
	 padXData = yy
	 padYData = xx
	 print "Value of Y:", yy,  "    Value of X:", xx



# BUTTONS
####################################################################################################################################################
def kill_switch(path, tags, args, source):
	state=int(args[0])
	print "Kill Switch:", state
	if state == 1:
		server.close()#THIS IS THE EMERGENCY KILL BUTTON!

# mode buttons for the main functions e.g. music, draw, lava
def mode11(path, tags, args, source): # music
	state=int(args[0])
	global mode11
	mode11 = state
	print "Mode 1: ", state;

def mode21(path, tags, args, source):
	state=int(args[0])
	global mode21
	mode21 = state
	print "Mode 2: ", state;

def mode31(path, tags, args, source):
	state=int(args[0])
	global mode31
	mode31 = state
	print "Mode 3: ", state;

def mode41(path, tags, args, source):
	state=int(args[0])
	global mode41
	mode41 = state
	print "Mode 4: ", state;

def mode51(path, tags, args, source):
	state=int(args[0])
	global mode51
	mode51 = state
	print "Mode 5: ", state;

def mode61(path, tags, args, source):
	state=int(args[0])
	global mode61
	mode61 = state
	print "Mode 6: ", state;

def mode71(path, tags, args, source):
	state=int(args[0])
	global mode71
	mode71 = state
	print "Mode 7: ", state;

# To control kill, restart, shutdown
def system11(path, tags, args, source): # Restart Python
	state=int(args[0])
	global system11
	system11 = state
	print "System11: ", state;
	time.sleep(5)
	os.system("sudo systemctl restart ledwall.service")


def system21(path, tags, args, source): # Kill python
	state=int(args[0])
	global system21
	system21 = state
	print "System21: ", state;

def system31(path, tags, args, source): # Restart RaspberryPi
	state=int(args[0])
	global system31
	system31 = state
	print "System31: ", state;
	time.sleep(5)
	os.system("sudo shutdown -r now")

def system41(path, tags, args, source): # shutdown RaspberryPi
	state=int(args[0])
	global system41
	system41 = state
	print "System41: ", state;
	time.sleep(5)
	os.system("sudo shutdown now")

# old python kill switch
def kill(path, tags, args, source):
	state=int(args[0])
	global kill
	kill = state
	print "Kill: ", state;

# unused
def control(path, tags, args, source):
	state=int(args[0])
	global control
	control = state
	print "Control: ", state;






# ACCELEROMETER (will onyl work if you have the Accelerometer option on, in the TouchOSC app)
###################################################################################################################################################
def accel(path, tags, args, source):
	y=float(args[0])
	x=float(args[1])
	z=float(args[2])
	print "X:", x
	print "Y:", y
	print "Z:", z
	print " "
	time.sleep(3);


#These are all the add-ons that you can name in the TouchOSC layout designer (you can set the values and directories)
server.addMsgHandler("/faderRed",faderRed)
server.addMsgHandler("/faderGreen",faderGreen)
server.addMsgHandler("/faderBlue",faderBlue)
server.addMsgHandler("/mode/1/1", mode11)
server.addMsgHandler("/mode/2/1", mode21)
server.addMsgHandler("/mode/3/1", mode31)
server.addMsgHandler("/mode/4/1", mode41)
server.addMsgHandler("/mode/5/1", mode51)
server.addMsgHandler("/mode/6/1", mode61)
server.addMsgHandler("/mode/7/1", mode71)
server.addMsgHandler("/kill", kill)
server.addMsgHandler("/system/1/1", system11)
server.addMsgHandler("/system/2/1", system21)
server.addMsgHandler("/system/3/1", system31)
server.addMsgHandler("/system/4/1", system41)
server.addMsgHandler("/control", control)
server.addMsgHandler("/speed", speed)
server.addMsgHandler("/brightness", brightness)
server.addMsgHandler("/pad", pad)
server.addMsgHandler("/1/xy1", xypad)
server.addMsgHandler("/1/toggle1", kill_switch)
server.addMsgHandler("accxyz", accel)#The Accelerometeer Values
#The way that the MSG Handlers work is by taking the values from set accessory, then it puts them into a function
#The function then takes the values and separates them according to their class (args, source, path, and tags)


#while True:
	#server.handle_request()

#server.close()
#This will kill the server when the program ends
