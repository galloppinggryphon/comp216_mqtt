from app.api.helpers.iot_device_config import IoTDeviceConfig
from app.config.device_data import device_data_1
# from app.config.device_data import device_data_2
# from app.config.device_data import device_data_3
# from app.config.device_data import device_data_4
# from app.config.device_data import device_data_5

connection_settings = {
    "host": "localhost",
    "port": 1883,
    # "keepalive": 60
}

IoTDevice1 = IoTDeviceConfig(
    id=1,
    name="temp_sensor",
    title="Temperature",
    type="temperature",
    topic="/sensors/temp",
    frequency=0.5, #Delay between updates, in seconds
    failure_frequency=0, #Every nth transmission
    payload_generator=device_data_1.generate_payload_data
)

# IoTDevice2 = IoTDeviceConfig()
# IoTDevice3 = IoTDeviceConfig()

device_config = [IoTDevice1]
