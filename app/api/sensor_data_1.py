from dataclasses import dataclass
from random import choice
import time
from typing import Any
from app.api.data_generator import DataGenerator
from app.api.mqtt.serializable_dataclass import SerializableDataclass

start_id = 1000
locations = ["Toronto", "Montreal", "Vancouver"]

@SerializableDataclass
@dataclass
class Payload:
    id: int
    location: str
    timecode: str
    barometric_pressure_mbar: float
    weather_warnings: list[str]
    wind_speed_ms: int
    precipitation_mm_24h: int
    precipitation_mm_hourly: list[int]
    temperature: float
    temperature_hourly: list[int]



barometric_gen = DataGenerator(type="brownian", value_range=(850, 1100), decimals=1)
temp_gen = DataGenerator(type="brownian", count=24, value_range=(10, 35), decimals=1)
precipitation_gen = DataGenerator(
    type="brownian", count=24, value_range=(0, 50), decimals=1
)
windspeed_gen = DataGenerator(type="brownian", value_range=(0, 50), count=1, decimals=1)



def create_sensor_data():
    start_id = +1

    location = choice(locations)

    precipitation_mm_hourly: Any = precipitation_gen.values
    temperature_hourly: Any = temp_gen.values

    barometric_pressure_mbar = barometric_gen.single
    windspeed = windspeed_gen.single
    weather_warnings = []

    if windspeed > 17.2:
        weather_warnings.append("Wind speed warning")
    if barometric_pressure_mbar < 980:
        weather_warnings.append("Low pressure alert")
    if temperature_hourly[-1] > 30:
        weather_warnings.append("Extreme temperature warning")

    return Payload(
        id=start_id,
        location=location,
        timecode=time.asctime(),
        weather_warnings=weather_warnings,
        barometric_pressure_mbar=barometric_pressure_mbar,
        wind_speed_ms=windspeed,
        temperature=temperature_hourly[-1],
        precipitation_mm_24h=round(sum(precipitation_mm_hourly), 1),
        precipitation_mm_hourly=precipitation_mm_hourly,
        temperature_hourly=temperature_hourly,
    )
