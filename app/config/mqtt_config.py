from app.api.data_generator import DataGenerator, DateTimeConfig, GaussConfig
from app.api.helpers.iot_device_config import IoTDeviceConfig

connection_settings = {
    "host": "localhost",
    "port": 1883,
}


##### SHARED DEVICE CONFIG #####
count = 10000
frequency = 1/5  # Delay between updates, in seconds
start_date_time = "2024-04-01 00:00"

date_range = DataGenerator("dates", count=count, aslist=True, date_time_config=DateTimeConfig(
    start_date_time=start_date_time,
    interval=1,
    time_unit="minute",
    format="epoch"
)).values


def data_generator(data_config):
    return DataGenerator(
        type=data_config["generator_type"],
        aslist=True,
        count=data_config["count"],
        value_range=data_config["value_range"],
        decimals=1
    ).values


##### DEVICE 1 #####
IoTDevice1 = IoTDeviceConfig(
    id=1,
    name="outdoor_temp",
    title="Outdoor",
    type="temperature",
    topic="/temp/outdoor",
    frequency=frequency,  # DEBUGGING VALUE
    data_config={
        "generator_type": "brownian",
        "count": count,
        "value_range": (-5, 20),
        "date_range": date_range,
    },
    data_generator=data_generator
)

##### DEVICE 2 #####
IoTDevice2 = IoTDeviceConfig(
    id=2,
    name="living_room_temp",
    title="Living Room",
    type="temperature",
    topic="/temp/living_room",
    frequency=frequency,
    data_config={
        "generator_type": "brownian",
        "count": count,
        "value_range": (18, 25),
        "date_range": date_range,
    },
    data_generator=data_generator
)

##### DEVICE 3 #####
IoTDevice3 = IoTDeviceConfig(
    id=3,
    name="greenhouse_temp",
    title="Greenhouse",
    type="temperature",
    topic="/temp/greenhouse",
    frequency=frequency,
    data_config={
        "generator_type": "brownian",
        "count": count,
        "value_range": (25, 32),
        "date_range": date_range,
    },
    data_generator=data_generator
)

device_config = [IoTDevice1, IoTDevice2, IoTDevice3]
