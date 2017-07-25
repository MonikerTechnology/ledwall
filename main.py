#!/usr/bin/env python

from __future__ import division
import time
import sys
import optparse
from random import randint
import random
import os

# My custom
from func import draw
import touchOSC
import audio
import opc
import color_utils

#
import thread
import threading

import sys
import subprocess

try:
    import json
except ImportError:
    import simplejson as json



#for the live audio
#import aubio
#import numpy as num
#import pyaudio
import time


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


#t1 = thread.start_new_thread(checkServer, ())
    #print t1.isAlive()

# Set up
t_check_touchOSC = threading.Thread(target=check_touchOSC, args=())
t_startListening = threading.Thread(target=startListening, args=())

# start
t_check_touchOSC.start()
t_startListening.start()


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


#-------------------------------------------------------------------------------
# color modes function



def music(t, coord, ii, n_pixels):

    # this was inside the color finciton
    x, y, z = coord
    r,g,b = 0,0,0

    #Z line
    if (r,g,b) == (0,0,0):
        r,g,b = draw.lineX(linePos,x,z,(x*17,pitchColor,150),mod)
    #Z line
    if (r,g,b) == (0,0,0):
        r,g,b = draw.lineX(linePos+4,x,z,(0,pitchColor*.6,0),mod)
        if (r,g,b) != (0,0,0):
            b = color_utils.cos(1, offset=t / 10, period=10, minn=0, maxx=1)
            r = color_utils.cos(5, offset=t / 4, period=2, minn=0, maxx=1)
            b = 150
            r = (x * 15) * r

    #Bass booms
    count = 0
    while count < 8:
        if (r,g,b) == (0,0,0):
            r,g,b = draw.boom(centerX[count],centerZ[count], x, z,color[count],pos[count])
        count += 1

    #color the rest
    if (r,g,b) == (0,0,0):
        b = color_utils.cos(1, offset=t / 10, period=10, minn=0, maxx=1)
        b = b * pitchColor / 7



    r = int(r)
    g = int(g)
    b = int(b)
    r /= 256
    g /= 256
    b /= 256


    return (r*redOSC, g*greenOSC, b*blueOSC)

def musicv2(t, coord, ii, n_pixels):

    # this was inside the color finciton
    x, y, z = coord
    r,g,b = 0,0,0

    #Z line
    if (r,g,b) == (0,0,0):
        r,g,b = draw.lineX(linePos,x,z,(x*17,pitchColor,150),mod)
    #Z line
    if (r,g,b) == (0,0,0):
        r,g,b = draw.lineX(linePos+4,x,z,(0,pitchColor*.6,0),mod)
        if (r,g,b) != (0,0,0):
            b = color_utils.cos(1, offset=t / 10, period=10, minn=0, maxx=1)
            r = color_utils.cos(5, offset=t / 4, period=2, minn=0, maxx=1)
            b = 150
            r = (x * 15) * r

    #Bass booms
    count = 0
    while count < 8:
        if (r,g,b) == (0,0,0):
            r,g,b = draw.boom(centerX[count],centerZ[count], x, z,color[count],pos[count])
        count += 1

    #color the rest
    if (r,g,b) == (0,0,0):
        b = color_utils.cos(1, offset=t / 10, period=10, minn=0, maxx=1)
        b = b * pitchColor / 7



    r = int(r)
    g = int(g)
    b = int(b)
    r /= 256
    g /= 256
    b /= 256


    return (r*redOSC, g*greenOSC, b*blueOSC)


def control_circle(t, coord, ii, n_pixels):
    """Compute the color of a given pixel.

    t: time in seconds since the program started.
    ii: which pixel this is, starting at 0
    coord: the (x, y, z) position of the pixel as a tuple
    n_pixels: the total number of pixels

    Returns an (r, g, b) tuple in the range 0-255

    """
    x,y,z = coord

    padXData = touchOSC.padXData
    padYData = int(touchOSC.padYData * .65)
    #print padYData
    #print touchOSC.padYData


    r,g,b = colorOSC

    #if x == padXData and z == padYData:
    r,g,b = draw.circle(padXData,padYData, x, z,colorOSC)
    #draw.circle(5,5, x, z)


    return (r, g, b)


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

    return (r*redOSC, g*greenOSC, b*blueOSC)

