# This class stores the current settings
# TODO: add option to pickle this??
import logging


class Settings:

    @classmethod
    def __init__(cls):
        cls.mode = "rainbow"
        cls.power = 1

    @classmethod
    def update_values(cls, **kwargs):
        for key, value in kwargs.items():
            logging.debug("%s == %s" % (key, value))

            if isinstance(value, list):
                cls.key = value[0]
            else:
                cls.key = value



