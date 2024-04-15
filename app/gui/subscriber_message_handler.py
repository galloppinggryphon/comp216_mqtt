import logging
from typing import Callable
import numpy as np


class SubscriberMessageHandler:
    # device_config: IoTDeviceConfig
    next_update: np.datetime64 = ...
    # callback_message_queues: dict[str, list]
    message_queue: list
    update_interval: int
    callbacks: list[Callable]

    def __init__(self, update_interval):
        self.callbacks = []
        self.message_queue = []
        self.update_interval = update_interval

    def add_callback(self, function):
        self.callbacks.append(function)

    def on_message(self, timecode, topic, data):
        if self.next_update == ...:
            should_update = True
        else:
            should_update = self.compare_timestamps(self.next_update, timecode)

        self.sub1_last_message = data

        if not should_update:
            message = {
                "timecode": timecode, "data": data, "topic": topic
            }
            self.message_queue.append(message)
            return

        logging.debug("Updating GUI")

        self.next_update = self.get_time_diff(timecode, self.update_interval)

        for callback in self.callbacks:
            callback(data, self.message_queue)

    def compare_timestamps(self, time1, time2):
        time2_dt = np.datetime64(time2, "s")
        return time2_dt >= time1

    def get_time_diff(self, timestamp, interval):
        time_span = interval
        date_diff = np.timedelta64(time_span, "s")
        timestamp_dt = np.datetime64(timestamp, "s")
        return timestamp_dt + date_diff
