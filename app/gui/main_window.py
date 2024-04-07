from tkinter.ttk import Frame, Button, Label
from app.api.data_generator import DataGenerator
from app.api.mqtt_controller import MQTTController
from app.config import theme_config, main_window_config, window_configs
from app.gui.clients.client_window_1 import ClientWindow1
from app.gui.framework.tkwindow import TKWindow
# from app.gui.framework.window_config import WindowConfig


class MainWindow(TKWindow):
    def __init__(self):
        super().__init__(True, main_window_config, theme_config.ThemeConfig, theme_config.window_style)

        self.main_section()


    def main_section(self):
        main = self.main
        wrapper = Frame(main)
        # wrapper.grid(row=0, column=2)
        client_box = Frame(wrapper)
        sensor_box = Frame(wrapper)

        wrapper.pack()
        sensor_box.pack(pady=(10, 10))
        client_box.pack()

        padding = 2

        Label(sensor_box, text="Sensors",justify="left").pack(padx=(padding, padding), pady=(padding, padding))
        Button(sensor_box, text="Start Sensor 1", command=self.start_sensor_1).pack(padx=(padding, padding), pady=(padding, padding))

        Label(client_box, text="Clients",justify="left").pack(padx=(padding, padding), pady=(padding, padding))
        Button(client_box, text="Open Client 1", command=self.open_client_1).pack(padx=(padding, padding), pady=(padding, padding))
        Button(client_box, text="Open Client 2", command=self.open_client_1).pack(padx=(padding, padding), pady=(padding, padding))

    def open_client_1(self):
        ClientWindow1()

    def start_sensor_1(self):

        #TODO: this has to be threaded so it doesn't hang or jank when started
        #TODO: feedback on screen if connection fails
        MQTTController.start_publisher('sensor_1')
