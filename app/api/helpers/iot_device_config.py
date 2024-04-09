from dataclasses import dataclass
from typing import Callable

from app.api.helpers.serializable_dataclass import SerializableDataclass


@SerializableDataclass
@dataclass
class PayloadBase:
    id: int


@dataclass
class IoTDeviceConfig:
    id: str #
    name: str # Human readable name
    type: str
    topic: str
    frequency: int
    failure_frequency: int
    payload_generator: Callable[..., PayloadBase]
