from typing import Literal, NotRequired, TypedDict, Unpack
from app.helpers.config_base import ConfigBase

WindowConfigKeys = Literal[
    "window_title", "header_title", "width", "height", "background"
]


class TWindowConfig(TypedDict):
    window_title: str
    header_title: str
    width: int
    height: int
    background: str
    options: NotRequired[dict]


class WindowConfig[WindowConfigKeys](ConfigBase[WindowConfigKeys]):
    config: TWindowConfig

    def __init__(self, **kwargs: Unpack[TWindowConfig]):
        self.config = kwargs
