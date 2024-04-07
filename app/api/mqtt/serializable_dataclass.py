import json
from numpy import ndarray

def SerializableDataclass(cls):
    """
    Decorator that adds a serialization method to a dataclass.
    Note: @dataclass must be the last decorator to be declared above the class signature.
    Numpy safe.
    """
    class WrapClass(cls):
        def to_json(self):
            _dict = {}
            for key in self.__dataclass_fields__.keys():
                value = getattr(self, key)

                # numpy arrays need custom handling
                if isinstance(value, ndarray):
                    _dict[key] = list(value)
                else:
                    _dict[key] = value

            return json.dumps(_dict)

    return WrapClass
