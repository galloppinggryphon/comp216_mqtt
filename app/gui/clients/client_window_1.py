import logging
from time import sleep
import tkinter as tk
from tkinter.ttk import Button, Entry, Frame, Label, Style
from typing import Callable
from app.api.iot_simulator import IoTSimulator
from app.gui.framework.tkwindow import TKWindow
from app.config import theme_config, window_configs, device_config
from tkinter import Canvas, BOTH
from app.gui.subscriber_message_handler import SubscriberMessageHandler

spacing_y = 10
spacing_x = 10
update_interval = 1

class ClientWindow1(TKWindow):
    def __init__(self):
        super().__init__(False, window_configs.client_window_1, theme_config.ThemeConfig, theme_config.window_styles)

        logging.info("Opened Client 1")

        self.canvas1 = Canvas()
        self.items1 = []
        self.data_arr1=[]

        self.canvas2 = Canvas()
        self.items2 = []
        self.data_arr2=[]

        # Must create a virtual event to ensure GUI updates are done from the main thread
        # Otherwise the GUI will be prone to freeze
        # evt_sub1_on_message = self.bind_virtual_event("evt_sub1_on_message", self.on_sub1_interval, True)
        evt_sub1_on_interval = self.bind_virtual_event("evt_sub1_on_interval", self.on_sub1_interval, True)
        evt_sub2_on_interval = self.bind_virtual_event("evt_sub2_on_interval", self.on_sub2_interval, True)

        self.sub1_mh = SubscriberMessageHandler(update_interval=update_interval)
        self.sub1_mh.add_interval_callback(evt_sub1_on_interval)
        # self.sub1_mh.add_message_received_callback(evt_sub1_on_message)
        self.sub1 = IoTSimulator.create_subscriber(
            "C1_1", ['/temp/outdoor'])
        IoTSimulator.subscriber_add_callback("C1_1", self.sub1_mh.on_message())
        IoTSimulator.start_subscriber("C1_1")

        self.sub2_mh = SubscriberMessageHandler(update_interval=update_interval)
        self.sub2_mh.add_interval_callback(evt_sub2_on_interval)
        self.sub2 = IoTSimulator.create_subscriber(
            "C1_2", ['/temp/living_room'])
        IoTSimulator.subscriber_add_callback("C1_2", self.sub2_mh.on_message())
        IoTSimulator.start_subscriber("C1_2")

        self.main_section()
        self.on_window_close(self.on_window_close_handler)


    def main_section(self):
        frame = Frame(self.main)
        frame.grid_columnconfigure(0, uniform="1", weight=1)
        frame.grid_columnconfigure(1, uniform="1", weight=1)
        frame.grid_rowconfigure(0)
        frame.pack(expand=True, fill=tk.BOTH)

        box_line1 = Frame(frame, padding=20)
        box_line1.grid(row=0, column=0, columnspan = 2, pady=15, sticky=tk.NSEW)

        label_line1 = Label(box_line1, style="H2.TLabel", text=f"{device_config[0].name}", justify="left")
        label_line1.pack(pady=(spacing_y, spacing_y), anchor=tk.NW)

        self.canvas1 = Canvas(box_line1, width=200, height=240, bg='white')
        self.canvas1.pack(fill="both", expand=True)

        box_line2 = Frame(frame, padding=20)
        box_line2.grid(row=1, column=0, columnspan = 2, pady=15, sticky=tk.NSEW)

        label_line2 = Label(box_line2, style="H2.TLabel", text=f"{device_config[1].name}", justify="left")
        label_line2.pack(pady=(spacing_y, spacing_y), anchor=tk.NW)

        self.canvas2 = Canvas(box_line2, width=200, height=240, bg='white')
        self.canvas2.pack(fill="both", expand=True)

    # event.event_data: { "timecode": timecode, "data": data, "topic": topic }
    def on_sub1_interval(self, event: tk.Event):
        data = event.event_data["data"]
        queue = event.event_data["queue"]

        #TODO: DATA FROM THE MESSAGE QUEUE MUST ALSO BE USED WHEN UPDATING THE CHART
        #NOTE: THE QUEUE DOES _NOT_ INCLUDE THE LAST MESSAGE
        #i.e. use data from [data, queue]
        print('\n\nMESSAGE QUEUE:', queue, '\n\n')

        self.create_line1(data)

    # event.event_data: {"data": data, "queue": [] }
    # data: { "timecode": timecode, "data": data, "topic": topic }
    # queue: list of messages received since last GUI update
    def on_sub2_interval(self, event: tk.Event):
        data = event.event_data["data"]


        self.create_line2(data)

    def on_window_close_handler(self, *args):
        IoTSimulator.destroy_subscriber("C1_1")
        IoTSimulator.destroy_subscriber("C1_2")
        logging.info("Closed Client 1")

    def create_line1(self,data):
        y_value=180

        canvas=self.canvas1
        arr=self.data_arr1
        items=self.items1

        startX = 20
        startY = 220
        x_line_gap = 20
        y_scale = 8

        data_info= device_config[0]
        min = data_info.data_config['value_range'][0]
        max = data_info.data_config['value_range'][1]

        length = len(arr)

        if length>30:
            arr.pop(0)

        arr.append(data["temperature"])
        canvas.delete('all')

        #x-axis,y-axis
        canvas.create_line(20,20,20,220,width=2, fill='black')
        canvas.create_line(20,y_value,700,y_value,width=2, fill='black')

        #minimum value & maximum value for y-axis
        canvas.create_text(10,220,text=f'{min}')
        canvas.create_text(10,20,text=f'{max}')

        for i in range(31):
            canvas.create_text(startX + i * x_line_gap,230,text=f"{i}")

        # Draw dynamic data lines
        for i in range(length-1):
            #start point
            x_line_start = startX + i * x_line_gap
            y_line_start = startY - (arr[i]-min)*y_scale
            #end point
            x_line_end = startX + (i+1) * x_line_gap
            y_line_end = startY - (arr[i+1]-min)*y_scale

            items.append(canvas.create_line(x_line_start, y_line_start, x_line_end, y_line_end, width=2, fill='red'))


    def create_line2(self,data):
        y_value=220
        canvas=self.canvas2
        arr=self.data_arr2
        items=self.items2

        startX = 20
        startY = 220
        x_line_gap = 20
        y_scale = 8

        data_info= device_config[1]
        min = data_info.data_config['value_range'][0]
        max = data_info.data_config['value_range'][1]

        length = len(arr)

        if length>30:
            arr.pop(0)

        arr.append(data["temperature"])
        canvas.delete('all')

        #x-axis,y-axis
        canvas.create_line(20,20,20,220,width=2, fill='black')
        canvas.create_line(20,y_value,700,y_value,width=2, fill='black')

        #minimum value & maximum value for y-axis
        canvas.create_text(10,220,text=f'{min}')
        canvas.create_text(10,20,text=f'{max}')

        for i in range(31):
            canvas.create_text(startX + i * x_line_gap,230,text=f"{i}")

        # Draw dynamic data lines
        for i in range(length-1):
            #start point
            x_line_start = startX + i * x_line_gap
            y_line_start = startY - (arr[i]-min)*y_scale
            #end point
            x_line_end = startX + (i+1) * x_line_gap
            y_line_end = startY - (arr[i+1]-min)*y_scale

            items.append(canvas.create_line(x_line_start, y_line_start, x_line_end, y_line_end, width=2, fill='red'))
