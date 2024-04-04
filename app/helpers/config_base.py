from typing import Any, Generic, TypeVar

T = TypeVar("T")

class ConfigBase(Generic[T]):
    config: dict[Any, Any] = {}

    def __init__(self, **kwargs):
        # self.config = kwargs
        ...

    def __getattr__(self, key: T):
        if not key in self.config:
            print(f'\nError: missing key `{key}` in configuration object.')
            return
        return self.config[key]

    def __setattr__(self, key: T, value):
        if key == "config":
            self.__dict__["config"] = value
            return

        self.config[key] = value
        return value

    def __getitem__(self, key: T):
        return self.config[key]

    def __setitem__(self, key: T, value):
        self.config[key] = value

    def __iter__(self):
        for el in self.config:
            yield el

    def __repr__(self):
        return f"{self.config}"
