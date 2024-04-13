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

class ClientWindow1(TKWindow):
    def __init__(self):
        super().__init__(False, window_configs.client_window_1, theme_config.ThemeConfig, theme_config.window_styles)

        logging.info("Opened Client 1")

        self.temp_msg_count = tk.IntVar(value=0)
        self.temp_prev_msg = tk.StringVar(value="")

        IoTSimulator.create_subscriber(1,[ '/sensors/temp'], self.on_mqtt_message)
        IoTSimulator.start_subscriber(1)

        self.main_section()

        self.on_window_close(self.on_window_close_handler)

    def main_section(self):
        self.demo()

    def demo(self):

        frame = Frame(self.main)
        frame.grid_columnconfigure(0, uniform="1", weight=1)
        frame.grid_columnconfigure(1, uniform="1", weight=1)
        frame.grid_rowconfigure(0)
        frame.pack(expand=True, fill=tk.BOTH)

        box1 = Frame(frame, style="LightNeutral.TFrame", padding=20)
        box1.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 10))
        Label(box1, text="Messages received:", justify="left").pack(
            pady=(spacing_y, spacing_y), side=tk.TOP, anchor=tk.NW)
        Entry(box1, textvariable=self.temp_msg_count).pack(
            pady=(spacing_y, spacing_y), side=tk.TOP, anchor=tk.NW)
        Button(box1, text="Stop subscriber", command=lambda: IoTSimulator.stop_subscriber(1)).pack(
            pady=(spacing_y, spacing_y), side=tk.TOP, anchor=tk.NW)

        box2 = Frame(frame, style="LightNeutral.TFrame", padding=20)
        # col.pack(pady=(25, spacing_y), expand=True, fill=tk.X)
        box2.grid(row=0, column=1, padx=(10, 0), sticky=tk.NSEW)
        # col.configure()
        Label(box2, text="Last message received:", justify="left").pack(
            pady=(spacing_y, spacing_y), anchor=tk.NW)

        temp_prev_msg = Label(box2, textvariable=self.temp_prev_msg, justify="left", wraplength=300)
        temp_prev_msg.pack(pady=(spacing_y, spacing_y), ipadx=5, ipady=5, expand=True, fill=tk.BOTH)


    def on_mqtt_message(self, topic, data):
        i = self.temp_msg_count.get()
        self.temp_msg_count.set(i + 1)
        self.temp_prev_msg.set(f"{data}")

    def on_window_close_handler(self):
        self.window.destroy()
        IoTSimulator.stop_subscriber(1)
        logging.info("Closed Client 1")
