from dataclasses import dataclass
import time
from typing import Callable
from app.api.data_generator import DataGenerator, DateTimeConfig, GaussConfig
from app.api.helpers.iot_device_config import PayloadBase
from app.api.helpers.sequence_gen import sequence_gen


@dataclass
class Payload(PayloadBase):
    timecode: str
    temperature: float

def create_sequence(values, interval):
    seq = [(i * interval) + values[i] for i in range(0, len(values)-1)]
    return seq

class PayloadSimulator:
    counter = 0
    data: list
    date_seq: list
    transmissions_missed: list[int]
    transmissions_send_gibberish: list[int]
    transmissions_skip_blocks: list[dict[str, int]]
    id_gen: Callable


    def __init__(self, count:int, data: list, date_seq: list):
        self.data = data
        self.date_seq = date_seq
        self.id_gen = sequence_gen(1000)

        #Generate list of tranmissions to "miss"
        self.transmissions_missed = DataGenerator("gaussian", aslist=True, count=count, decimals=0, gauss_config=GaussConfig(mean=100,std=20)).values
        self.transmissions_missed = create_sequence(self.transmissions_missed, 100)

    def __call__(self):
        if not self.data:
            return

        self.counter += 1
        temp = self.data.pop()
        date_val = self.date_seq.pop()

        payload_obj = Payload(
            id=self.id_gen.next(),
            timecode=date_val,
            temperature = temp
        )

        payload = self.simulate_errors(payload_obj)
        if payload:
            return  payload.to_json()
        return payload

    def simulate_errors(self, payload):
        if self.counter == self.transmissions_missed[0]:
            self.transmissions_missed = self.transmissions_missed[1:]
            return

        return payload
