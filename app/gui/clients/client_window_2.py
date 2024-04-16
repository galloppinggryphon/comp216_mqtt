import logging
from time import sleep
import tkinter as tk
from tkinter.ttk import Button, Entry, Frame, Label, Style
from typing import Callable
from app.api.helpers.iot_device_config import IoTDeviceConfig
from app.api.iot_simulator import IoTSimulator
from app.gui.framework.components.form_table import FormTable
from app.gui.framework.event_data import EventData
from app.gui.framework.tkwindow import TKWindow
from app.config import theme_config, window_configs
from tkinter import Canvas, BOTH

from app.gui.framework.utils import format_time
from app.gui.subscriber_message_handler import SubscriberMessageHandler
from app.config import device_config, mqtt_config

TC = theme_config.ThemeConfig

spacing_y = 10
spacing_x = 10
update_interval = 1

class ClientWindow2(TKWindow):
    thermometer_widgets: list[dict]

    def __init__(self):
        super().__init__(False, window_configs.client_window_2, theme_config.ThemeConfig, theme_config.window_styles)

        logging.info("Opened Client 2")

        self.canvas = Canvas()
        self.data_arr=[]
        self.thermometer_widgets = []

        # Initialize temperature variables
        self.s1_vars = {
            "temp": tk.StringVar(value="0°C"),
            "time": tk.StringVar(value="00:00")
        }
        self.s2_vars = {
            "temp": tk.StringVar(value="0°C"),
            "time": tk.StringVar(value="00:00")
        }
        self.s3_vars = {
            "temp": tk.StringVar(value="0°C"),
            "time": tk.StringVar(value="00:00")
        }

        self.sub1, self.mh1 = self.start_sub(
            sub_id = "C2_1",
            topic = '/temp/outdoor',
            interval_event = "evt_sub1_on_interval",
            on_interval = self.on_sub1_interval,
        )
        self.sub2, self.mh2 = self.start_sub(
            sub_id = "C2_2",
            topic = '/temp/living_room',
            interval_event = "evt_sub2_on_interval",
            on_interval = self.on_sub2_interval,
        )
        self.sub3, self.mh3 = self.start_sub(
            sub_id = "C2_3",
            topic = '/temp/greenhouse',
            interval_event = "evt_sub3_on_interval",
            on_interval = self.on_sub3_interval,
        )

        self.main_section()
        self.on_window_close(self.on_window_close_handler)

    def start_sub(self, sub_id, topic, interval_event, on_interval):
        # Must create a virtual event to ensure GUI updates are done from the main thread
        # Otherwise the GUI will be prone to freeze
        interval_callback = self.bind_virtual_event(interval_event, on_interval, True)

        mh = SubscriberMessageHandler(update_interval=update_interval)
        mh.add_interval_callback(interval_callback)
        sub = IoTSimulator.create_subscriber(
            sub_id, [topic])
        IoTSimulator.subscriber_add_callback(sub_id, mh.on_message())
        IoTSimulator.start_subscriber(sub_id)

        return (sub, mh)

    def main_section(self):
        # Create main frame
        frame = Frame(self.main, padding=20)
        frame.grid_columnconfigure(0, uniform="1", weight=1)
        frame.grid_columnconfigure(1, uniform="1", weight=1)
        frame.grid_columnconfigure(2, uniform="1", weight=1)
        frame.pack(expand=True, fill=tk.BOTH)

        # Create thermometer frames
        self.thermometer_frame1 = Frame(frame, style="MediumNeutral.TFrame", padding=20)
        self.thermometer_frame1.grid(column=0, row=0)
        self.thermometer_frame2 = Frame(frame, style="MediumNeutral.TFrame", padding=20)
        self.thermometer_frame2.grid(column=1, row=0, padx=(10,10))
        self.thermometer_frame3 = Frame(frame, style="MediumNeutral.TFrame", padding=20)
        self.thermometer_frame3.grid(column=2, row=0)

        self.create_thermometer_info(self.thermometer_frame1, device_config[0])
        self.create_thermometer_info(self.thermometer_frame2, device_config[1])
        self.create_thermometer_info(self.thermometer_frame3, device_config[2])

        # Create thermometer bars
        self.create_thermometer_bar(self.thermometer_frame1)
        self.create_thermometer_bar(self.thermometer_frame2)
        self.create_thermometer_bar(self.thermometer_frame3)


    def create_thermometer_info(self, frame: Frame, device: IoTDeviceConfig):
        background = TC.medium_neutral
        var_list = [self.s1_vars, self.s2_vars, self.s3_vars]
        vars = var_list[device.id - 1]

        Label(frame, style="H3.TLabel", text=f"{device.title}", justify="left", background=background).pack(pady=(0, spacing_y), anchor=tk.NW)

        row1 = Frame(frame, style="MediumNeutral.TFrame")
        row1.pack(anchor=tk.NW, side=tk.TOP, expand=True, fill=tk.X)
        Label(row1, text="Time:", justify="left", background=background).pack(pady=(0, spacing_y), padx=(0, 20), anchor=tk.NW, side=tk.LEFT)
        Label(row1, textvariable=vars["time"], justify="left", background=background).pack(pady=(0, spacing_y), anchor=tk.NW, side=tk.RIGHT)

        row2 = Frame(frame, style="MediumNeutral.TFrame")
        row2.pack(anchor=tk.NW, side=tk.TOP, expand=True, fill=tk.X, pady=(0,20))
        Label(row2, text="Current temp:", justify="left", background=background).pack(pady=(0, spacing_y), padx=(0, 20), anchor=tk.NW, side=tk.LEFT)
        Label(row2, textvariable=vars["temp"], justify="left", background=background).pack(pady=(0, spacing_y), anchor=tk.NW, side=tk.RIGHT)

    def create_thermometer_bar(self, frame):
        # Create a sub-frame to hold thermometer components
        sub_frame = Frame(frame, style="MediumNeutral.TFrame", padding=0)
        sub_frame.pack(fill=tk.BOTH, expand=True)

        canvas = Canvas(sub_frame, width=200, height=240, bd=0, bg='white', highlightthickness=0, borderwidth=0)
        canvas.pack(fill="both", expand=True, padx=0)

        # Draw thermometer bar
        canvas.create_rectangle(50, 40, 150, 240, fill="#75caeb") # Thermometer bar

        widget = {"canvas": canvas, "marker": None}
        self.thermometer_widgets.append(widget)

    def update_thermometer(self, index, value):
        widget = self.thermometer_widgets[index]

        # Remove previous
        if widget["marker"] is not None:
            widget["canvas"].delete(widget["marker"])

        # Update marker position based on value
        marker_pos = 150 - (value * 2)

        widget["marker"] = widget["canvas"].create_rectangle(50, marker_pos, 150, 240, fill="#ff851b")

        print('x')
        # widget["canvas"].coords(widget["marker"], 100, 220, 100, marker_pos)


    # event.event_data: {"data": data, "queue": [] }
    # data: { "timecode": timecode, "data": data, "topic": topic }
    # queue: list of messages received since last GUI update
    def on_sub1_interval(self, event: tk.Event):
        event_data = EventData.get(id(self), "evt_sub1_on_interval")
        data = event_data["data"]

        # Update temperature and time
        time_formatted = format_time(data['timecode'], "%H:%M")
        self.s1_vars["temp"].set(f"{data['temperature']}°C")
        self.s1_vars["time"].set(time_formatted)

        # Update thermometer bar
        self.update_thermometer(0, data['temperature'])

    def on_sub2_interval(self, event: tk.Event):
        # data = event.event_data["data"]
        event_data = EventData.get(id(self), "evt_sub2_on_interval")
        data = event_data["data"]

        # Update temperature and time
        time_formatted = format_time(data['timecode'], "%H:%M")
        self.s2_vars["temp"].set(f"{data['temperature']}°C")
        self.s2_vars["time"].set(time_formatted)

        # Update thermometer bar
        self.update_thermometer(1, data['temperature'])

    def on_sub3_interval(self, event: tk.Event):
        # data = event.event_data["data"]
        event_data = EventData.get(id(self), "evt_sub3_on_interval")
        data = event_data["data"]

        # Update temperature and time
        time_formatted = format_time(data['timecode'], "%H:%M")
        self.s3_vars["temp"].set(f"{data['temperature']}°C")
        self.s3_vars["time"].set(time_formatted)

        # Update thermometer bar
        self.update_thermometer(2, data['temperature'])


    def on_window_close_handler(self, *args):
        IoTSimulator.destroy_subscriber("C2_1")
        IoTSimulator.destroy_subscriber("C2_2")
        IoTSimulator.destroy_subscriber("C2_3")
        logging.info("Closed Client 2")
