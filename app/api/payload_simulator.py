from dataclasses import dataclass
import logging
from typing import Callable
from app.api.data_generator import DataGenerator, DateTimeConfig, GaussConfig
from app.api.helpers.sequence_gen import sequence_gen
from app.api.helpers.serializable_dataclass import SerializableDataclass


@SerializableDataclass
@dataclass
class Payload:
    id: int
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

    def __init__(self, count: int, data: list, date_seq: list):
        self.data = data
        self.date_seq = date_seq
        self.id_gen = sequence_gen(1000)

        # Generate random sequence of transmissions to "miss"
        miss_count = count // 100
        self.transmissions_missed = DataGenerator(
            "gaussian", aslist=True, count=miss_count, decimals=0, gauss_config=GaussConfig(mean=100, std=20)).values
        self.transmissions_missed = create_sequence(
            self.transmissions_missed, 100)

        logging.debug(f'self.transmissions_missed {len(self.transmissions_missed) }')

        # Generate sequence of points where the generator should miss a whole series of transmissions
        # About every 150th trans
        # miss_count = count // 150
        # skip_blocks_start = DataGenerator(
        #     "gaussian", aslist=True, count=miss_count, decimals=0, gauss_config=GaussConfig(mean=150, std=20)).values
        # skip_number = DataGenerator("constant", value_range=[10,100], count=1)
        # self.transmissions_skip_block = zip(
        #     create_sequence(self.skip_blocks_start, 150),
        #     skip_number
        # )


    # Call the PayloadSimulator instance to generate the next payload
    def __call__(self):
        if self.data is None:
            return

        self.counter += 1

        # Pop next data and date value
        value = self.data.pop()
        date_val = self.date_seq[0]
        self.date_seq = self.date_seq[1:]

        payload_obj = Payload(
            id=self.id_gen.next(),
            timecode=date_val,
            temperature=value
        )

        payload = self.simulate_errors(payload_obj)

        if payload:
            return payload.to_json()
        return payload

    def simulate_errors(self, payload):
        if not self.transmissions_missed:
            return

        if self.counter == self.transmissions_missed[0]:
            self.transmissions_missed = self.transmissions_missed[1:]
            return

        return payload