def spatial_stripes(t, coord, ii, n_pixels):
    """Compute the color of a given pixel.

    t: time in seconds since the program started.
    ii: which pixel this is, starting at 0
    coord: the (x, y, z) position of the pixel as a tuple
    n_pixels: the total number of pixels

    Returns an (r, g, b) tuple in the range 0-255

    """

    x, y, z = coord

    # Scale the x and z to match the original map file wall.json
    x = scale(x, (0,14), (-0.7,0.7))
    z = scale(z, (0,8), (-0.4,0.4))

    # make moving stripes for x, y, and z
    r = color_utils.cos(x, offset=t / 4, period=1, minn=0, maxx=0.7)
    g = color_utils.cos(y, offset=t / 4, period=1, minn=0, maxx=0.7)
    b = color_utils.cos(z, offset=t / 4, period=1, minn=0, maxx=0.7)
    r, g, b = color_utils.contrast((r, g, b), 0.5, 2)

    # make a moving white dot showing the order of the pixels in the layout file
    spark_ii = (t*80) % n_pixels
    spark_rad = 8
    spark_val = max(0, (spark_rad - color_utils.mod_dist(ii, spark_ii, n_pixels)) / spark_rad)
    spark_val = min(1, spark_val*2)
    r += spark_val
    g += spark_val
    b += spark_val

    # apply gamma curve
    # only do this on live leds, not in the simulator
    #r, g, b = color_utils.gamma((r, g, b), 2.2)

    return (r*redOSC, g*greenOSC, b*blueOSC)


def pixel_color(t, coord, ii, n_pixels):
    r,g,b = colorOSC
    r *= .95
    g *= .95
    b *= .95
    return (r,g,b)

def blank(t, coord, ii, n_pixels):
    r,g,b = 0,0,0
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



#define variables for music

# Bass booms
i = 0
doBoom = [0,0,0,0,0,0,0,0] #for if conditions have been meet to do a boom
centerX = [0,0,0,0,0,0,0,0] #for each boom
centerZ = [0,0,0,0,0,0,0,0] #for each boom
pos = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0] #the step each boom is at
color = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)] #the color for each boom
delay = 0 #keeps from doing too many booms on the same note


# config
# Larger is faster max = 1
speed = .001 #bass booms

# Keep track of vol and pitch
pitchMax = 1000
pitchMin = 50
volumeMax = 50
volumeMin = 10

countByTwo = 0
pitchDelay = 1 #sets a delay so the pitch color doesnt flicker
pitchColor = 1
count = 0

# fps counter
oneSec = 0 # moves every second
sleepFPS = .03 # Guess!
loopCount = 0 # to track FPS



