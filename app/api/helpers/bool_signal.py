# TODO: not sure if this is threadsafe
class BoolSignal:
    """
    Signal listeners/loops can check to trigger actions (e.g. break).
    """
    __value = False

    @property
    def abort(self):
        return self.__value

    @property
    def is_true(self):
        return self.__value

    def __call__ (self):
        self.__value = True

    def __str__ (self):
        return f"{self.__value}"
