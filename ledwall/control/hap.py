"""
 Apple Homekit API Call Order
 User changes light settings on iOS device
 Changing Brightness - State - Hue - Brightness
 Changing Color      - Saturation - Hue
 Changing Temp/Sat   - Saturation - Hue
 Changing State      - State
"""

from neopixel import *
from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB
from ledwall.settings import Settings
import threading
import socket
Settings.__init__()


class NeoPixelLightStrip(Accessory):

    category = CATEGORY_LIGHTBULB

    def __init__(self, LED_pin, LED_count, *args, **kwargs):

        """
        LED_Count - the number of LEDs in the array
        is_GRB - most neopixels are GRB format - Normal:True
        LED_pin - must be PWM pin 18 - Normal:18
        LED_freq_hz - frequency of the neopixel leds - Normal:800000
        LED_DMA - Normal:10
        LED_Brightness - overall brightness - Normal:255
        LED_invert - Normal:False
        For more information regarding these settings
            please review rpi_ws281x source code
        """

        super().__init__(*args, **kwargs)

        self.set_info_service(
            manufacturer='Cody McComber',
            model='Raspberry Pi',
            firmware_revision='1.0',
            serial_number='1',
            # AccessoryFlags="AccessoryFlags Test"
        )

        # Set our neopixel API services up using Lightbulb base
        serv_light = self.add_preload_service(
            'Lightbulb', chars=['On', 'Hue', 'Saturation', 'Brightness'])

        # Configure our callbacks
        self.char_hue = serv_light.configure_char(
            'Hue', setter_callback=self.set_hue)
        self.char_saturation = serv_light.configure_char(
            'Saturation', setter_callback=self.set_saturation)
        self.char_on = serv_light.configure_char(
            'On', setter_callback=self.set_state)
        self.char_on = serv_light.configure_char(
            'Brightness', setter_callback=self.set_brightness)

        # Set our instance variables
        self.accessory_state = 0  # State of the neo light On/Off
        self.hue = 0  # Hue Value 0 - 360 Homekit API
        self.saturation = 100  # Saturation Values 0 - 100 Homekit API
        self.brightness = 100  # Brightness value 0 - 100 Homekit API

        # self.is_GRB = is_GRB  # Most neopixels are Green Red Blue
        self.LED_count = LED_count

        order = GRB
        # self.neo_strip = NeoPixel(LED_pin, LED_count, pixel_order=order)
        # self.neo_strip.begin()

    def set_state(self, value):
        self.accessory_state = value
        if value == 1:  # On
            self.set_hue(self.hue)
        else:
            self.update_neopixel_with_color(0, 0, 0)  # Off

    def set_hue(self, value):
        # Lets only write the new RGB values if the power is on
        # otherwise update the hue value only
        if self.accessory_state == 1:
            self.hue = value
            rgb_tuple = self.hsv_to_rgb(
                self.hue, self.saturation, self.brightness)
            if len(rgb_tuple) == 3:
                self.update_neopixel_with_color(
                    rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
        else:
            self.hue = value

    def set_brightness(self, value):
        self.brightness = value
        self.set_hue(self.hue)

    def set_saturation(self, value):
        self.saturation = value
        self.set_hue(self.hue)

    def update_neopixel_with_color(self, red, green, blue):
        #for i in range(self.LED_count):
        # self.neo_strip.fill((red, green, blue))
        print("Uppdating settings to:", (red, green, blue))
        Settings.update_values(rgb=(red, green, blue))
        # Settings.rgb = (red, green, blue)
            # Red,Green,Blue
        #self.neo_strip.show()

    def hsv_to_rgb(self, h, s, v):
        """
        This function takes
         h - 0 - 360 Deg
         s - 0 - 100 %
         v - 0 - 100 %
        """

        hPri = h / 60
        s = s / 100
        v = v / 100

        if s <= 0.0:
            return int(0), int(0), int(0)

        C = v * s  # Chroma
        X = C * (1 - abs(hPri % 2 - 1))

        RGB_Pri = [0.0, 0.0, 0.0]

        if 0 <= hPri <= 1:
            RGB_Pri = [C, X, 0]
        elif 1 <= hPri <= 2:
            RGB_Pri = [X, C, 0]
        elif 2 <= hPri <= 3:
            RGB_Pri = [0, C, X]
        elif 3 <= hPri <= 4:
            RGB_Pri = [0, X, C]
        elif 4 <= hPri <= 5:
            RGB_Pri = [X, 0, C]
        elif 5 <= hPri <= 6:
            RGB_Pri = [C, 0, X]
        else:
            RGB_Pri = [0, 0, 0]

        m = v - C

        return int((RGB_Pri[0] + m) * 255), int((RGB_Pri[1] + m) * 255), int((RGB_Pri[2] + m) * 255)

"""An example of how to setup and start an Accessory.

This is:
1. Create the Accessory object you want.
2. Add it to an AccessoryDriver, which will advertise it on the local network,
    setup a server to answer client queries, etc.
"""
import logging
import signal
import random

from pyhap.accessory import Accessory
from pyhap.accessory_driver import AccessoryDriver
# from accessories.NeoPixelLightStrip import NeoPixelLightStrip
import pyhap.loader as loader
# from pyhap import camera
# from pyhap.const import CATEGORY_SENSOR
import board
from time import sleep

logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")


def get_accessory(driver):
    """Call this method to get a standalone Accessory."""
    return NeoPixelLightStrip(board.D12, 135, driver, "led-wall")
    # return TemperatureSensor(driver, 'MyTempSensor')


def wait_for_network():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    count = 0
    while True:
        try:
            s.connect(("8.8.8.8", 80))
            sleep(count)
            if count < 60:
                count += 1
            break
        except OSError:
            pass
    print(f"Found local IP address: {s.getsockname()[0]}")
    s.close()


def main():
    wait_for_network()
    # Start the accessory on port 51826
    driver = AccessoryDriver(port=51826, persist_file='/home/pi/github/HAP-python/accessory.state')

    # Change `get_accessory` to `get_bridge` if you want to run a Bridge.
    driver.add_accessory(accessory=get_accessory(driver))

    # We want SIGTERM (terminate) to be handled by the driver itself,
    # so that it can gracefully stop the accessory, server and advertising.
    signal.signal(signal.SIGTERM, driver.signal_handler)

    # Start it!
    # driver.start()
    run_loop = threading.Thread(target=driver.start)
    run_loop.start()


if __name__ == "__main__":
    main()
