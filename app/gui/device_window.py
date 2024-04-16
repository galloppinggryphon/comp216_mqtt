import logging
import tkinter as tk
from tkinter.ttk import Button, Entry, Frame, Label
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

    def __init__(self, device_config: IoTDeviceConfig, save_config_handler):
        super().__init__(False, window_configs.device_window_1, theme_config.ThemeConfig, theme_config.window_styles)
        logging.info(f"Opened Device {device_config.id}")

        self.device_config = device_config
        self.header.config(text=f"Configure {device_config.name}")

        self.save_config_handler = save_config_handler
        self.original_config = {
            "title": self.device_config.title,
            "frequency": self.device_config.frequency,
            "value_range": self.device_config.data_config['value_range']
        }

        self.var_preview = tk.StringVar(value="")

        self.draw_main_section()
        self.draw_footer()

        self.on_window_close(self.on_window_close_handler)
        self.on_reset()

    def draw_main_section(self):
        frame = Frame(self.main, padding=10)
        self.main_frame = frame
        frame.grid_columnconfigure(0, uniform="1", weight=1)
        frame.grid_columnconfigure(1, uniform="1", weight=1)
        frame.grid_rowconfigure(0)
        frame.pack(expand=True, fill=tk.BOTH)

        self.config_box()
        self.preview_box()

    def draw_footer(self):
        bottom = self.bottom
        bottom.config(padding=20)

        Button(bottom, text="Save Changes", style="Success.TButton", command=self.on_save).pack(
            padx=(spacing_x, spacing_x), pady=(spacing_y, spacing_y), side=tk.LEFT)

        Button(bottom, text="Close", command=self.close).pack(
            padx=(spacing_x, spacing_x), pady=(spacing_y, spacing_y), side=tk.LEFT)

        Button(bottom, text="Reset", style="Warning.TButton", command=self.on_reset).pack(
            padx=(spacing_x, spacing_x), pady=(spacing_y, spacing_y), side=tk.RIGHT)

    def config_box(self):
        frame = self.main_frame
        form = FormTable(frame, 8) # {"style": "LightNeutral.TFrame"}
        form.frame.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 10))

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
            R.col1 = Label(R(), text="Title")
            R.col2 = Entry(R())
            self.title_entry = Entry(R.col2)
            self.title_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        with form.addRow() as R:
            R.col1 = Label(R(), text="Frequency")
            R.col2 = Entry(R())
            self.frequency_entry = Entry(R.col2)
            self.frequency_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        with form.addRow() as R:
            R.col1 = Label(R(), text="Value range (min-max)")
            R.col2 = Frame(R())
            self.vmin = Entry(R.col2, width=10)
            self.vmin.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            Label(R.col2, text=" - ").pack(side=tk.LEFT)
            self.vmax = Entry(R.col2)
            self.vmax.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    def preview_box(self):
        frame = self.main_frame

        box = Frame(frame, style="MediumNeutral.TFrame", padding=20)
        box.grid(row=0, column=1, padx=(10, 0), sticky=tk.NSEW)

        Label(box, text="Output Preview", style="H3.TLabel", justify="left").pack(
            pady=(spacing_y, spacing_y), anchor=tk.NW)

        output = Label(box, textvariable=self.var_preview, justify="left",  wraplength=300, padding=5, background="white", anchor=tk.NW)
        output.pack(pady=(spacing_y, spacing_y), expand=True, fill=tk.BOTH, side=tk.TOP)

        preview_btn = Button(box, text="Generate output", command=self.generate_output)
        preview_btn.pack(
            pady=(spacing_y, spacing_y), side=tk.LEFT)

    def generate_output(self):
        payload = IoTSimulator.publisher_get_payload_preview(self.device_config.name)
        self.var_preview.set(payload)

    def on_save(self):
        try:
            title = self.title_entry.get()
            frequency = float(self.frequency_entry.get())
            min_val = float(self.vmin.get())
            max_val = float(self.vmax.get())
            if min_val >= max_val:
                raise ValueError("Minimum value must be less than maximum value.")

            new_config = {
                "title": title,
                "frequency": frequency,
                "value_range": (min_val, max_val)
            }
            self.save_config_handler(self.device_config.id, new_config)
        except ValueError as e:
            logging.error(f"Error saving configuration: {e}")

    def on_reset(self):
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, self.original_config['title'])

        self.frequency_entry.delete(0, tk.END)
        self.frequency_entry.insert(0, self.original_config['frequency'])

        self.vmin.delete(0, tk.END)
        self.vmin.insert(0, self.original_config['value_range'][0])

        self.vmax.delete(0, tk.END)
        self.vmax.insert(0, self.original_config['value_range'][1])

    def on_window_close_handler(self, window):

        logging.info(f"Closed Device {self.device_config.id}")
