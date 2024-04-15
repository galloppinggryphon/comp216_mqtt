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

class ClientWindow1(TKWindow):
    def __init__(self):
        super().__init__(False, window_configs.client_window_1, theme_config.ThemeConfig, theme_config.window_styles)

        logging.info("Opened Client 1")

        # self.temp_msg_count = tk.IntVar(value=0)
        self.canvas1 = Canvas()
        self.items1 = []
        self.data_arr1=[]

        self.canvas2 = Canvas()
        self.items2 = []
        self.data_arr2=[]

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

        box_line1 = Frame(frame, style="LightNeutral.TFrame", padding=20)
        box_line1.grid(row=0, column=0, columnspan = 2, pady=15, sticky=tk.NSEW)
        
        label_line1 = Label(box_line1, text=f"Line Chart: {device_config[0].name}", justify="left")
        label_line1.pack(pady=(spacing_y, spacing_y), anchor=tk.NW)
        
        self.canvas1 = Canvas(box_line1, width=200, height=240, bg='white')
        self.canvas1.pack(fill="both", expand=True)

        box_line2 = Frame(frame, style="LightNeutral.TFrame", padding=20)
        box_line2.grid(row=1, column=0, columnspan = 2, pady=15, sticky=tk.NSEW)
        
        label_line2 = Label(box_line2, text=f"Line Chart: {device_config[1].name}", justify="left")
        label_line2.pack(pady=(spacing_y, spacing_y), anchor=tk.NW)
        
        self.canvas2 = Canvas(box_line2, width=200, height=240, bg='white')
        self.canvas2.pack(fill="both", expand=True)

    def on_sub1_message(self, topic, data):
        # i = self.temp_msg_count.get()
        # self.temp_msg_count.set(i + 1)
        self.create_line1(topic, data)

    def on_sub2_message(self, topic, data):
        # i = self.temp_msg_count.get()
        # self.temp_msg_count.set(i + 1)
        self.create_line1(topic, data)

    def on_window_close_handler(self):
        self.window.destroy()
        IoTSimulator.stop_subscriber(1)
        logging.info("Closed Client 1")
    
    def create_line1(self,topic,data):
        topicID = 0
        y_value = 0
        canvas=Canvas()
        arr=[]
        items=[]
        if topic=='/temp/outdoor':
            topicID=0
            y_value=180
            canvas=self.canvas1
            arr=self.data_arr1
            items=self.items1
        if topic =='/temp/living_room':
            topicID=1
            y_value=220
            canvas=self.canvas2
            arr=self.data_arr2
            items=self.items2
        
        startX = 20
        startY = 220
        x_line_gap = 20
        y_scale = 8

        data_info= device_config[topicID]
        min = data_info.data_config['value_range'][0]
        max = data_info.data_config['value_range'][1]

        length = len(arr)
        
        if length>30:
            arr.pop(0)
 
        arr.append(data["temperature"])
        canvas.delete('all')

        canvas.create_line(20,20,20,220,width=2, fill='black')
        canvas.create_line(20,y_value,700,y_value,width=2, fill='black')

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
