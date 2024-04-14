from dataclasses import dataclass
from typing import Any, Callable

from app.api.payload_simulator import Payload, PayloadSimulator

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
    payload_generator: Callable[..., Payload] = ...

    def configure_payload(self):
        self.payload_generator = PayloadSimulator(
            count=self.data_config["count"],
            data=self.data_config["data"],
            date_seq=self.data_config["date_range"]
        )

    # data_config={
    #     "count": count,
    #     "value_range":(-5, 20),
    #     # "start_date_time": start_date_time,
    # },
    # payload_generator=PayloadSimulator(
    #     count=count,
    #     data=device1_data,
    #     date_seq=date_range
    # )
