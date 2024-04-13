from dataclasses import dataclass
from random import choice
import time
from typing import Any
import numpy as np
from app.api.data_generator import DataGenerator
from app.api.helpers.iot_device_config import PayloadBase
from app.api.helpers.sequence_gen import sequence_gen


# Type: dataclass
@dataclass
class Payload(PayloadBase):
    location: str
    timecode: str
    temperature: float


# Config
id_gen = sequence_gen(1000)

# Define generators
temp_gen = DataGenerator(type="brownian", count=100, value_range=(10, 35), decimals=1)

temperature_data = temp_gen.values.tolist()

def generate_payload_data():

    # temp = temperature_data[0]
    # temperature_data = temperature_data[1:]

    temp = temperature_data.pop()

    return Payload(
        id=id_gen.next(),
        location="location",
        timecode=time.asctime(),
        temperature = temp
    )
