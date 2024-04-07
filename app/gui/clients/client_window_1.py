from tkinter.ttk import Button, Style
from typing import Callable
from app.gui.framework.tkwindow import TKWindow
from app.config import theme_config, window_configs

class ClientWindow1(TKWindow):
    def __init__(self):
        super().__init__(False, window_configs.client_window_1, theme_config.ThemeConfig, theme_config.window_style)
        self.main_section()

    def main_section(self):
        main = self.main
        Button(main, text="Client 1").grid(row=0, column=2)
