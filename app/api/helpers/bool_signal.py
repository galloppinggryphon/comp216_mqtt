# TODO: not sure if this is threadsafe
class BoolSignal:
    """
    Signal listeners/loops can check to trigger actions (e.g. break).
    """
    __value: bool

    @property
    def value(self):
        return self.__value

    def __init__(self, initial_value: bool = False):
        self.__value = initial_value

    def reset(self):
        self.__value = False

    def __call__ (self):
        self.__value = True

    def __str__ (self):
        return f"{self.__value}"

    def __repr__(self):
        return self.__value
