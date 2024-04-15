import logging
from time import sleep
import tkinter as tk
from tkinter.ttk import Button, Entry, Frame, Label, Style
from typing import Callable
from app.api.iot_simulator import IoTSimulator
from app.gui.framework.tkwindow import TKWindow
from app.config import theme_config, window_configs
from tkinter import Canvas, BOTH

spacing_y = 10
spacing_x = 10

class ClientWindow2(TKWindow):
    def __init__(self):
        super().__init__(False, window_configs.client_window_2, theme_config.ThemeConfig, theme_config.window_styles)

        logging.info("Opened Client 2")

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

    def create_thermometer_bar(self, frame, title):
        # Create a sub-frame to hold thermometer components
        sub_frame = Frame(frame, style="LightNeutral.TFrame")
        sub_frame.pack(fill=tk.BOTH, expand=True)

        # Add title for the frame
        Label(sub_frame, text=title, justify="left").pack(pady=(10, 5), anchor=tk.W)

        # Create thermometer bar
        canvas = Canvas(sub_frame, width=200, height=240, bg='white')
        canvas.pack(fill="both", expand=True)

        # Draw "Current Temperature" text on the canvas
        canvas.create_text(100, 20, text="Current Temperature:", anchor=tk.N)

        # Draw thermometer bar
        canvas.create_rectangle(25, 40, 100, 240, fill="light blue")  # Thermometer bar
        marker = canvas.create_line(100, 240, 100, 240, fill="red", width=2)  # Marker
        
    def demo(self):
        # Create main frame
        frame = Frame(self.main)
        frame.pack(expand=True, fill=tk.BOTH)

        # Create title frame
        title_frame = Frame(frame, style="LightNeutral.TFrame", padding=20)
        title_frame.pack(fill=tk.X)
        Label(title_frame, text="Temperature Sensor Thermometer", justify="left").pack(pady=(10, 0), anchor=tk.W)

        # Create thermometer frames
        thermometer_frame1 = Frame(frame, style="LightNeutral.TFrame", padding=20)
        thermometer_frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        thermometer_frame2 = Frame(frame, style="LightNeutral.TFrame", padding=20)
        thermometer_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        thermometer_frame3 = Frame(frame, style="LightNeutral.TFrame", padding=20)
        thermometer_frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create thermometer bars
        self.create_thermometer_bar(thermometer_frame1, "Outdoor Temperature")
        self.create_thermometer_bar(thermometer_frame2, "LivingRoom Temperature")
        self.create_thermometer_bar(thermometer_frame3, "GreenHouse Temperature")

        # Initialize temperature variables
        self.temp_msg_count = tk.IntVar()
        self.temp_prev_msg = tk.StringVar()

    def on_sub1_message(self, topic, data):
    # Update temperature value
        self.temp_msg_count.set(self.temp_msg_count.get() + 1)
        self.temp_prev_msg.set(f"{data}")

        # Update thermometer bar
        self.update_thermometer(self.thermometer_frame1, data)
        self.update_thermometer(self.thermometer_frame2, data)
        self.update_thermometer(self.thermometer_frame3, data)
        # i = self.temp_msg_count.get()
        # self.temp_msg_count.set(i + 1)
        # self.temp_prev_msg.set(f"{data}")
        # length = len(self.data_arr)
        # if length>30:
        #     self.data_arr.pop(0)
 
        # self.data_arr.append(data["temperature"])
        # self.canvas.delete('all')

    def update_thermometer(self, frame, value):
        # Update marker position based on value
        marker_pos = 220 - (value * 2)
        self.canvas = frame.winfo_children()[1]  # Get the canvas
        self.canvas.coords(self.marker, 100, 220, 100, marker_pos)    


    def on_sub2_message(self, topic, data):
        i = self.temp_msg_count.get()
        self.temp_msg_count.set(i + 1)
        self.temp_prev_msg.set(f"{data}")

    def on_window_close_handler(self):
        self.window.destroy()
        IoTSimulator.stop_subscriber(1)
        logging.info("Closed Client 2")
