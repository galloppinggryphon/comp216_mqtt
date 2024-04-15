from __future__ import annotations
import logging
import tkinter as tk

### IMPORT ALL COMPONENTS FROM TTK IF POSSIBLE! ###
from tkinter.ttk import Frame, Button, Label
from typing import Callable, Optional
import weakref

from app.api.helpers.iot_device_config import IoTDeviceConfig
from app.api.iot_simulator import IoTSimulator
from app.config import theme_config, window_configs
from app.config import device_config
from app.gui.clients.client_window_1 import ClientWindow1
from app.gui.clients.client_window_2 import ClientWindow2
from app.gui.clients.client_window_3 import ClientWindow3
from app.gui.device_window import DeviceWindow1
from app.gui.framework.components.form_table import FormTable
from app.gui.framework.tkwindow import TKWindow
from app.gui.framework.toggle_button import ToggleButton

spacing_y = 2
spacing_x = 5


class MainWindow(TKWindow):
    controls: dict[str, tk.Widget | ToggleButton]
    windows: weakref.WeakValueDictionary[str, TKWindow]
    client_win: TKWindow
    frame: Frame

    def __init__(self):
        super().__init__(True, window_configs.main_window_config,
                         theme_config.ThemeConfig, theme_config.window_styles)

        self.resizable(False, False)

        self.windows = weakref.WeakValueDictionary()
        self.controls = {}

        self.draw_main_section()
        self.draw_footer()

    def draw_main_section(self):
        frame = Frame(self.main)
        frame.grid_columnconfigure(0, uniform=1)
        frame.grid_columnconfigure(1, uniform=1)
        frame.grid_rowconfigure(0)
        frame.pack(expand=True, fill=tk.BOTH)
        self.frame = frame

        self.draw_device_table_container()
        self.draw_device_table()
        self.draw_client_table()

    def draw_footer(self):
        bottom = self.bottom
        bottom.config(padding=20)

        Button(bottom, text="Quit", style="Warning.TButton", command=self.window.destroy).pack(
            padx=(spacing_x, spacing_x), pady=(spacing_y, spacing_y), side=tk.RIGHT)

        Button(bottom, text="About", style="Success.TButton", command=lambda: ...).pack(
            padx=(spacing_x, spacing_x), pady=(spacing_y, spacing_y), side=tk.RIGHT)

    def draw_client_table(self):
        container = Frame(self.frame)
        container.grid(row=0, column=1, sticky=tk.NSEW)
        client_table = FormTable(container, rows=2)
        self.controls["client_table"] = client_table

        Label(container, text="Clients", justify="left", style="H2.TLabel").pack(
            padx=(spacing_x, spacing_x), pady=(0, 5))

        client_table.frame.pack()

        self.add_client(1)
        self.add_client(2)
        self.add_client(3)

    def draw_device_table_container(self):
        container  = Frame(self.frame)
        container.grid(row=0, column=0, sticky=tk.NSEW)
        self.controls["device_table_container"] = container

        # Devices
        Label(container, text="Temperature Sensors", justify="left", style="H2.TLabel").pack(
            padx=(spacing_x, spacing_x), pady=(0, 5))

    def draw_device_table(self):
        container = self.controls["device_table_container"]

        device_table = FormTable(container, rows=len(device_config))
        self.controls["device_table"] = device_table
        device_table.frame.pack()

        for device in device_config:
            self.add_device(device)

    def update_device_table(self):
        self.controls["device_table"].frame.pack_forget()
        self.draw_device_table()

    def add_device(self, device_config: IoTDeviceConfig):
        device_table = self.controls["device_table"]
        with device_table.addRow() as R:
            R.col1 = Label(R(), text=device_config.title, justify="left")
            R.col2 = Frame(R())

            # TOGGLE BUTTON -->
            start_toggle = ToggleButton(R.col2, text="►", width=0)
            start_toggle.pack(padx=(spacing_x, spacing_x), side=tk.LEFT)

            # Register callback
            def toggle_on_handler(current_state, new_state, event, is_virtual):
                logging.debug(f'toggle_on_handler {
                    (current_state, new_state, event, is_virtual)}')
                if not current_state:
                    self.start_device(device_config, start_toggle)
                return True

            def toggle_off_handler(current_state, new_state, event, is_virtual):
                logging.debug(f'toggle_off_handler {
                    (current_state, new_state, event, is_virtual)}')
                return False if is_virtual else True

            start_toggle.on_toggle(
                toggle_on_callback=toggle_on_handler, toggle_off_callback=toggle_off_handler)
            self.controls[f"start_device_{device_config.id}"] = start_toggle
            # <-- TOGGLE BUTTON

            Button(R.col2, text="⬛", command=lambda: self.stop_device(device_config), width=0).pack(
                padx=(spacing_x, spacing_x), side=tk.LEFT)

            open_win = Button(R.col2, text="🔧", style="Primary.Md.TButton", command=lambda: self.open_device_window(
                device_config.id), width=0, padding=(8, 1))
            open_win.pack(
                padx=(spacing_x, spacing_x), side=tk.LEFT)  # ⚙ 🔧 ⚒  ✎
            open_win.config()

    def add_client(self, client_id: int):
        client_table = self.controls["client_table"]

        with client_table.addRow() as R:
            R.col1 = Label(R(), text=f"Client {client_id}", justify="left")
            R.col2 = Button(R(), text="Open",
                            command=lambda: self.open_client_window(client_id))

    def open_client_window(self, client_id: int):
        match client_id:
            case 1:
                self.open_window('ClientWindow1', ClientWindow1)
            case 2:
                self.open_window('ClientWindow2', ClientWindow2)
            case 3:
                self.open_window('ClientWindow3', ClientWindow3)

    def open_device_window(self, device_id: int):
        device = device_config[device_id - 1]
        IoTSimulator.stop_publisher(device.name)

        def _on_close(*args):
            self.update_device_table()

        self.open_window(
            name = 'DeviceWindow',
            Window= DeviceWindow1,
            modal = True,
            on_window_close=_on_close,
            args=[device,IoTSimulator.update_publisher_config]
        )


    def open_window(self, name: str, Window: type[TKWindow], modal=False, on_window_close: Optional[Callable] = None, args = []):
        if self.window_exists(name):
            return self.windows[name]

        win = Window(*args)
        self.windows[name] = win

        if on_window_close:
            win.on_window_close(on_window_close)

        if modal:
            win.modal()

        return win

    def window_exists(self, name: str):
        exists = name in self.windows

        if exists and self.windows[name].is_window_open():
            logging.info(f"Window '{name}' is already open.")
            return True

        return False

    def start_device(self, device_config: IoTDeviceConfig, toggle_button: ToggleButton):
        logging.info(f"Starting device #{
                     device_config.id} ({device_config.name})")
        IoTSimulator.start_publisher(
            device_config.name, lambda: toggle_button.trigger_toggle(False))

    def stop_device(self, device_config: IoTDeviceConfig):
        logging.info(f"Stopping device #{
                     device_config.id} ({device_config.name})")
        IoTSimulator.stop_publisher(device_config.name)
