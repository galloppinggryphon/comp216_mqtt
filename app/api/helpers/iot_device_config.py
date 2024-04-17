from dataclasses import dataclass
import logging
from typing import Any, Callable

from app.api.payload_simulator import Payload, PayloadSimulator


@dataclass
class IoTDeviceConfig:
    """
    id: int # Unique numeric ID
    name: str # Short device name, no spaces
    title: str # Human readable name
    """
    id: int  # Unique numeric ID
    name: str  # Short device name, no spaces
    title: str  # Human readable name
    type: str
    topic: str
    frequency: int
    data_config: dict[str, Any]
    data_generator: Callable[[dict], list]

    # TODO: This should be called "next_payload"
    payload_generator: Callable[..., Payload] = ...

    def configure_payload(self):
        # Generate data
        data = self.data_generator(self.data_config)

        # Create PayloadSimulator
        self.payload_generator = PayloadSimulator(
                    data=data,
                    count=self.data_config["count"],
                    date_seq=self.data_config["date_range"]
                )
