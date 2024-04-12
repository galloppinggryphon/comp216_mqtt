from typing import Any, Callable, Concatenate, Optional, ParamSpec, Protocol, TypeVar

"""
Based on https://stackoverflow.com/a/77674576/8785542
"""

P = ParamSpec("P")
SelfT = TypeVar("SelfT", contravariant=True)


class Init(Protocol[SelfT, P]):
    def __call__(__self, self: SelfT, *args: P.args, **kwds: P.kwargs) -> None:
        ...


def super_init(init: Callable[Concatenate[SelfT, P], None], on_init: Optional[Callable] = None) -> Init[SelfT, P]:
    def __init__(self: SelfT, *args: P.args, **kwargs: P.kwargs) -> None:
        # Like calling super()
        init(self, *args, **kwargs)

        if on_init:
            on_init(self, *args, **kwargs)

    return __init__


# class Parent:
#     def __init__(self, a: int, b: str, c: float) -> None:
#         self.a = a
#         self.b = b
#         self.c = c


# class Child(Parent):
#     def init(self, *args, **kwargs):
#         print(self, *args, **kwargs)

#     __init__ = preserve_init(Parent.__init__, init)

# Child(1, "123", 123)
