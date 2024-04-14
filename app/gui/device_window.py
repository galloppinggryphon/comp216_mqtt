from dataclasses import dataclass
import logging
import tkinter as tk
from tkinter.ttk import Button, Entry, Frame, Label, Style
from app.api.helpers.iot_device_config import IoTDeviceConfig
from app.api.iot_simulator import IoTSimulator
from app.gui.framework.components.form_table import FormTable
from app.gui.framework.tkwindow import TKWindow
from app.config import theme_config, window_configs

spacing_y = 10
spacing_x = 10

class DeviceWindow1(TKWindow):
    frame: Frame
    device_config: IoTDeviceConfig

    def __init__(self, device_config: IoTDeviceConfig):
        super().__init__(False, window_configs.device_window_1, theme_config.ThemeConfig, theme_config.window_styles)
        logging.info(f"Opened Device {device_config.id}")

        self.device_config = device_config
        self.temp_msg_count = tk.IntVar(value=0)
        self.temp_prev_msg = tk.StringVar(value="")

        # IoTSimulator.create_subscriber(1,[ '/temp/outdoor'], self.on_sub1_message)
        # IoTSimulator.start_subscriber(1)

        self.main_section()
        self.footer()

        self.on_window_close(self.on_window_close_handler)

    def main_section(self):
        frame = Frame(self.main)
        self.main_frame = frame
        frame.grid_columnconfigure(0, uniform="1", weight=1)
        frame.grid_columnconfigure(1, uniform="1", weight=1)
        frame.grid_rowconfigure(0)
        frame.pack(expand=True, fill=tk.BOTH)

        self.config_box()
        self.preview_box()


    def footer(self):
        bottom = self.bottom
        bottom.config(padding=20)

        Button(bottom, text="Save Changes", style="Success.TButton", command=lambda: ...).pack(
            padx=(spacing_x, spacing_x), pady=(spacing_y, spacing_y), side=tk.LEFT)

        Button(bottom, text="Close", command=self.window.destroy).pack(
            padx=(spacing_x, spacing_x), pady=(spacing_y, spacing_y), side=tk.LEFT)

        Button(bottom, text="Reset", style="Warning.TButton", command=lambda: ...).pack(
            padx=(spacing_x, spacing_x), pady=(spacing_y, spacing_y), side=tk.RIGHT)




    def config_box(self):
        frame = self.main_frame
        form = FormTable(frame, 8) # {"style": "LightNeutral.TFrame"}
        form.table.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 10))

        with form.addRow() as R:
            R.col1 = Label(R(), text="ID")
            R.col2 = Label(R(), text=self.device_config.id)

        with form.addRow() as R:
            R.col1 = Label(R(), text="Name")
            R.col2 = Label(R(), text=self.device_config.name)

        with form.addRow() as R:
            R.col1 = Label(R(), text="Device type")
            R.col2 = Label(R(), text=self.device_config.type)

        with form.addRow() as R:
            R.col1 = Label(R(), text="Topic")
            R.col2 = Label(R(), text=self.device_config.topic)

        with form.addRow() as R:
            t = tk.StringVar()
            R.col1 = Label(R(), text="Title")
            R.col2 = Entry(R(), textvariable=self.device_config.title)

        with form.addRow() as R:
            t = tk.StringVar()
            R.col1 = Label(R(), text="Frequency")
            R.col2 = Entry(R(), textvariable=t)




    def preview_box(self):
        frame = self.main_frame

        box = Frame(frame, style="LightNeutral.TFrame", padding=20)
        box.grid(row=0, column=1, padx=(10, 0), sticky=tk.NSEW)
        Label(box, text="Output Preview", style="H3.TLabel", justify="left").pack(
            pady=(spacing_y, spacing_y), anchor=tk.NW)

        temp_prev_msg = Label(box, textvariable=self.temp_prev_msg, justify="left", wraplength=300)
        temp_prev_msg.pack(pady=(spacing_y, spacing_y), ipadx=5, ipady=5, expand=True, fill=tk.BOTH)


    sub1_counter = 0
    sub1_update_counter = 0
    prev_time = 'time'

    def on_sub1_message(self, topic, data):
        # x transmissions / minute
        # Chart: 10 minute interval on the x-axis
        # data = {
        #     "id": 1006,
        #     "location": "outdoor",
        #     "timestamp": "",
        #     "temperature": 24.1
        # }

        timestamp = datetime.fromtimestamp( data["timecode"] )
        datetime_str = timestamp.strftime( "%Y-%m-%d  %H:%M:%S")

        i = self.temp_msg_count.get()
        self.temp_msg_count.set(i + 1)
        self.temp_prev_msg.set(f"{data}")

    def on_sub2_message(self, topic, data):
        i = self.temp_msg_count.get()
        self.temp_msg_count.set(i + 1)
        self.temp_prev_msg.set(f"{data}")

    def on_window_close_handler(self):
        self.window.destroy()
        IoTSimulator.stop_subscriber(1)
        logging.info(f"Closed Device {self.device_config.id}")
