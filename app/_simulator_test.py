from app.api.iot_simulator import IoTSimulator
from app.gui.main_window import MainWindow
from app.config import device_config, mqtt_config
from app.main import Main

#Configure logger
Main.configure_logger()

dev1 = device_config[0]

IoTSimulator(mqtt_config)
pub = IoTSimulator.create_publisher(dev1)
IoTSimulator.start_publisher(dev1.id)
pub.loop_forever()
