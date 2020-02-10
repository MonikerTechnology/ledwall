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


class Physical:

    def __init__(self):
        if rpi:
            self.run = True
            self.clk = 17
            self.dt = 18

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

            self.clkLastState = GPIO.input(self.clk)
            self.run_loop = threading.Thread(target=self.run_loop)
            self.run_loop.start()
        else:
            print("Could not 'import RPi.GPIO as GPIO' - Must run as root")

    def run_loop(self):
        try:
                while self.run:
                        clk_state = GPIO.input(self.clk)
                        dt_state = GPIO.input(self.dt)
                        if clk_state != self.clkLastState:
                                if dt_state != clk_state:
                                        Settings.modify_brightness(.01)

                                else:
                                        Settings.modify_brightness(-.01)
                                print(Settings.brightness)
                        self.clkLastState = clk_state
                        sleep(0.01)
        finally:
                GPIO.cleanup()