random_values = [random.random() for ii in range(n_pixels)]
while run_main == True:

    # set looping variables
    t = time.time() - start_time # keep track of how long the program has been running
    colorOSC = touchOSC.faderRedData*touchOSC.brightnessData, touchOSC.faderGreenData*touchOSC.brightnessData, touchOSC.faderBlueData*touchOSC.brightnessData # RGB tuple 0-256
    redOSC,greenOSC,blueOSC = colorOSC # RGB 0-256


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







    # call the function and draw the pixels
    if touchOSC.mode11 == 1: # React to music

        # pull the values in
        pitch = audio.pitch
        volume = float(audio.volume) * 50000


        #count += 1

        # this is for the bass booms
        speed = .005 * touchOSC.speedData
        if doBoom[i] == 1:
            i += 1
            if i == 8:
                i = 0

        delay += 1 #keeps from doing too many booms on the same note

        tolerance = pitchMin * 4
        # if (pitch < tolerance and volume > volumeMin * 1.00) and pitch > 0 and doBoom[i] == 0 and delay > 50:
        if pitch < tolerance and pitch > 0 and doBoom[i] == 0 and volume > (volumeMin * 1.5) and delay > 5:
            delay = 0
            doBoom[i] = 1 # sets this as an active boom
            centerX[i] = randint(0, 14)
            centerZ[i] =  draw.inverse(int(scale(pitch,(10,int(tolerance)),(0,3))))
            color[i] = randint(50, 250),randint(50, 250),randint(100, 256)
        count = 0
        while count < 8: # rotats through all active booms and increases the step
            if pos[count] <= 6.0 and doBoom[count] == 1:
                pos[count] += scale(touchOSC.speedData,(1,100),(.005,.5))
            else:
                pos[count] = 0
                doBoom[count] = 0
            count += 1 # keep track of the



        # pitch color and Z axis line
        pitchDelay -= 1 # sets a delay so the pitch color doesnt flicker
        if pitchDelay == 0:
            pitchColor = int(draw.scale(pitch,(pitchMin,pitchMax+1),(50,225)))
            if volume > volumeMax * .8:
                linePos = 0
                mod = 0
            elif volume > volumeMax * .7:
                linePos = 0
                mod = 1
            elif volume > volumeMax * .6:
                linePos = 1
                mod = 0
            elif volume > volumeMax * .5:
                linePos = 1
                mod = 1
            elif volume > volumeMax * .3:
                linePos = 2
                mod = 1
            elif volume > volumeMax * .2:
                linePos = 3
                mod = 0
            elif volume > volumeMax * .1:
                linePos = 3
                mod = 1
            else:
                linePos = 4
                mod = 0
            pitchDelay = 2

        # print ("volume: %f") % volume
        # print ("pitch %f ")% pitch




        #Dynamically keep track of the min and max pitch
        if pitch > pitchMax:
            pitchMax = pitch
        if pitch < pitchMin and pitch > 20:
            pitchMin = pitch
        #Dynamically keep track of the min and max volume
        if volume > volumeMax:
            volumeMax = volume
        if volume < volumeMin and volume > 2.5:
            volumeMin = volume
        #every 2 seconds move the pitch and volume in
        if countByTwo < t:
            countByTwo += 2
            pitchMax *= .9
            pitchMin *= 1.1
            volumeMax *= .9
            volumeMin *= 1.1
            # print
            # print ("pitchMax: %f ")% pitchMax
            # print ("pitchMin: %f ")% pitchMin
            # print ("volumeMax: %f ")% volumeMax
            # print ("volumeMin: %f ")% volumeMin
            # print

        #print volume
        # print "pitch color: %i" % pitchColor
        # print ("pitch: %f ")% pitch
        # print ("pitchMax: %f ")% pitchMax
        # print ("pitchMin: %f ")% pitchMin
        # print tolerance
        # print ("volumeMax: %f ")% volumeMax
        # print ("volumeMin: %f ")% volumeMin
        # print ("volume %f") % volume
        # print delay
        # print
        # print ("time: %f") % t
        # print ("count by two: %i") % countByTwo
        # print loopCount
        # print ("Loops per sec: %i ") % int(loopCount / t)
        # print



        pixels = [music(t, coord, ii, n_pixels) for ii, coord in enumerate(coordinates)]
        client.put_pixels(pixels, channel=0)
    elif touchOSC.mode21 == 1:
        padXData = touchOSC.padXData
        touchOSC.padYData
        padYData = scale(touchOSC.padYData,(0,14),(0,8))
        pixels = [control_circle(t, coord, ii, n_pixels) for ii, coord in enumerate(coordinates)]
        client.put_pixels(pixels, channel=0) # Draw circle
    elif touchOSC.mode31 == 1:
        pixels = [rainbow(t*scale(touchOSC.speedData,(1,100),(.05,2)), coord, ii, n_pixels, random_values) for ii, coord in enumerate(coordinates)]
        client.put_pixels(pixels, channel=0)
        # time.sleep(1 / options.fps) # ranbow (lava lamp)
    elif touchOSC.mode41 == 1:
        pixels = [spatial_stripes(t*scale(touchOSC.speedData,(1,100),(.05,2)), coord, ii, n_pixels) for ii, coord in enumerate(coordinates)]
        client.put_pixels(pixels, channel=0)
        # time.sleep(1 / options.fps) # spatial_stripes
    elif touchOSC.mode71 == 1:
        doNothing = 0
    elif touchOSC.mode51 == 1: # React to musicv2

        # pull the values in
        pitch = audio.pitch
        volume = float(audio.volume) * 50000


        #count += 1

        # this is for the bass booms
        speed = .005 * touchOSC.speedData
        if doBoom[i] == 1:
            i += 1
            if i == 8:
                i = 0

        delay += 1 #keeps from doing too many booms on the same note

        tolerance = pitchMin * 4
        # if (pitch < tolerance and volume > volumeMin * 1.00) and pitch > 0 and doBoom[i] == 0 and delay > 50:
        if pitch < tolerance and pitch > 0 and doBoom[i] == 0 and volume > (volumeMin * 1.5) and delay > 5:
            delay = 0
            doBoom[i] = 1 # sets this as an active boom
            centerX[i] = randint(0, 14)
            centerZ[i] =  draw.inverse(int(scale(pitch,(10,int(tolerance)),(0,3))))
            color[i] = randint(50, 250),randint(50, 250),randint(100, 256)
        count = 0
        while count < 8: # rotats through all active booms and increases the step
            if pos[count] <= 6.0 and doBoom[count] == 1:
                pos[count] += scale(touchOSC.speedData,(1,100),(.005,.5))
            else:
                pos[count] = 0
                doBoom[count] = 0
            count += 1 # keep track of the



        # pitch color and Z axis line
        pitchDelay -= 1 # sets a delay so the pitch color doesnt flicker
        if pitchDelay == 0:
            pitchColor = int(draw.scale(pitch,(pitchMin,pitchMax+1),(50,225)))
            if volume > volumeMax * .8:
                linePos = 0
                mod = 0
            elif volume > volumeMax * .7:
                linePos = 0
                mod = 1
            elif volume > volumeMax * .6:
                linePos = 1
                mod = 0
            elif volume > volumeMax * .5:
                linePos = 1
                mod = 1
            elif volume > volumeMax * .3:
                linePos = 2
                mod = 1
            elif volume > volumeMax * .2:
                linePos = 3
                mod = 0
            elif volume > volumeMax * .1:
                linePos = 3
                mod = 1
            else:
                linePos = 4
                mod = 0
            pitchDelay = 2

        # print ("volume: %f") % volume
        # print ("pitch %f ")% pitch




        #Dynamically keep track of the min and max pitch
        if pitch > pitchMax:
            pitchMax = pitch
        if pitch < pitchMin and pitch > 20:
            pitchMin = pitch
        #Dynamically keep track of the min and max volume
        if volume > volumeMax:
            volumeMax = volume
        if volume < volumeMin and volume > 2.5:
            volumeMin = volume

        #every 2 seconds try to move the pitch and volume in
        if countByTwo < t and volumeMin * 1.5 < volumeMax:
            volumeMax *= .9
            volumeMin *= 1.1
        if countByTwo < t and pitchMin * 1.5 < pitchMax:
            pitchMax *= .9
            pitchMin *= 1.1
        if countByTwo < t:
            countByTwo += 2

            # print
            # print ("pitchMax: %f ")% pitchMax
            # print ("pitchMin: %f ")% pitchMin
            # print ("volumeMax: %f ")% volumeMax
            # print ("volumeMin: %f ")% volumeMin
            # print

        #print volume
        # print "pitch color: %i" % pitchColor
        print ("pitch: %f ")% pitch
        print ("pitchMax: %f ")% pitchMax
        print ("pitchMin: %f ")% pitchMin
        print tolerance
        print ("volumeMax: %f ")% volumeMax
        print ("volumeMin: %f ")% volumeMin
        print ("volume %f") % volume
        print delay
        print
        # print ("time: %f") % t
        # print ("count by two: %i") % countByTwo
        # print loopCount
        # print ("Loops per sec: %i ") % int(loopCount / t)
        # print



        pixels = [musicv2(t, coord, ii, n_pixels) for ii, coord in enumerate(coordinates)]
        client.put_pixels(pixels, channel=0)
    else:
        pixels = [pixel_color(t, coord, ii, n_pixels) for ii, coord in enumerate(coordinates)]
        client.put_pixels(pixels, channel=0)


    if touchOSC.kill == 1:
        killSwitch()
    if touchOSC.system11 == 1:
        restartPython()
    elif touchOSC.system21 == 1:
        killSwitch()
    elif touchOSC.system31 == 1:
        restartPi()
    elif touchOSC.system41 == 1:
        shutdownPi()
    audio.run = run_audio
    touchOSC.run = run_touchOSC
