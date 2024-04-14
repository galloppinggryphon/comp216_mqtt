from app.api.data_generator import DataGenerator, DateTimeConfig
from app.api.helpers.iot_device_config import IoTDeviceConfig
from app.api.payload_simulator import PayloadSimulator


connection_settings = {
    "host": "localhost",
    "port": 1883,
    # "keepalive": 60
}

##### SHARED DEVICE CONFIG #####
count = 1000
start_date_time = "2024-04-01 00:00"

date_range = DataGenerator("dates", count=count, aslist=True, date_time_config=DateTimeConfig(
    start_date_time=start_date_time,
    interval=1,
    time_unit="minute",
    format="epoch"
)).values


##### DEVICE 1 #####
# Outdoor

device1_data = DataGenerator(
    type="brownian",
    count=count,
    aslist=True,
    value_range=(-5, 20),
    decimals=1
).values

IoTDevice1 = IoTDeviceConfig(
    id=1,
    name="outdoor_sensor",
    title="Outdoor",
    type="temperature",
    topic="/temp/outdoor",
    # frequency=1/10, #Delay between updates, in seconds
    frequency=0.5,  # DEBUGGING VALUE
    data_config={
        "count": count,
        "value_range": (-5, 20),
        "date_range": date_range,
        "data": device1_data
        # "start_date_time": start_date_time,
    },
    # payload_generator=PayloadSimulator(
    #     count=count,
    #     data=device1_data,
    #     date_seq=date_range
    # )
)

##### DEVICE 2 #####
device1_data = ...
IoTDevice2 = ...

##### CLIENT SETTINGS #####
client1 = {
    "id": 1,

}


device_config = [IoTDevice1]
