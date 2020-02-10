try:
    import RPi.GPIO as GPIO
    rpi = True
except ImportError:
    rpi = False

import requests
import threading
from time import sleep
from ledwall.settings import Settings
Settings.__init__()

# self.capture_thread = threading.Thread(target=self._capture)


class Pysical:

    def __init__(self):
        if rpi:
            self.run = True
            self.clk = 17
            self.dt = 18

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

            self.counter = 0
            self.clkLastState = GPIO.input(self.clk)
            # self.capture_thread = threading.Thread(target=self._capture)
            self.run_loop = threading.Thread(target=self.run_loop)
            self.run_loop.start()
        else:
            print("Could not import from RPi import GPIO - Must run as root")

    def run_loop(self):
        try:
                while self.run:
                        clkState = GPIO.input(self.clk)
                        dtState = GPIO.input(self.dt)
                        if clkState != self.clkLastState:
                                if dtState != clkState:
                                        self.counter += 1
                                        # Settings.brightness += .05
                                        Settings.modify_brightness(.05)
                                        # payload = {'brightness': '.1'}
                                        # r = requests.get('http://localhost:8080', params=payload)

                                else:
                                        self.counter -= 1
                                        # Settings.brightness -= .05
                                        Settings.modify_brightness(-.05)
                                        # payload = {'brightness': '-0.1'}
                                        # r = requests.get('http://localhost:8080', params=payload)
                                print(Settings.brightness)
                        self.clkLastState = clkState
                        sleep(0.01)
        finally:
                GPIO.cleanup()




