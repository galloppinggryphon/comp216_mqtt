from dataclasses import dataclass
from typing import Any, Callable

from app.api.helpers.serializable_dataclass import SerializableDataclass


@SerializableDataclass
@dataclass
class PayloadBase:
    id: int


@dataclass
class IoTDeviceConfig:
    """
    id: int # Unique numeric ID
    name: str # Short device name, no spaces
    title: str # Human readable name
    """
    id: int # Unique numeric ID
    name: str # Short device name, no spaces
    title: str # Human readable name
    type: str
    topic: str
    frequency: int
    data_config: dict[str, Any]
    payload_generator: Callable[..., PayloadBase]