import sys
import threading
import logging

from app.api.iot_simulator import IoTSimulator
from app.gui.main_window import MainWindow
from app.config import device_config, mqtt_config


class Main:
    def __init__(self):
        self.configure_logger()
        logging.info('Starting app')
        self.start_simulator_thread()

        app = MainWindow()
        app.mainloop()

    @staticmethod
    def configure_logger():
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt="[%H:%M:%S]")

        # Continuous output to screen
        log_handler = logging.StreamHandler(sys.stdout)
        log_handler.setFormatter(formatter)
        logging.getLogger().addHandler(log_handler)
        logging.getLogger().setLevel(logging.DEBUG)


    #TODO: Not sure if the whole simulator should be threaded or just MQTT clients when they're started
    def start_simulator_thread(self):
        logging.info('Starting simulator thread')
        sim_thread = threading.Thread(target=self.start_simulator, daemon=True) # Background thread
        sim_thread.start()

    def start_simulator(self):
        logging.debug('Hello from the simulator thread')

        IoTSimulator(mqtt_config)
        IoTSimulator.create_publisher(device_config[0])
        IoTSimulator.start_publisher(device_config[0].id)



if __name__ == '__main__':
    Main()
