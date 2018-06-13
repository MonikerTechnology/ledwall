#!/usr/bin/env python

from __future__ import division
import time
import sys
import optparse
from random import randint
import random
import os
import colorsys

# My custom
import opc
import color_utils
import audio

import HTTPserver
import googleAssistant
import log
file = str(os.path.basename(__file__))
import requests
import threading

import sys
import subprocess

try:
    import json
except ImportError:
    import simplejson as json


print()
print()
                                                                                                                                                  
                                                                                                                                                  
print("LLLLLLLLLLL             EEEEEEEEEEEEEEEEEEEEEEDDDDDDDDDDDDD             WWWWWWWW                           WWWWWWWW               lllllll lllllll ")
print("L:::::::::L             E::::::::::::::::::::ED::::::::::::DDD          W::::::W                           W::::::W               l:::::l l:::::l ")
print("L:::::::::L             E::::::::::::::::::::ED:::::::::::::::DD        W::::::W                           W::::::W               l:::::l l:::::l ")
print("LL:::::::LL             EE::::::EEEEEEEEE::::EDDD:::::DDDDD:::::D       W::::::W                           W::::::W               l:::::l l:::::l ")
print("  L:::::L                 E:::::E       EEEEEE  D:::::D    D:::::D       W:::::W           WWWWW           W:::::Waaaaaaaaaaaaa    l::::l  l::::l ")
print("  L:::::L                 E:::::E               D:::::D     D:::::D       W:::::W         W:::::W         W:::::W a::::::::::::a   l::::l  l::::l ")
print("  L:::::L                 E::::::EEEEEEEEEE     D:::::D     D:::::D        W:::::W       W:::::::W       W:::::W  aaaaaaaaa:::::a  l::::l  l::::l ")
print("  L:::::L                 E:::::::::::::::E     D:::::D     D:::::D         W:::::W     W:::::::::W     W:::::W            a::::a  l::::l  l::::l ")
print("  L:::::L                 E:::::::::::::::E     D:::::D     D:::::D          W:::::W   W:::::W:::::W   W:::::W      aaaaaaa:::::a  l::::l  l::::l ")
print("  L:::::L                 E::::::EEEEEEEEEE     D:::::D     D:::::D           W:::::W W:::::W W:::::W W:::::W     aa::::::::::::a  l::::l  l::::l ")
print("  L:::::L                 E:::::E               D:::::D     D:::::D            W:::::W:::::W   W:::::W:::::W     a::::aaaa::::::a  l::::l  l::::l ")
print("  L:::::L         LLLLLL  E:::::E       EEEEEE  D:::::D    D:::::D              W:::::::::W     W:::::::::W     a::::a    a:::::a  l::::l  l::::l ")
print("LL:::::::LLLLLLLLL:::::LEE::::::EEEEEEEE:::::EDDD:::::DDDDD:::::D                W:::::::W       W:::::::W      a::::a    a:::::a l::::::ll::::::l ")
print("L::::::::::::::::::::::LE::::::::::::::::::::ED:::::::::::::::DD                  W:::::W         W:::::W       a:::::aaaa::::::a l::::::ll::::::l ")
print("L::::::::::::::::::::::LE::::::::::::::::::::ED::::::::::::DDD                     W:::W           W:::W         a::::::::::aa:::al::::::ll::::::l ")
print("LLLLLLLLLLLLLLLLLLLLLLLLEEEEEEEEEEEEEEEEEEEEEEDDDDDDDDDDDDD                         WWW             WWW           aaaaaaaaaa  aaaallllllllllllllll ")
                                                                                                                                                  
                                                                                                                                                  
print()
print ()
log.header(file,"SETUP")
print()

#-------------------------------------------------------------------------------
# Try to start fadecandy server 

log.header(file,"Trying to start FC server...")
try:
    os.system("sudo /home/pi/fadecandy/bin/fcserver-rpi /home/pi/fadecandy/bin/fcserver_config.json &")
    log.header(file,"Backgrounding FC server and continuing with python")
