# This class stores the current settings
# TODO: add option to pickle this??
import logging


class Settings:

    @classmethod
    def __init__(cls):
        cls.logger = logging.getLogger(f'Settings')
        cls.mode = "rainbow"
        cls.power = 1

    @classmethod
    def update_values(cls, **kwargs):
        for key, value in kwargs.items():

            if isinstance(value, list):
                logging.debug("%s == %s" % (key, value[0]))
                setattr(cls, key, value[0])

            else:
                logging.debug("%s == %s" % (key, value))
                setattr(cls, key, value)

        logging.debug(f"Current mode is: {cls.mode}")
        logging.debug(f"Current power is: {cls.power}")



