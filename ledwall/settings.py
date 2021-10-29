# This class stores the current settings
# TODO: add option to pickle this??
import logging


# curl -X GET 'http://localhost:8080/?id=3&hsv=1,2,3&mode=pizza'
# curl -X GET 'http://localhost:8080/?id=3&power=1&mode=audio_bars'

class Settings:
    # rgb = (0, 0, 0)
    # rgb_last = (0, 0, 0)
    # scenes = {
    #     "rainbow": (2, 2, 1),
    #     "theater chase": (10, 6, 6)}
    # brightness = 1.0
    # power = "On"
    # mode = "rainbow"

    def __init__(self):
        self.logger = logging.getLogger(f'Settings')
        self.mode = "rainbow"
        self.power = "1"
        self.brightness = 1.0  # 0 is off, 1 is full
        self.rgb = (0, 0, 0)
        self.rgb_last = (0, 0, 0)
        self.scenes = {
                "rainbow": (2, 2, 1),
                "theater chase": (10, 6, 6)}

    def check_for_scene(self):
        for scene, value in self.scenes.items():
            if value == self.rgb:
                return scene
        return "rgb"  # Basic scene

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

            self.mode = self.check_for_scene()

        logging.info(f"Current mode is: {self.mode}")
        logging.info(f"Current power is: {self.power}")
        logging.info(f"Current brightness is: {self.brightness}")


settings = Settings()