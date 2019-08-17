#!/usr/bin/python3


import argparse
import json
import logging

import os
import platform
import random
import requests
import time
# import subprocess
import sys

# My custom
from audioprocessing import *
from ledwall import http_server, opc, animation
from ledwall.settings import Settings


def get_args():
    global debug

    # -------------------------------------------------------------------------------
    # logging setup

    logging.getLogger(f'LedWall.{__name__}')
    debug = logging.WARNING

    logging.basicConfig(level=debug, format=f'%(asctime)s %(levelname)s %(name)s Line:%(lineno)s %(message)s')
    # format='%(asctime)s %levelname)s: %(message)s',
    #                         datefmt='%m/%d/%Y %I:%M:%S %p'
    logging.info(f"Logging level: {str(debug)}")

    parser = argparse.ArgumentParser(description="LED Board Controller")

    parser.add_argument('-d', '--debug', action='count', help='Increase debug level for each -d')

    parser.add_argument('-l', '--layout', dest='layout', default='ledwall/supporting_files/ledwall15x9.json',
                        action='store', type=str, required=False,
                        help='layout file')
    parser.add_argument('-s', '--server', dest='server', default='localhost:7890',
                        action='store', type=str,
                        help='ip and port of server')
    parser.add_argument('-f', '--fps', dest='fps', default=30,
                        action='store', type=int,
                        help='frames per second')
    parser.add_argument('-m', dest='mode', help='start mode: rainbow, audio_bars', default='rainbow')
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
def kill_switch(audio_obj, client, coordinates, args):

    global run_main
    print('\n\n')
    logging.info('Killing main loop')
    run_main = False

    logging.info(f'Stopping audio loop')
    audio_obj.stop_capturing()

    logging.info(f"Setting pixels to 0,0,0")
    # pixels = [(0, 0, 0) for ii, coord in enumerate(coordinates)]  # set all the pixels to off
    pixels = [(0, 0, 0)] * len(coordinates)
    client.put_pixels(pixels, channel=0)
    time.sleep(.25)

    logging.info(f'Stopping http_server')
    http_server.httpd.server_close()
    time.sleep(.25)
    # requests.get('http://localhost:8080')

    # sudo kill $(ps aux | grep 'fadecandy' | awk '{print $2}')
    # sudo kill $(ps aux | grep 'main.py' | awk '{print $2}')

    logging.info(f"killing fadecandy server")
    # os.system("sudo kill $(ps aux | grep 'fcserver' | grep -v grep | awk '{print $2}')")
    os.system("sudo killall fcserver-rpi")
    time.sleep(.5)

    if http_server.server_thread.is_alive():
        requests.get('http://localhost:8080')
    logging.info(f"Is the HTTP server thread running " + str(http_server.server_thread.is_alive()))

    print("\n\n")
    return None


def restart_pi(client, coordinates):
    # TODO simplify this
    pixels = [(0, 0, 0) for ii, coord in enumerate(coordinates)]
    client.put_pixels(pixels, channel=0)
    os.system("sudo shutdown -r now")


def shutdown_pi(client, coordinates):
    pixels = [(0, 0, 0) for ii, coord in enumerate(coordinates)]
    client.put_pixels(pixels, channel=0)
    os.system("sudo shutdown now")


def restart_python(client, coordinates):
    pixels = [(0, 0, 0) for ii, coord in enumerate(coordinates)]
    client.put_pixels(pixels, channel=0)
    os.system("sudo systemctl restart LedWall.service")


def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


def pixel_color(t, coord, ii, n_pixels):
    # r,g,b = colorOSC
    r, g, b = 50, 50, 50
    r *= .95
    g *= .95
    b *= .95
    return r, g, b


