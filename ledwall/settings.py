# This class stores the current settings
# TODO: add option to pickle this??
import logging


# curl -X GET 'http://localhost:8080/?id=3&hsv=1,2,3&mode=pizza'
# curl -X GET 'http://localhost:8080/?id=3&power=1&mode=audio_bars'

class Settings:

    @classmethod
    def __init__(cls):
        cls.logger = logging.getLogger(f'Settings')
        cls.mode = "rainbow"
        cls.power = "1"
        cls.brightness = 1.0  # 0 is off, 1 is full

    @classmethod
    def update_brightness(cls, value):
        """Give new brightness value 0-1"""
        pass

    @classmethod
    def modify_brightness(cls, value):
        """Add or subtract from brightness value
            Maintain range 0-1 """

        cls.brightness += value

        if cls.brightness > 1:
            cls.brightness = 1
        if cls.brightness < 0:
            cls.brightness = 0

    @classmethod
    def update_values(cls, **kwargs):
        for key, value in kwargs.items():

            if isinstance(value, list):
                logging.debug("%s == %s" % (key, value[0]))
                setattr(cls, key, value[0])

            else:
                logging.debug("%s == %s" % (key, value))
                setattr(cls, key, value)

        logging.info(f"Current mode is: {cls.mode}")
        logging.info(f"Current power is: {cls.power}")
        logging.info(f"Current brightness is: {cls.brightness}")
