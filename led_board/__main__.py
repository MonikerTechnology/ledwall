#!/usr/bin/python3

import sys
print(sys.path)

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
from audio_processing import *
from led_board import http_server, opc, animation
from led_board.settings import Settings




# import googleAssistant

def get_args():
    global debug

    parser = argparse.ArgumentParser(description="LED Board Controller")

    parser.add_argument('-d', '--debug', action='count', help='Increase debug level for each -d')

    parser.add_argument('-l', '--layout', dest='layout', default='led_board/supporting_files/ledwall15x9.json',
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

    logger.info('Killing main loop')
    run_main = False

    logger.info(f'Stopping audio loop')
    audio_obj.start_capturing()

    logger.info(f'Stopping http_server')
    http_server.httpd.server_close()

    # sudo kill $(ps aux | grep 'fadecandy' | awk '{print $2}')
    # sudo kill $(ps aux | grep 'main.py' | awk '{print $2}')

    # log.info(file, "killing googleAssistant")
    # googleAssistant.run = False

    logger.info(f"killing fadecandy server")
    os.system("kill $(ps aux | grep 'fcserver' | grep -v grep | awk '{print $2}')")
    # os.system("killall fcserver")
    time.sleep(.5)

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


# -------------------------------------------------------------------------------
# logging setup

logger = logging.getLogger(f'ledwall.{__name__}')
debug = logging.WARNING

logging.basicConfig(level=debug, format=f'%(asctime)s %(levelname)s %(name)s Line:%(lineno)s %(message)s')
# format='%(asctime)s %levelname)s: %(message)s',
#                         datefmt='%m/%d/%Y %I:%M:%S %p'
logging.info(f"Logging level: {str(debug)}")


run_main = True

# -------------------------------------------------------------------------------
# args

args = get_args()

if args.layout == 'supported_files/ledwall15x9.json':
    logger.info(f"No layout selected, using default layout: {str(args.layout)}")

logger.info(f'setup')

# -------------------------------------------------------------------------------
# Try to start fadecandy server

logger.info(f'Trying to start FC server...')

print('\nls of .')
os.system('sudo ls')

print('\nls of supporting_files')
os.system('sudo  ls supporting_files')

print('\nls of led_board')
os.system('sudo ls led_board')
print()

if platform.system() == "Darwin":
    logger.info(f'Backgrounding FC server for Mac and continuing with python')
    os.system(f"led_board/supporting_files/fcserver-osx led_board/supporting_files/fcserver_config.json &")
if platform.system() == "Linux":
    logger.info(f'Backgrounding FC server for Linux and continuing with python')
    os.system(f"sudo led_board/supporting_files/fcserver-rpi led_board/supporting_files/fcserver_config.json &")


# logging.warning(f'{file} Failed to start FC server Maybe it is already running?')

time.sleep(1)
# -------------------------------------------------------------------------------
# Threading
# -------------------------------------------------------------------------------
# Threads for audio input and the threading all kill switch stuff

# Starts listening and server, launch via threading
logger.info(f"Starting audio loop")
audio_obj = AudioProcessor(num_pitch_ranges=15, start=False)


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
print('l\ns')
os.system('ls')
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
# TODO: Keep track of pixels last position to add in an optional fade

random_values = [random.random() for ii in range(n_pixels)]

Settings.__init__()

try:
    logger.info(f"about to start main loop")
    while run_main:

        # set looping variables
        t = fps.elapsed  # keep track of how long the program has been running

        # ----------------------------------------------
        # this tracks the FPS and adjusts the delay to keep it consistent.
        fps.maintain()
        Settings.mode = "rainbow"
        if not Settings.power or Settings.mode != 'audio_bars':
            audio_obj.run = False

        if Settings.power:

            # Force for testing
            Settings.mode = "rainbow"
            if Settings.mode == "rainbow":

                pixels = [animation.rainbow(t * scale(30, (1, 100), (.05, 2)), coord, ii, n_pixels,
                                                      random_values) for ii, coord in
                                                      enumerate(coordinates)]
                client.put_pixels(pixels, channel=0)
            elif Settings.mode == "breathe":
                pixels = [animation.start_up(t, coord, ii, n_pixels) for ii, coord in enumerate(coordinates)]
                client.put_pixels(pixels, channel=0)

            elif Settings.mode == "audio_bars":
                audio_obj.update()
                pixels = animation.audio_bars(t, random_values, audio_obj, coordinates)
                # pixels = [animation.audio_bars(t * scale(30, (1, 100), (.05, 2)), coord, ii, n_pixels, random_values) for ii, coord in
                #          enumerate(coordinates)]
                client.put_pixels(pixels, channel=0)
            elif Settings.mode == "solid":
                pixels = [animation.solid(t * scale(30, (1, 100), (.05, 2)), coord, ii, n_pixels, random_values) for ii, coord in
                          enumerate(coordinates)]
            else:  # catch all maybe do loading
                nothing = 0

        if Settings.mode == "off" or Settings.power == 0:
        # add fade out!!

            pixels = [(0, 0, 0) for ii, coord in enumerate(coordinates)]  # set all the pixels to off
            client.put_pixels(pixels, channel=0)

except KeyboardInterrupt:
    logger.warning(f'Interrupt detected')
    kill_switch()  # shut down all the things as gracefully as possible
    sys.exit()
