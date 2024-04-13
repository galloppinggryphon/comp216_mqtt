from app.api.data_generator import DataGenerator, DateTimeConfig
from app.api.helpers.iot_device_config import IoTDeviceConfig
from app.api.payload_simulator import PayloadSimulator


connection_settings = {
    "host": "localhost",
    "port": 1883,
    # "keepalive": 60
}

##### SHARED DEVICE CONFIG #####
count = 100
start_date_time = "2024-04-01 00:00"

date_range = DataGenerator("dates", count=count, aslist=True, date_time_config=DateTimeConfig(
    start_date_time=start_date_time,
    interval=1,
    time_unit="minute",
    format="epoch"
)).values


##### DEVICE DATA #####

#Outdoor
device1_data = DataGenerator(
    type="brownian",
    count=count,
    aslist=True,
    value_range=(-5, 20),
    decimals=1
).values

##### DEVICE SETTINGS #####
IoTDevice1 = IoTDeviceConfig(
    id=1,
    name="outdoor_sensor",
    title="Outdoor",
    type="temperature",
    topic="/temp/outdoor",
    frequency=0.5, #Delay between updates, in seconds
    failure_frequency=0, #Every nth transmission
    data_config={
        "count": count,
        "value_range":(-5, 20),
        "start_date_time": start_date_time,
    },
    payload_generator=PayloadSimulator(
        count=count,
        data=device1_data,
        date_seq=date_range
    )
)

# print('\nHello\n')

# print(IoTDevice1)

# IoTDevice2 = IoTDeviceConfig(
#     id=1,
#     name="livingroom_sensor",
#     title="Living Room",
#     type="temperature",
#     topic="/temp/living_room",
#     frequency=1, #Delay between updates, in seconds
#     failure_frequency=0, #Every nth transmission
#     payload_generator=device_data_1.generate_payload_data
# )


device_config = [IoTDevice1]
