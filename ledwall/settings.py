# This class stores the current settings
# TODO: add option to pickle this??


def test():
    print('pizza Test is good\n\n')

class Settings:

    @classmethod
    def __init__(cls):
        cls.mode = "rainbow"
        cls.power = 1
