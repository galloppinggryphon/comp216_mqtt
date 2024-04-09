from __future__ import annotations
import logging
import tkinter as tk

### IMPORT ALL COMPONENTS FROM TTK IF POSSIBLE! ###
from tkinter.ttk import Frame, Button, Label

from app.api.iot_simulator import IoTSimulator
from app.config import theme_config, window_configs
from app.gui.clients.client_window_1 import ClientWindow1
from app.gui.framework.tkwindow import TKWindow

class MainWindow(TKWindow):
    device_list_container: Frame
    client_list_container: Frame

    def __init__(self):
        super().__init__(True, window_configs.main_window_config,
                         theme_config.ThemeConfig, theme_config.window_styles)
        self.main_section()

    def main_section(self):
        wrapper = Frame(self.main)
        wrapper.grid_columnconfigure(0, weight=1)
        wrapper.grid_columnconfigure(1, weight=1)
        wrapper.grid_rowconfigure(0)
        wrapper.pack(expand=True, fill=tk.BOTH)

        self.device_list_container = Frame(wrapper)
        # device_list_box.pack(pady=(0, 25))
        self.device_list_container.grid(row=0, column=0)

        self.client_list_container = Frame(wrapper)
        self.client_list_container.grid(row=0, column=1)

        self.draw_client_list()
        self.draw_device_list()

    def draw_device_list(self):
        spacing_y = 2
        spacing_x = 5

        parent = self.device_list_container

        # Devices
        Label(parent, text="IoT devices", justify="left").pack(
            padx=(spacing_x, spacing_x), pady=(0, 5))

        row1 = Frame(parent)
        row1.pack(pady=(spacing_y, spacing_y), side=tk.BOTTOM)
        Label(row1, text="Device 1", justify="left").pack(
            padx=(spacing_x, spacing_x))
        Button(row1, text="Start", command=self.start_device_1).pack(
            padx=(spacing_x, spacing_x), side=tk.LEFT)
        Button(row1, text="Stop", command=self.stop_device_1).pack(
            padx=(spacing_x, spacing_x), side=tk.LEFT)

    def draw_client_list(self):
        spacing_y = 2
        spacing_x = 5

        parent = self.client_list_container

        Label(parent, text="Clients", justify="left").pack(
            padx=(spacing_x, spacing_x), pady=(0, 5))
        Button(parent, text="Open Client 1", command=self.open_client_1).pack(
            padx=(spacing_x, spacing_x), pady=(spacing_y, spacing_y))
        Button(parent, text="Open Client 2", command=self.open_client_1).pack(
            padx=(spacing_x, spacing_x), pady=(spacing_y, spacing_y))


    def open_client_1(self):
        ClientWindow1()


    def start_device_1(self):
        IoTSimulator.start_publisher('temp_sensor')

    def stop_device_1(self):
        IoTSimulator.stop_publisher('temp_sensor')
