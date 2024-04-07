from abc import ABC
from tkinter import Button
from tkinter.ttk import Style
from typing import Callable
from app.config.themes import ThemeConfig
from app.gui.framework.tkwindow import TKWindow
from app.gui.framework.window_config import WindowConfig


class BaseWindow(ABC, TKWindow):
    def init(self, config: WindowConfig, theme: ThemeConfig, window_style: Callable[..., Style]):
        super().__init__(config, theme, window_style)

        def main_section(self):
            main = self.main
            Button(main, text="Open Client 1", command=self.open_client_1).grid(row=0, column=2)