except:
    log.warning(file,"Failed...Maybe it is already running?")


#-------------------------------------------------------------------------------
# Threads for audio input and the threading all kill switch stuff

# Kill switches
run_audio = True
run_main = True
run_HTTPserver = True



# Starts listening, launch via thread
def startListening():
    audio.startAudio()
    return ()

# #t_HTTPserver = threading.Thread()
# def startHTTPserver():
#     HTTPserver.start() #Port 321
#     return()

# Main kill switch to stop the threads
def killSwitch():
    end = "run"
    global run_audio
    global run_main
    global run_HTTPserver
    run_audio = False
    
    #sudo kill $(ps aux | grep 'fadecandy' | awk '{print $2}')
    #sudo kill $(ps aux | grep 'main.py' | awk '{print $2}')

    log.info(file,"killing HTTPserver")
    log.info(file,"Sending one last request to kill the HTTPserver")
    HTTPserver.run = False
    try: # try to send one last request to kill the server
        r = requests.get("http://localhost:321")
    except:
        pass
    time.sleep(.5)


    log.info(file,"killing googleAssistant")
    googleAssistant.run = False


    print()
    print()
    log.info(file,"killing fadecandy server")
    os.system("sudo kill $(ps aux | grep 'fadecandy' | awk '{print $2}')")
    time.sleep(.5)



    log.info(file,"Killing main")
    run_main = False

    log.info(file,"Setting pixels to 0,0,0")
    pixels = [(0,0,0) for ii, coord in enumerate(coordinates)] #set all the pixels to off
    client.put_pixels(pixels, channel=0)

    print()
    print()
    log.info(file,"Is the HTTPserver thread running " + str(t_HTTPserver.is_alive()))
    log.info(file,"Is the googleAssistant thread running " + str(t_googleAssistant.is_alive()))
    print()
    return ()

def restartPi():
    pixels = [(0,0,0) for ii, coord in enumerate(coordinates)]
    client.put_pixels(pixels, channel=0)
    os.system("sudo shutdown -r now")
def shutdownPi():
    pixels = [(0,0,0) for ii, coord in enumerate(coordinates)]
    client.put_pixels(pixels, channel=0)
    os.system("sudo shutdown now")
def restartPython():
    pixels = [(0,0,0) for ii, coord in enumerate(coordinates)]
    client.put_pixels(pixels, channel=0)
    os.system("sudo systemctl restart ledwall.service")

def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]


time.sleep(1)
#-------------------------------------------------------------------------------
# Threading


#add in a check to see if it stopped and restart it
# also check fadecandy
#t_HTTPserver = threading.Thread(target=startHTTPserver, args=())

t_HTTPserver = threading.Thread(target=HTTPserver.start, args=())
t_googleAssistant = threading.Thread(target=googleAssistant.start)
t_audio = threading.Thread(target=audio.startAudio)

#start
log.header(file,"Starting HTTPserver")
t_HTTPserver.start()
log.header(file,"Starting googleAssistant server")
t_googleAssistant.start()
log.header(file,"Starting audio loop")
t_audio.start()
    

#-------------------------------------------------------------------------------
# command line options for main

parser = optparse.OptionParser()
parser.add_option('-l', '--layout', dest='layout', default='supporting_files/ledwall15x9.json',
                    action='store', type='string',
                    help='layout file')
parser.add_option('-s', '--server', dest='server', default='ledwall:7890',
                    action='store', type='string',
                    help='ip and port of server')
parser.add_option('-f', '--fps', dest='fps', default=30,
                    action='store', type='int',
                    help='frames per second')

options, args = parser.parse_args()

if options.layout == 'supported_files/ledwall15x9.json':
    log.info(file,"\nNo layout selected, using default layout: " + str(options.layout) + "\n")

if not options.layout:
    parser.print_help()
    print()
    log.warning(file,'ERROR: you must specify a layout file using --layout')
    print()
    sys.exit(1)


