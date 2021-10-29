try:
    import RPi.GPIO as GPIO
    rpi = True
except ImportError:
    rpi = False

import sys
import threading
from time import sleep
from ledwall.settings import settings
import signal
settings.__init__()

# self.capture_thread = threading.Thread(target=self._capture)

def kill_switch(a, b):
    print("Ran the kill switch from rotary!!")
    sys.exit()

class Physical:

    def __init__(self):
        signal.signal(signal.SIGTERM, kill_switch)
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
                                        settings.modify_brightness(.05)

                                else:
                                        settings.modify_brightness(-.05)
                                print(settings.brightness)
                        self.clkLastState = clk_state
                        sleep(0.01)
        finally:
                GPIO.cleanup()




