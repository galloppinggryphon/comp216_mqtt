import sys
import logging

from app.api.iot_simulator import IoTSimulator
from app.gui.main_window import MainWindow
from app.config import device_config, mqtt_config

class Main:
    def __init__(self):
        self.configure_logger()
        logging.info('Starting app')

        self.start_simulator()

        app = MainWindow()
        app.mainloop()

    def start_simulator(self):
        logging.info('Starting simulator')
        IoTSimulator(mqtt_config)

        for device in device_config:
            IoTSimulator.create_publisher(device)

    @staticmethod
    def configure_logger():
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt="[%H:%M:%S]")

        # Continuous output to screen
        log_handler = logging.StreamHandler(sys.stdout)
        log_handler.setFormatter(formatter)
        logging.getLogger().addHandler(log_handler)
        logging.getLogger().setLevel(logging.DEBUG)


if __name__ == '__main__':
    Main()
