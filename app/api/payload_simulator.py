from dataclasses import dataclass
import logging
import numpy as np
from typing import Callable, reveal_type
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
    transmissions_skip_blocks: list[tuple[int,int]] # list[dict[str, int]]
    id_gen: Callable
    skip_blocks = 0

    def __init__(self, count: int, data: list, date_seq: list):
        #reverse so we can use pop
        data.reverse()
        date_seq.reverse()

        self.data = data
        self.date_seq = date_seq
        self.id_gen = sequence_gen(1000)

        # Generate random sequence of transmissions to "miss", approximately every 100th transmission
        approx_location = 100
        seq_len = count // approx_location
        sequence = DataGenerator(
            "gaussian", aslist=True, count=seq_len, decimals=0, gauss_config=GaussConfig(mean=approx_location, std=15)).values
        self.transmissions_missed = create_sequence(
            sequence, approx_location)
        self.transmissions_missed.reverse()

        # Generate sequence of points where the generator should miss a whole series of transmissions
        # About every 150th trans
        approx_location = 150
        seq_len = count // approx_location
        sequence = DataGenerator(
            "gaussian", aslist=True, count=seq_len, decimals=0, gauss_config=GaussConfig(mean=approx_location, std=20)).values

        #Number of blocks to skip
        skip_number = DataGenerator(
            "gaussian", aslist=True, count=seq_len, decimals=0, gauss_config=GaussConfig(mean=30, std=15)).values

        self.transmissions_skip_blocks = list(zip(
            create_sequence(sequence, approx_location),
            skip_number
        ))
        self.transmissions_skip_blocks.reverse()

        #Transmit gibberish
        approx_location = 75
        seq_len = count // approx_location
        sequence = DataGenerator(
            "gaussian", aslist=True, count=seq_len, decimals=0, gauss_config=GaussConfig(mean=approx_location, std=5)).values
        self.transmissions_send_gibberish = create_sequence(
            sequence, approx_location)
        self.transmissions_send_gibberish.reverse()

        self.transmissions_send_gibberish = [5,4,3,2]

        logging.debug('***************************************')
        logging.debug(f'transmissions_missed {self.transmissions_missed}')
        logging.debug(f'transmissions_skip_blocks {self.transmissions_skip_blocks}')
        logging.debug('***************************************')


    # Call the PayloadSimulator instance to generate the next payload
        if self.data is None:
            # Return nothing
            return

        self.counter += 1

        # Pop next data and date value
        value = self.data.pop()
        date_val = self.date_seq.pop()

        if self.skip_blocks:
            self.skip_blocks -= 1
            return 0

        payload_obj = Payload(
            id=self.id_gen.next(),
            timecode=date_val,
            temperature=value
        )

        payload = self.simulate_errors(payload_obj)

        if isinstance(payload, Payload):
            return payload.to_json()

        return payload

    def simulate_errors(self, payload):
        skip_single = None
        skip_blocks = (None, None)
        send_gibberish = None

        if self.transmissions_missed:
            skip_single = self.transmissions_missed[-1]

        if self.transmissions_skip_blocks:
            skip_blocks = self.transmissions_skip_blocks[-1]

        if self.transmissions_send_gibberish:
            send_gibberish = self.transmissions_send_gibberish[0]

        if self.counter == skip_single:
            self.transmissions_missed.pop()

            logging.info("Simulating a single missed/skipped transmissions.")
            return 0

        if self.counter == skip_blocks[0]:
            self.transmissions_skip_blocks.pop()
            self.skip_blocks = skip_blocks[1] - 1

            logging.info(f"Simulating missed/skipped transmissions (skipping {self.skip_blocks}).")
            return 0

        if self.counter == send_gibberish:
            self.transmissions_send_gibberish.pop()
            data = np.random.bytes(10)

            logging.info(f"Simulating corrupt data transmission.")
            return data

        return payload
