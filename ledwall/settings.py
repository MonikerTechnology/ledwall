# This class stores the current settings
# TODO: add option to pickle this??
import logging


# curl -X GET 'http://localhost:8080/?id=3&hsv=1,2,3&mode=pizza'
# curl -X GET 'http://localhost:8080/?id=3&power=1&mode=audio_bars'

class settings:

    def __init__(self):
        self.logger = logging.getLogger(f'Settings')
        self.mode = "rainbow"
        self._power = 1
        self._brightness = 1.0  # 0 is off, 1 is full
        self.rgb = (0, 0, 0)
        self.rgb_last = (0, 0, 0)
        self.scenes = {
                "rainbow": (2, 2, 1),
                "rainbow_cycle": (17, 43, 16),
                "theater chase": (10, 6, 6),
                "rgb": (25, 6, 7)}

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        if value in [1, True, "on", "On", "ON"]:
            self._power = 1
        else:
            self._power = 0

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = value

    def check_for_scene(self):
        for scene, color_code in self.scenes.items():
            if color_code == self.rgb:
                self.brightness = 1
                return scene
        return None

    def update_brightness(self, value):
        """Give new brightness value 0-1"""
        pass

    def modify_brightness(self, value):
        """Add or subtract from brightness value
            Maintain range 0-1 """

        self.brightness += value

        if self.brightness > 1:
            self.brightness = 1
        if self.brightness < 0:
            self.brightness = 0

    def update_values(self, **kwargs):
        """update_values(rgb=(100,200,100))"""
        for key, value in kwargs.items():

            if isinstance(value, list):
                logging.debug("%s == %s" % (key, value[0]))
                setattr(self, key, value[0])

            else:
                logging.debug("%s == %s" % (key, value))
                setattr(self, key, value)

            new_mode = self.check_for_scene()
            if new_mode:
                self.mode = new_mode

        logging.info(f"Current mode is: {self.mode}")
        logging.info(f"Current power is: {self.power}")
        logging.info(f"Current brightness is: {self.brightness}")


settings = settings()