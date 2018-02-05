#!/usr/bin/env python

from __future__ import division
import time
import sys
import optparse
from random import randint
import random
import os

# My custom
import opc
import color_utils
import paho.mqtt.client as mqtt

#
import thread
import threading

import sys
import subprocess

try:
    import json
except ImportError:
    import simplejson as json


print
print
print " _      ___________   _    _       _ _" 
print "| |    |  ___|  _  \ | |  | |     | | |"
print "| |    | |__ | | | | | |  | | __ _| | |"
print "| |    |  __|| | | | | |/\| |/ _` | | |"
print "| |____| |___| |/ /  \  /\  / (_| | | |"
print "\_____/\____/|___/    \/  \/ \__,_|_|_|"
print
print
print

#-------------------------------------------------------------------------------
# Try to start fadecandy server 
try:
    print("Trying to start FC server\n")
    os.system("sudo /home/pi/fadecandy/bin/fcserver-rpi /home/pi/fadecandy/bin/fcserver_config.json &")
    print("\nBackgrounding FC server and continuing with python\n")
except:
    print("Maybe it is already running?\n")


#-------------------------------------------------------------------------------
# Threads for audio input and touchOSC

# Kill switches
run_audio = True
run_touchOSC = True
run_check_touchOSC = True
run_main = True

# Checks the touchOSC server for input, launch via thread
def check_touchOSC():
    global run_check_touchOSC
    while run_check_touchOSC == True:
        touchOSC.server.handle_request()
    touchOSC.server.close()
    return ()

# Starts listening, launch via thread
def startListening():
    audio.startAudio()
    return ()

# Main kill switch to stop the threads
def killSwitch():
    end = "run"
    global run_audio
    global run_check_touchOSC
    global run_main
    run_audio = False
    run_check_touchOSC = False
    #sudo kill $(ps aux | grep 'fadecandy' | awk '{print $2}')
    #sudo kill $(ps aux | grep 'main.py' | awk '{print $2}')
    time.sleep(.5)
    run_main = False
    pixels = [(0,0,0) for ii, coord in enumerate(coordinates)]
    client.put_pixels(pixels, channel=0)
    print
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
# command line

parser = optparse.OptionParser()
parser.add_option('-l', '--layout', dest='layout', default='ledwall15x9.json',
                    action='store', type='string',
                    help='layout file')
parser.add_option('-s', '--server', dest='server', default='piledwall:7890',
                    action='store', type='string',
                    help='ip and port of server')
parser.add_option('-f', '--fps', dest='fps', default=30,
                    action='store', type='int',
                    help='frames per second')

options, args = parser.parse_args()

if options.layout == 'ledwall15x9.json':
    print "\nUsing default layout: " , options.layout , "\n"

if not options.layout:
    parser.print_help()
    print
    print 'ERROR: you must specify a layout file using --layout'
    print
    sys.exit(1)


#-------------------------------------------------------------------------------
# parse layout file

print
print
print '    parsing layout file'
print

coordinates = []
for item in json.load(open(options.layout)):
    if 'point' in item:
        coordinates.append(tuple(item['point']))


#-------------------------------------------------------------------------------
# connect OPC to server

client = opc.Client(options.server)
if client.can_connect():
    print '    connected to %s' % options.server
else:
    # can't connect, but keep running in case the server appears later
    print '    WARNING: could not connect to %s' % options.server
print

#-------------------------------------------------------------------------------
# Setup MQTT
def on_message(client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        #print("message qos=",message.qos)
        #print("message retain flag=",message.retain)

broker_address="localhost" #Controled locally
topic = "/test"

print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic",topic)
client.subscribe(topic)

#print("Publishing message to topic","/test")
#client.publish("/test","OFF")

#client.loop_stop() #stop the loop


#-------------------------------------------------------------------------------
# color modes function






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

    return (r*250, g*250, b*250)


def pixel_color(t, coord, ii, n_pixels):
    #r,g,b = colorOSC
    r,g,b = 50,50,50
    r *= .95
    g *= .95
    b *= .95
    return (r,g,b)


#-------------------------------------------------------------------------------
# send pixels

print '    sending pixels forever (control-c to exit)...'
print
#-------------------------------------------------------------------------------


n_pixels = len(coordinates)
start_time = time.time()

#This is the main loop
delay = 0
mode = "default"

# fps counter
oneSec = 0 # moves every second
sleepFPS = .03 # Guess!
loopCount = 0 # to track FPS

# valid mode options:
# "rainbow", "music", "spatial",
def setMode():  
    if 1: 
        print "Empty mode"
    elif 0:
        print "Empty mode"
    elif 0:
        print "Empty mode"
    else: # Catch all 
        pixels = [rainbow(t*scale(30,(1,100),(.05,2)), coord, ii, n_pixels, random_values) for ii, coord in enumerate(coordinates)]
        client.put_pixels(pixels, channel=0)


random_values = [random.random() for ii in range(n_pixels)]
try:
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

        setMode()


        # call the rainbow function
        # later this needs to be in a switch
        


except KeyboardInterrupt:
    print '\nInterrupt detected'
    # Kill fadecandy server
    print "killing fadecandy server"
    os.system("sudo kill $(ps aux | grep 'fadecandy' | awk '{print $2}')")
    print "Stopping the MQTT loop"
    client.loop_stop() #stop the MQTT loop
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)