import logging
from time import sleep
import tkinter as tk
from tkinter.ttk import Button, Entry, Frame, Label, Style
from typing import Callable
from app.api.iot_simulator import IoTSimulator
from app.gui.framework.tkwindow import TKWindow
from app.config import theme_config, window_configs

spacing_y = 10
spacing_x = 10

class DeviceWindow1(TKWindow):
    def __init__(self):
        super().__init__(False, window_configs.client_window_1, theme_config.ThemeConfig, theme_config.window_styles)

        logging.info("Opened Device 1")

        self.main_section()

        self.on_window_close(self.on_window_close_handler)

    def main_section(self):
        Button(self.main, text="Device 1").pack(
            pady=(spacing_y, spacing_y), side=tk.TOP, anchor=tk.NW)

        # frame = Frame(self.main)
        # frame.grid_columnconfigure(0, uniform="1", weight=1)
        # frame.grid_columnconfigure(1, uniform="1", weight=1)
        # frame.grid_rowconfigure(0)
        # frame.pack(expand=True, fill=tk.BOTH)

    def on_window_close_handler(self):
        self.window.destroy()
        IoTSimulator.stop_subscriber(1)
        logging.info("Closed Device 1")
