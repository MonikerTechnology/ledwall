#!/usr/bin/env python

from __future__ import division
# import colorsys
import argparse
import json
import logging

import os
import platform
import random
# import requests
import time
# import subprocess
import sys

# My custom
import animation
from audio_processing import *
from led_board import http_server, opc

# import googleAssistant
logger = logging.getLogger(f'ledwall.{__name__}')
debug = logging.WARNING

logging.basicConfig(level=debug, format=f'%(asctime)s %(levelname)s %(name)s %(lineno)s %(message)s')
# format='%(asctime)s %levelname)s: %(message)s',
#                         datefmt='%m/%d/%Y %I:%M:%S %p'
logging.info(f"Logging level: {str(debug)}")


run_main = True


def get_args():
    global debug

    parser = argparse.ArgumentParser(description="Interactive Programming Game")

    parser.add_argument('-d', '--debug', action='count', help='Increase debug level for each -d')

    parser.add_argument('-l', '--layout', dest='layout', default='../v2/supporting_files/ledwall15x9.json',
                        action='store', type=str, required=False,
                        help='layout file')
    parser.add_argument('-s', '--server', dest='server', default='localhost:7890',
                        action='store', type=str,
                        help='ip and port of server')
    parser.add_argument('-f', '--fps', dest='fps', default=30,
                        action='store', type=int,
                        help='frames per second')
    arguments = parser.parse_args()

    if arguments.debug:
        # Turn up the logging level
        debug -= arguments.debug * 10
        if debug < 0:
            debug = 0
        logging.getLogger().setLevel(debug)
        logging.warning(f'Updated log level to: {logging.getLevelName(debug)}({debug})')

    return arguments

# Main kill switch to stop the threads
def kill_switch():
    global run_main
    run_main = False

    logger.info(f'Stopping audio loop')
    audio_obj.run = False

    logger.info(f'Stopping http_server')
    http_server.httpd.server_close()

    # sudo kill $(ps aux | grep 'fadecandy' | awk '{print $2}')
    # sudo kill $(ps aux | grep 'main.py' | awk '{print $2}')

    # log.info(file, "killing googleAssistant")
    # googleAssistant.run = False

    logger.info(f"killing fadecandy server")
    # os.system("sudo kill $(ps aux | grep 'fadecandy' | awk '{print $2}')")
    os.system("killall fcserver")
    time.sleep(.5)

    logger.info(f"Killing main")

    logger.info(f"Setting pixels to 0,0,0")
    pixels = [(0, 0, 0) for ii, coord in enumerate(coordinates)]  # set all the pixels to off
    client.put_pixels(pixels, channel=0)

    logger.info(f"Is the HTTPserver thread running " + str(http_server.server_thread.is_alive()))
    # logging.info(f"{file} Is the googleAssistant thread running " + str(t_googleAssistant.is_alive()))

    return None


def restart_pi():
    pixels = [(0, 0, 0) for ii, coord in enumerate(coordinates)]
    client.put_pixels(pixels, channel=0)
    os.system("sudo shutdown -r now")


def shutdown_pi():
    pixels = [(0, 0, 0) for ii, coord in enumerate(coordinates)]
    client.put_pixels(pixels, channel=0)
    os.system("sudo shutdown now")


def restart_python():
    pixels = [(0, 0, 0) for ii, coord in enumerate(coordinates)]
    client.put_pixels(pixels, channel=0)
    os.system("sudo systemctl restart ledwall.service")


def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


print('about to get args')
args = get_args()
logger.info('got args')

if args.layout == 'supported_files/ledwall15x9.json':
    logger.info(f"No layout selected, using default layout: {str(args.layout)}")

logger.info(f'setup')


# -------------------------------------------------------------------------------
# Try to start fadecandy server

logger.info(f'Trying to start FC server...')


if platform.system() == "Darwin":
    logger.info(f'Backgrounding FC server for Mac and continuing with python')
    os.system("./fcserver-osx ./../v2/supporting_files/fcserver_config.json &")
if platform.system() == "Linux":
    logger.info(f'Backgrounding FC server for Linux and continuing with python')
    os.system("sudo /home/pi/fadecandy/bin/fcserver-rpi /home/pi/fadecandy/bin/fcserver_config.json &")