#-------------------------------------------------------------------------------
# parse layout file

print
print
log.header(file,'    parsing FC layout file')
print

coordinates = []
for item in json.load(open(options.layout)):
    if 'point' in item:
        coordinates.append(tuple(item['point']))


#-------------------------------------------------------------------------------
# connect OPC to server

client = opc.Client(options.server)
if client.can_connect():
    log.header(file,'    OPC connected to %s' % options.server)
else:
    # can't connect, but keep running in case the server appears later
    log.warning(file,'    WARNING: could not connect to %s' % options.server)
print()

#-------------------------------------------------------------------------------
# Setup MQTT

mode = "default" #global
lastMode = ""
redMultiplier = 1
greenMultiplier = 1
blueMultiplier = 1

"""
print
print(" __  __  _____  ____  ____ ")
print("(  \/  )(  _  )(_  _)(_  _)")
print(" )    (  )(_)(   )(    )(  ")
print("(_/\/\_)(___/\\\ (__)  (__) ") #double \\ to escape


broker_address="localhost" #Controled locally
topic = "/LEDwall"

#def on_message(client, userdata, message):
def on_message(MQTTclient, userdata, message):
    global mode
    global lastMode
    global redMultiplier
    global greenMultiplier
    global blueMultiplier
    #print("message received " ,str(message.payload.decode("utf-8")))
    #print("message topic=",message.topic)
    MQTTMessage = str(message.payload.decode("utf-8"))
    print("MQTT message recived: " + MQTTMessage)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)

    #lastMode = mode
    #mode = MQTTMessage[0:8] # first 8 char is mode
    # Mode      Data
    # rainbowX  None
    # HSVXXXXX  0.000,0.850,0.960
    # loadingX  None
    # musicXXX  None
    # offXXXXX  None

    # Maybe use this for initial set up?
    if "HSVXXXXX" == MQTTMessage[0:8]: 
        print("New HSV data")
        #print MQTTMessage[8:13]
        #print MQTTMessage[14:19]
        #print MQTTMessage[20:24]
      
        redMultiplier, greenMultiplier, blueMultiplier = colorsys.hsv_to_rgb(float(MQTTMessage[8:13]), float(MQTTMessage[14:19]), float(MQTTMessage[20:24]))

    elif "offXXXXX" == MQTTMessage[0:8]:
        print("Empty mode")
        mode = MQTTMessage[0:8]
        #make blank???
    elif "rainbowX" == MQTTMessage[0:8]:
        print("rainbowX mode")
        mode = MQTTMessage[0:8]

    else: # Catch all - maybe loading pattern?
        print("Empty mode - catch all")


print
print("MQTT initializing...")
print("creating new instance")
MQTTclient = mqtt.Client("P1") #create new instance
MQTTclient.on_message=on_message #attach function to callback
print("connecting to broker")
MQTTclient.connect(broker_address) #connect to broker
MQTTclient.loop_start() #start the loop
print("Subscribing to topic: " + topic)
print
print
MQTTclient.subscribe(topic)

#print("Publishing message to topic","/test")
#client.publish("/test","OFF")

#client.loop_stop() #stop the loop

"""


message = HTTPserver.postDic
mode = "rainbow"
power = 0

#power message
#{"type":"power","power":1}
#{"power":1,"type":"power"}

#HSV message
#{"type":"HSV","HSV":{"H":123,"S":123,"V":123}}

#mode message
#{"type":"mode","mode":"rainbow"}

#-------------------------------------------------------------------------------
# color modes function


