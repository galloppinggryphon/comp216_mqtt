import logging
from time import sleep
import tkinter as tk
from tkinter.ttk import Button, Entry, Frame, Label, Style
from typing import Callable
from app.api.iot_simulator import IoTSimulator
from app.gui.framework.tkwindow import TKWindow
from app.config import theme_config, window_configs, device_config
from tkinter import Canvas, BOTH

spacing_y = 10
spacing_x = 10

class ClientWindow3(TKWindow):
    def __init__(self):
        super().__init__(False, window_configs.client_window_3, theme_config.ThemeConfig, theme_config.window_styles)

        logging.info("Opened Client 1")

        self.temp_msg_count = tk.IntVar(value=0)
        self.temp_prev_msg = tk.StringVar(value="")
        self.canvas = Canvas()
        self.data_arr=[]

        IoTSimulator.create_subscriber(1,[ '/temp/outdoor'], self.on_sub1_message)
        IoTSimulator.start_subscriber(1)

        IoTSimulator.create_subscriber(2,[ '/temp/living_room'], self.on_sub2_message)
        IoTSimulator.start_subscriber(2)
        IoTSimulator.create_subscriber(3,[ '/temp/greenhouse'], self.on_sub3_message)
        IoTSimulator.start_subscriber(3)

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
        
        # box_line = Frame(frame, style="LightNeutral.TFrame", padding=20)
        # box_line.grid(row=1, column=0, columnspan = 2, pady=15, sticky=tk.NSEW)

        
        # label_line = Label(box_line, text=f"Line Chart: {device_config[0].name}", justify="left")
        # label_line.pack(pady=(spacing_y, spacing_y), anchor=tk.NW)
        
        # self.canvas = Canvas(box_line, width=200, height=240, bg='white')
        # self.canvas.pack(fill="both", expand=True)

        temp_prev_msg = Label(box2, textvariable=self.temp_prev_msg, justify="left", wraplength=300)
        temp_prev_msg.pack(pady=(spacing_y, spacing_y), ipadx=5, ipady=5, expand=True, fill=tk.BOTH)

    def on_sub1_message(self, topic, data):
        i = self.temp_msg_count.get()
        self.temp_msg_count.set(i + 1)
        self.temp_prev_msg.set(f"{data}")
        self.create_line(data)

    def on_sub2_message(self, topic, data):
        i = self.temp_msg_count.get()
        self.temp_msg_count.set(i + 1)
        self.temp_prev_msg.set(f"{data}")

    def on_sub3_message(self, topic, data):
        i = self.temp_msg_count.get()
        self.temp_msg_count.set(i + 1)
        self.temp_prev_msg.set(f"{data}")

    def on_window_close_handler(self):
        self.window.destroy()
        IoTSimulator.stop_subscriber(1)
        logging.info("Closed Client 1")
    

