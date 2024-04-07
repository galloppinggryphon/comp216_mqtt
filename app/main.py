from app.api.data_generator import DataGenerator
from app.api.mqtt_controller import MQTTController
from app.gui.clients.client_window_1 import ClientWindow1
from app.gui.main_window import MainWindow
from app.config import mqtt_config

class Main:
    def __init__(self):
        MQTTController(mqtt_config)
        app = MainWindow()
        # app = ClientWindow1()
        app.mainloop()


if __name__ == '__main__':
    Main()