def start_fc_server(args):

    # TODO: first check if running
    # This will fail if it is already running, but it can still connect
    logging.info(f'Trying to start FC server...')

    # TODO stop using absalute path
    fc_mac = f'/usr/local/supporting_files/fcserver-osx'
    fc_rpi = f'/usr/local/supporting_files/fcserver-rpi'
    config_mac = f'/usr/local/supporting_files/fcserver_config.json'
    config = f'/usr/local/supporting_files/fcserver_config.json'

    if platform.system() == "Darwin":
        logging.info(f'Backgrounding FC server for Mac and continuing with python')
        os.system(f"{fc_mac} {config_mac} &")
    if platform.system() == "Linux":
        logging.info(f'Backgrounding FC server for Linux and continuing with python')
        os.system(f"sudo {fc_rpi} {config} &")

    time.sleep(.5)

    # -------------------------------------------------------------------------------
    # connect OPC to server

    client = opc.Client(args.server)
    if client.can_connect():
        logging.info(f'OPC connected to {args.server}')
    else:
        # can't connect, but keep running in case the server appears later
        logging.warning(f'could not connect to {args.server}')

    return client


def parse_layout():
    # parse layout file

    logging.info(f'parsing FC layout file')

    coordinates = []
    for item in json.load(open(f'/usr/local/supporting_files/ledwall15x9.json')):
        if 'point' in item:
            coordinates.append(tuple(item['point']))

    audio_coordinates = []
    for item in json.load(open(f'/usr/local/supporting_files/audio_coord.json')):
        if 'point' in item:
            audio_coordinates.append(tuple(item['point']))

    return coordinates, audio_coordinates


def main():

    run_main = True

    args = get_args()

    logging.info(f'setup')
    client = start_fc_server(args)

    time.sleep(1)

    # Starts listening and server, launch via threading
    logging.info(f"Starting audio loop")
    audio_obj = AudioProcessor(num_pitch_ranges=15, start=False)

    logging.info(f"Starting http_server")
    http_server.start_server()

    coordinates, audio_coordinates =  parse_layout()




    # -------------------------------------------------------------------------------
    # color modes function

    n_pixels = len(coordinates)

    # fps counter
    fps = FPS(args.fps)
    # TODO: Keep track of pixels last position to add in an optional fade

    random_values = [random.random() for ii in range(n_pixels)]

    Settings.__init__()

    value = [] # list from 0 - 250 - 0
    value.extend(range(0,250))
    value.extend(reversed(range(0,250)))

    try:
        logging.info(f"about to start main loop")
        Settings.power = 'On'
        Settings.mode = args.mode
        while run_main:

            # set looping variables
            t = fps.elapsed  # keep track of how long the program has been running

            # ----------------------------------------------
            # this tracks the FPS and adjusts the delay to keep it consistent.
            fps.maintain()

            if not Settings.power or Settings.mode != 'audio_bars':
                audio_obj.run = False

            if Settings.power.lower() in ('1', 'on', 1):

                if Settings.mode == "rainbow":

                    pixels = [animation.rainbow(t * scale(30, (1, 100), (.05, 2)), coord, ii, n_pixels,
                                                random_values) for ii, coord in
                                                enumerate(coordinates)]

                    client.put_pixels(pixels, channel=0)
                elif Settings.mode == "breathe":

                    pixels = [animation.start_up(t, coord, ii, n_pixels, value) for ii, coord in enumerate(coordinates)]

                    client.put_pixels(pixels, channel=0)

                elif Settings.mode == "audio_bars":
                    audio_obj.run = True
                    audio_obj.update()
                    pixels = animation.audio_bars(t, random_values, audio_obj, audio_coordinates)

                    # pixels = [animation.audio_bars(t * scale(30, (1, 100), (.05, 2)), coord, ii, n_pixels, random_values) for ii, coord in
                    #          enumerate(coordinates)]
                    client.put_pixels(pixels, channel=0)

                elif Settings.mode == "solid":
                    pixels = [animation.solid(t * scale(30, (1, 100), (.05, 2)), coord, ii, n_pixels, random_values) for ii, coord in
                              enumerate(coordinates)]
                    pixels = [(200, 200, 200)] * len(coordinates)
                    client.put_pixels(pixels, channel=0)

                else:  # catch all maybe do loading
                    pass

            if Settings.power.lower() in ['0', 'off', 0]:
                # add fade out!!

                pixels = [(0, 0, 0) for ii, coord in enumerate(coordinates)]  # set all the pixels to off
                client.put_pixels(pixels, channel=0)

    except KeyboardInterrupt:
        logging.warning(f'Interrupt detected')
        kill_switch(audio_obj, client, coordinates, args)  # shut down all the things as gracefully as possible
        sys.exit()


if __name__ == '__main__':
    main()