def startup(t, coord, ii, n_pixels):
    """Compute the color of a given pixel.
    t: time in seconds since the program started.
    ii: which pixel this is, starting at 0
    coord: the (x, y, z) position of the pixel as a tuple
    n_pixels: the total number of pixels
    Returns an (r, g, b) tuple in the range 0-255
    """
    global position
    x,y,z = coord
    #print(coord)
    #print("position")
    #print(int(position))
    if (ii == 0):
        r = value[int(position)]
        g = value[int(position)]
        b = value[int(position)]
    elif (ii == 1 or ii == 29 or ii == 28):
        r = value[int(position)] * .7
        g = value[int(position)] * .5
        b = value[int(position)] * .5
    else: 
        r = 0
        g = 0
        b = 0

    
    position += .01
    if (position > 499):
        position = 0

    #padXData = touchOSC.padXData
    #padYData = int(touchOSC.padYData * .65)
    #print padYData
    #print touchOSC.padYData


    #r,g,b = colorOSC

    #if x == padXData and z == padYData:
    #r,g,b = draw.circle(padXData,padYData, x, z,colorOSC)
    #draw.circle(5,5, x, z)


    return (r, g, b)

def audioBars(t, coord, ii, n_pixels, random_values):
    x, y, z = coord

    h = int(audio.positionVolume13[x])
    #print("h ", h)

    l = int(audio.lastPositionVolume13[x])
    #print("l ",l)



    if z == l: #max volume falling
        return (250,10,250)
        #return (0,0,0)
    elif z > h: #everything below(above) the current volume
        #return (0,0,0)
        return (250,250,250)
    else:
        return (0,0,0)

#def bar(label, value,last):
    # string = ""
    # count = 0
    # if value > 2000:
    #     value = 2000
    # while value > 0:
    #     count+=1
    #     string+="-" 
    #     value-=50        
    # while count < last - 1: #add space for the memory bar
    #     string+=" "
    #     count+=1
    
    # string+="|"
    # print(label , string)
    # return count

def rainbow(t, coord, ii, n_pixels, random_values):

    """Compute the color of a given pixel.

    t: time in seconds since the program started.
    ii: which pixel this is, starting at 0
    coord: the (x, y, z) position of the pixel as a tuple
    n_pixels: the total number of pixels
    random_values: a list containing a constant random value for each pixel

    Returns an (r, g, b) tuple in the range 0-255

    """


    # make moving stripes for x, y, and z
    x, y, z = coord

    # Scale the x and z to match the original map file wall.json
    x = scale(x, (0,14), (-0.7,0.7))
    z = scale(z, (0,8), (-0.4,0.4))



    y += color_utils.cos(x + 0.2*z, offset=0, period=1, minn=0, maxx=0.6)
    z += color_utils.cos(x, offset=0, period=1, minn=0, maxx=0.3)
    x += color_utils.cos(y + z, offset=0, period=1.5, minn=0, maxx=0.2)

    # rotate
    x, y, z = y, z, x

     # shift some of the pixels to a new xyz location
    # if ii % 17 == 0:
    #     x += ((ii*123)%5) / n_pixels * 32.12 + 0.1
    #     y += ((ii*137)%5) / n_pixels * 22.23 + 0.1
    #     z += ((ii*147)%7) / n_pixels * 44.34 + 0.1

    # make x, y, z -> r, g, b sine waves
    r = color_utils.cos(x, offset=t / 4, period=2, minn=0, maxx=1)
    g = color_utils.cos(y, offset=t / 4, period=2, minn=0, maxx=1)
    b = color_utils.cos(z, offset=t / 4, period=2, minn=0, maxx=1)
    r, g, b = color_utils.contrast((r, g, b), 0.5, 1.5)
    # r, g, b = color_utils.clip_black_by_luminance((r, g, b), 0.5)
    #
    # # shift the color of a few outliers
    # if random_values[ii] < 0.03:
    #     r, g, b = b, g, r

    # black out regions
    r2 = color_utils.cos(x, offset=t / 10 + 12.345, period=3, minn=0, maxx=1)
    g2 = color_utils.cos(y, offset=t / 10 + 24.536, period=3, minn=0, maxx=1)
    b2 = color_utils.cos(z, offset=t / 10 + 34.675, period=3, minn=0, maxx=1)
    clampdown = (r2 + g2 + b2)/2
    clampdown = color_utils.remap(clampdown, 0.8, 0.9, 0, 1)
    clampdown = color_utils.clamp(clampdown, 0, 1)
    r *= clampdown
    g *= clampdown
    b *= clampdown

    # color scheme: fade towards blue-and-orange
    # g = (r+b) / 2
    g = g * 0.6 + ((r+b) / 2) * 0.4

    # apply gamma curve
    # only do this on live leds, not in the simulator
    r, g, b = color_utils.gamma((r, g, b), 2.2)

    return (r*250*HTTPserver.redMultiplier, g*250*HTTPserver.greenMultiplier, b*250*HTTPserver.blueMultiplier)


