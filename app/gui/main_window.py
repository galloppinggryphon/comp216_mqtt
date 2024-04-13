from __future__ import annotations
import logging
import tkinter as tk

### IMPORT ALL COMPONENTS FROM TTK IF POSSIBLE! ###
from tkinter.ttk import Frame, Button, Label
from typing import Callable
import weakref

from app.api.helpers.iot_device_config import IoTDeviceConfig
from app.api.iot_simulator import IoTSimulator
from app.config import theme_config, window_configs
from app.config import device_config
from app.gui.clients.client_window_1 import ClientWindow1
from app.gui.framework.tkwindow import TKWindow
from app.gui.framework.toggle_button import ToggleButton

spacing_y = 2
spacing_x = 5


class MainWindow(TKWindow):
    controls: dict[str, tk.Widget | ToggleButton]
    windows: weakref.WeakValueDictionary[str, TKWindow]
    client_win: TKWindow

    def __init__(self):
        super().__init__(True, window_configs.main_window_config,
                         theme_config.ThemeConfig, theme_config.window_styles)

        self.windows = weakref.WeakValueDictionary()
        self.controls = {}
        self.main_section()

    def main_section(self):
        wrapper = Frame(self.main)
        wrapper.grid_columnconfigure(0, uniform=1)
        wrapper.grid_columnconfigure(1, uniform=1)
        wrapper.grid_rowconfigure(0)
        wrapper.pack(expand=True, fill=tk.BOTH)

        device_list_container = Frame(wrapper)
        device_list_container.grid(row=0, column=0)
        # device_list_box.pack(pady=(0, 25))

        client_list_container = Frame(wrapper)
        client_list_container.grid(row=0, column=1)

        self.controls["device_list_container"] = device_list_container
        self.controls["client_list_container"] = client_list_container

        self.draw_client_list()
        self.draw_device_list()

    def draw_client_list(self):
        parent = self.controls["client_list_container"]
        Label(parent, text="Clients", justify="left").pack(
        padx=(spacing_x, spacing_x), pady=(0, 5))

        self.add_client(1)
        self.add_client(2)

    def draw_device_list(self):
        parent = self.controls["device_list_container"]

        # Devices
        Label(parent, text="IoT devices", justify="left").pack(
            padx=(spacing_x, spacing_x), pady=(0, 5))

        for device in device_config:
            self.add_device(device)

    def add_device(self, device_config: IoTDeviceConfig):

        parent = self.controls["device_list_container"]

        row = Frame(parent)
        row.pack(pady=(spacing_y, spacing_y), side=tk.TOP)
        Label(row, text=device_config.title, justify="left").pack(
            padx=(spacing_x, spacing_x), side=tk.LEFT)

        # TOGGLE BUTTON -->
        start_toggle = ToggleButton(row, text="►", width=0)
        start_toggle.pack(padx=(spacing_x, spacing_x), side=tk.LEFT)

        # Register callback
        def toggle_on_handler(current_state, new_state, event, is_virtual):
             logging.debug(f'toggle_on_handler {(current_state, new_state, event, is_virtual)}')
             if not current_state:
                self.start_device(device_config, start_toggle)
             return True

        def toggle_off_handler(current_state, new_state, event, is_virtual):
             logging.debug(f'toggle_off_handler {(current_state, new_state, event, is_virtual)}')
             return False if is_virtual else True

        start_toggle.on_toggle(toggle_on_callback=toggle_on_handler, toggle_off_callback=toggle_off_handler)
        self.controls[f"start_device_{device_config.id}"] = start_toggle
        # <-- TOGGLE BUTTON

        Button(row, text="⬛", command=lambda: self.stop_device(device_config), width=0).pack(
            padx=(spacing_x, spacing_x), side=tk.LEFT)
        Button(row, text="🔧", command=lambda: ..., width=0).pack(
            padx=(spacing_x, spacing_x), side=tk.LEFT)

    def add_client(self, client_id: int):
        parent = self.controls["client_list_container"]

        row = Frame(parent)
        row.pack(pady=(spacing_y, spacing_y), side=tk.TOP)
        Label(row, text=f"Client {client_id}", justify="left").pack(
        padx=(spacing_x, spacing_x), pady=(0, 5), side=tk.LEFT)

        Button(row, text="Open", command=lambda: self.open_client_window(client_id)).pack(
            padx=(spacing_x, spacing_x), pady=(spacing_y, spacing_y), side=tk.LEFT)

    def open_client_window(self, client_id: int):
        match client_id:
            case 1:
                if not self.window_exists('ClientWindow1'):
                    self.windows['ClientWindow1'] = ClientWindow1()
            case 2:
                print(self.client_win)

    def open_device_window(self, device_id: int):
        match device_id:
            case 1: ...

    def window_exists(self, name):
        exists = name in self.windows

        if exists and self.windows[name].is_window_open():
            logging.info(f"Window '{name}' is already open.")
            return True

        return False


    def start_device(self, device_config: IoTDeviceConfig, toggle_button: ToggleButton):
        logging.info(f"Starting device #{device_config.id} ({device_config.name})")
        IoTSimulator.start_publisher(device_config.name, lambda: toggle_button.trigger_toggle(False))

    def stop_device(self, device_config: IoTDeviceConfig):
        logging.info(f"Stopping device #{device_config.id} ({device_config.name})")
        toggle_button = self.controls[f"start_device_{device_config.id}"]

        #Toggle off via virtual event
        toggle_button.trigger_toggle(False)  # type: ignore
        IoTSimulator.stop_publisher(device_config.name)
