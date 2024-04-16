import logging
import tkinter as tk
from tkinter.ttk import Button, Entry, Frame, Label, Style
from typing import Callable
from app.api.iot_simulator import IoTSimulator
from app.gui.framework.components.form_table import FormTable
from app.gui.framework.event_data import EventData
from app.gui.framework.tkwindow import TKWindow
from app.config import theme_config, window_configs, device_config

from app.gui.subscriber_message_handler import SubscriberMessageHandler

spacing_y = 10
spacing_x = 10

class ClientWindow3(TKWindow):
    def __init__(self):
        super().__init__(False, window_configs.client_window_3, theme_config.ThemeConfig, theme_config.window_styles)

        logging.info("Opened Client 3")

        self.var_msg_count = tk.IntVar(value=0)
        self.var_upd_count = tk.IntVar(value=0)
        self.var_last_upd_id = tk.IntVar(value=0)
        self.var_prev_msg = tk.StringVar(value="")

        # Must create a virtual event to ensure GUI updates are done from the main thread
        # Otherwise the GUI will be prone to freeze
        evt_sub1_on_message = self.bind_virtual_event("evt_sub1_on_message", self.on_sub1_message, True)
        evt_sub1_on_interval = self.bind_virtual_event("evt_sub1_on_interval", self.on_sub1_interval, True)

        self.sub1_mh = SubscriberMessageHandler(update_interval=1)
        self.sub1_mh.add_interval_callback(evt_sub1_on_interval)
        self.sub1_mh.add_message_received_callback(evt_sub1_on_message)
        self.sub1 = IoTSimulator.create_subscriber(
            "C3_1", ['/temp/outdoor'])
        IoTSimulator.subscriber_add_callback("C3_1", self.sub1_mh.on_message())
        IoTSimulator.start_subscriber("C3_1")

        self.main_section()
        self.on_window_close(self.on_window_close_handler)

    def main_section(self):
        frame = Frame(self.main)
        frame.grid_columnconfigure(0, uniform="1", weight=1)
        frame.grid_columnconfigure(1, uniform="1", weight=1)
        frame.grid_rowconfigure(0)
        frame.pack(expand=True, fill=tk.BOTH)

        # COLUMN 1
        box1 = Frame(frame, padding=0)
        box1.grid(row=0, column=0, sticky=tk.NSEW, padx=(10, 10))

        form = FormTable(box1, rows=8, settings={"padding": 0})
        form.frame.pack(anchor=tk.NW, side=tk.TOP)

        sub = IoTSimulator.get_subscriber("C3_1")

        with form.addRow() as R:
            R.col1 = Label(R(), text="Subscriber ID:")
            R.col2 = Label(R(), text=self.sub1.id)

        with form.addRow() as R:
            R.col1 = Label(R(), text="Topics:")
            R.col2 = Label(R(), text=str.join(", ", sub.topics))

        with form.addRow() as R:
            R.col1 = Label(R(), text="Messages received:")
            R.col2 = Entry(R(), textvariable=self.var_msg_count)

        with form.addRow() as R:
            R.col1 = Label(R(), text="Update count:")
            R.col2 = Entry(R(), textvariable=self.var_upd_count)

        with form.addRow() as R:
            R.col1 = Label(R(), text="Last update #:")
            R.col2 = Entry(R(), textvariable=self.var_last_upd_id)

        Button(box1, text="Stop subscriber", command=lambda: IoTSimulator.stop_subscriber("C3_1") and None).pack(anchor=tk.NW, pady=(20, 0))

        # COLUMN 2
        box2 = Frame(frame, style="MediumNeutral.TFrame", padding=20)
        box2.grid(row=0, column=1, padx=(10, 10), sticky=tk.NSEW)
        Label(box2, text="Last message received:", justify="left").pack(
            pady=(spacing_y, spacing_y), anchor=tk.NW)

        # prev_msg = Label(box2, textvariable=self.var_prev_msg, justify="left", wraplength=300)
        # prev_msg.pack(pady=(spacing_y, spacing_y), ipadx=5, ipady=5, expand=True, fill=tk.BOTH)

        prev_msg = Label(box2, textvariable=self.var_prev_msg, justify="left",  wraplength=300, padding=5, background="white", anchor=tk.NW)
        prev_msg.pack(pady=(spacing_y, spacing_y), expand=True, fill=tk.BOTH, side=tk.TOP)


    # event.event_data: { "timecode": timecode, "data": data, "topic": topic }
    def on_sub1_message(self, event: tk.Event):
        # event_data = event.event_data
        i = self.var_msg_count.get()
        self.var_msg_count.set(i + 1)

    # EventData {"data": data, "queue": [], "last_message_id": int }
    # data: { "timecode": timecode, "data": data, "topic": topic }
    # queue: list of messages received since last GUI update
    def on_sub1_interval(self, event: tk.Event): # data, message_queue):
        event_data = EventData.get(id(self), "evt_sub1_on_interval")
        data = event_data["data"]

        i = self.var_upd_count.get()
        self.var_upd_count.set(i + 1)
        self.var_last_upd_id.set(data['id'])
        self.var_prev_msg.set(f"{data}")

    @staticmethod
    def on_window_close_handler(self):
        IoTSimulator.destroy_subscriber("C3_1")
        logging.info("Closed Client 3")