def pixel_color(t, coord, ii, n_pixels):
    #r,g,b = colorOSC
    r,g,b = 50,50,50
    r *= .95
    g *= .95
    b *= .95
    return (r,g,b)


#-------------------------------------------------------------------------------
# send pixels

log.info(file,'    sending pixels forever (control-c to exit)...')
print()
#-------------------------------------------------------------------------------


n_pixels = len(coordinates)
start_time = time.time()

#This is the main loop
delay = 0
mode = "default"
#

# fps counter
oneSec = 0 # moves every second
sleepFPS = .03 # Guess!
loopCount = 0 # to track FPS

#counter for the startup
position = 0
value = [] # list from 0 - 250 - 0
value.extend(range(0,250))
value.extend(reversed(range(0,250)))


random_values = [random.random() for ii in range(n_pixels)]
try:
    log.info(file,"about to start main loop")
    while run_main == True:
        

        # set looping variables
        t = time.time() - start_time # keep track of how long the program has been running

        #----------------------------------------------
        # this tracks the FPS and adjusts the delay to keep it consistant.
        loopCount += 1
        if oneSec < t:
            oneSec += 1
            trueFPS = loopCount
            # print options.fps
            # print ("Loops per sec: %i") % loopCount
            # print
            if trueFPS < options.fps - 1:
                sleepFPS *= .95
            elif trueFPS > options.fps + 1:
                sleepFPS *= 1.05
            loopCount = 0
        time.sleep(sleepFPS)
        # End FPS tracker
        #----------------------------------------------
        HTTPserver.mode = "audio"
        HTTPserver.power = 1
        if HTTPserver.mode == "rainbow" and HTTPserver.power == 1:
        #if HTTPserver.power == 1:
            pixels = [rainbow(t*scale(30,(1,100),(.05,2)), coord, ii, n_pixels, random_values) for ii, coord in enumerate(coordinates)]
            client.put_pixels(pixels, channel=0)
        if HTTPserver.mode == "breathe" and HTTPserver.power == 1:
            pixels = [startup(t, coord, ii, n_pixels) for ii, coord in enumerate(coordinates)]
            client.put_pixels(pixels, channel=0)
        elif HTTPserver.mode == "off" or HTTPserver.power == 0:
            nothing = 0
            #pixels = [pixel_color(t, coord, ii, n_pixels) for ii, coord in enumerate(coordinates)]
            #client.put_pixels(pixels, channel=0)

            #add fade out!!
            pixels = [(0,0,0) for ii, coord in enumerate(coordinates)] #set all the pixels to off
            client.put_pixels(pixels, channel=0)
        elif HTTPserver.mode == "audio" and HTTPserver.power == 1:
            options.fps = 10
            audio.getResults()
            pixels = [audioBars(t*scale(30,(1,100),(.05,2)), coord, ii, n_pixels, random_values) for ii, coord in enumerate(coordinates)]
            client.put_pixels(pixels, channel=0)

        else: # catch all maybe do loading
            nothing = 0

      

       

except KeyboardInterrupt:
    print
    log.warning(file,'\nInterrupt detected')
    killSwitch() #shut down all the things as gracfully as possible

    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
