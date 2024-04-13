import logging
import threading
from time import sleep
from app.api.helpers.iot_device_config import IoTDeviceConfig
from app.api.iot_simulator import IoTSimulator
from app.gui.main_window import MainWindow
from app.config import device_config, mqtt_config
from app.config.device_data import device_data_1
from app.main import Main


#Configure logger
Main.configure_logger()

# dev1 = device_config[0]
dev1 = IoTDeviceConfig(
    id=1,
    name="temp_sensor",
    title="Temperature",
    type="temperature",
    topic="/temp/living_room",
    frequency=2, #Delay between updates, in seconds
    failure_frequency=0, #Every nth transmission
    payload_generator=device_data_1.generate_payload_data
)

IoTSimulator(mqtt_config)

def publisher_test():
    pub = IoTSimulator.create_publisher(dev1)
    IoTSimulator.start_publisher(dev1.name, lambda: print('complete'))
    sleep(10)

def subscriber_test():
    def on_message(topic, payload):
        # logging.info(f"\ntopic: {topic}\n{payload}\n")
        ...

    IoTSimulator.create_subscriber(1, ['/temp/living_room'], on_message)
    IoTSimulator.start_subscriber(1)

    # IoTSimulator.subscriber_wait()
    # sleep(2)

    # IoTSimulator.stop_subscriber(1)

    # IoTSimulator.check_status()


    # for t in threading.enumerate():
    #     print(t.name)



subscriber_test()
publisher_test()
