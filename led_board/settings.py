# This class stores the current settings
# TODO: add option to pickle this??


class Settings:

    @classmethod
    def __init__(cls):
        cls.test_data = [1]
        cls.mode = ['start_up']
        cls.last_mode = ['']
        cls.power = [1]

    @classmethod
    def __getitem__(cls, key):
        return cls.__dict__[key]

    @classmethod
    def __setitem__(cls, key, value):
        cls.__dict__[key] = value

    @classmethod
    def update_values(cls, **kwargs):
        allowed_keys = {'mode', 'power', 'test_data'}
        # self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

        for k, v in kwargs.items():
            if k in allowed_keys:
                if k.lower() == 'mode':  # Then save to last_mode
                    if len(v) == 1 and isinstance(v, list):
                        cls.last_mode = cls.mode[0]
                    else:
                        cls.last_mode = cls.mode[0]
                if len(v) == 1 and isinstance(v, list):
                    cls.__dict__.update({k: v[0]})
                else:
                    cls.__dict__.update({k: v})

    @classmethod
    def print_all(cls):
        for key in cls.__dict__.keys():
            print(f'{key}: {cls.__dict__[key]}')
        print()