# logging.warning(f'{file} Failed to start FC server Maybe it is already running?')





time.sleep(1)
# -------------------------------------------------------------------------------
# Threading
# -------------------------------------------------------------------------------
# Threads for audio input and the threading all kill switch stuff

# Starts listening and server, launch via threading
logger.info(f"Starting audio loop")
audio_obj = AudioProcessor(num_pitch_ranges=15)


logger.info(f"Starting http_server")
http_server.start_server()

# add in a check to see if it stopped and restart it
# also check fadecandy

# log.header(file, "Starting googleAssistant server")
# t_googleAssistant.start()

# -------------------------------------------------------------------------------
# command line options for main







# -------------------------------------------------------------------------------
# parse layout file

logger.info(f'parsing FC layout file')

coordinates = []
for item in json.load(open(args.layout)):
    if 'point' in item:
        coordinates.append(tuple(item['point']))

# -------------------------------------------------------------------------------
# connect OPC to server

client = opc.Client(args.server)
if client.can_connect():
    logger.info(f'OPC connected to {args.server}')
else:
    # can't connect, but keep running in case the server appears later
    logger.warning(f'could not connect to {args.server}')

# -------------------------------------------------------------------------------
# Setup MQTT

# mode = "default"  # global
# lastMode = ""
# redMultiplier = 1
# greenMultiplier = 1
# blueMultiplier = 1

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

# message = HTTPserver.postDic
# mode = "rainbow"
# power = 0


# power message
# {"type":"power","power":1}
# {"power":1,"type":"power"}

# HSV message
# {"type":"HSV","HSV":{"H":123,"S":123,"V":123}}

# mode message
# {"type":"mode","mode":"rainbow"}

# -------------------------------------------------------------------------------
# color modes function


def pixel_color(t, coord, ii, n_pixels):
    # r,g,b = colorOSC
    r, g, b = 50, 50, 50
    r *= .95
    g *= .95
    b *= .95
    return (r, g, b)


# -------------------------------------------------------------------------------
# send pixels

logger.info(f'sending pixels forever (control-c to exit)...')

# -------------------------------------------------------------------------------

n_pixels = len(coordinates)


# fps counter
fps = FPS(args.fps)


random_values = [random.random() for ii in range(n_pixels)]
try:
    logger.info(f"about to start main loop")
    while run_main:

        # set looping variables
        t = fps.elapsed  # keep track of how long the program has been running

        # ----------------------------------------------
        # this tracks the FPS and adjusts the delay to keep it consistent.
        fps.maintain()

        if not http_server.http_data.power or http_server.http_data.mode != 'audio_bars':
            audio_obj.run = False
            pass

        if http_server.http_data.power:

            if http_server.http_data.mode == "rainbow":
                pixels = [animation.rainbow(t * scale(30, (1, 100), (.05, 2)), coord, ii, n_pixels, random_values) for ii, coord in
                          enumerate(coordinates)]
                client.put_pixels(pixels, channel=0)
            elif http_server.http_data.mode == "breathe":
                pixels = [animation.start_up(t, coord, ii, n_pixels) for ii, coord in enumerate(coordinates)]
                client.put_pixels(pixels, channel=0)

            elif http_server.http_data.mode == "audio_bars":
                audio_obj.capture = True
                audio_obj.update()
                pixels = animation.audio_bars(t, random_values, audio_obj, coordinates)
                # pixels = [animation.audio_bars(t * scale(30, (1, 100), (.05, 2)), coord, ii, n_pixels, random_values) for ii, coord in
                #          enumerate(coordinates)]
                client.put_pixels(pixels, channel=0)
            else:  # catch all maybe do loading
                nothing = 0

        if http_server.http_data.mode == "off" or http_server.http_data.power == 0:
        # add fade out!!

            pixels = [(0, 0, 0) for ii, coord in enumerate(coordinates)]  # set all the pixels to off
            client.put_pixels(pixels, channel=0)

except KeyboardInterrupt:
    logger.warning(f'Interrupt detected')
    kill_switch()  # shut down all the things as gracefully as possible
    sys.exit()
