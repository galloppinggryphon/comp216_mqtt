import logging
from typing import Callable
import numpy as np

from app.gui.framework.utils import format_iso_time, get_time_diff


class SubscriberMessageHandler:
    _elapsed_intervals = 0
    _next_update: np.datetime64 = ...
    _last_message_id: int
    _message_queue: list
    _update_interval: int
    _illegal_packets: list
    __on_message_received_callbacks: list[Callable]
    __on_interval_callbacks: list[Callable]

    def __init__(self, update_interval):
        self.callbacks = []
        self._message_queue = []
        self.__on_message_received_callbacks = []
        self.__on_interval_callbacks = []
        self._update_interval = update_interval
        self._last_message_id = 0
        logging.info(f"Subscriber update interval: {update_interval}s")

    #Triggered for every message
    def add_message_received_callback(self, function):
        self.__on_message_received_callbacks.append(function)

    #Triggered only every interval
    def add_interval_callback(self, function):
        self.__on_interval_callbacks.append(function)

    def on_message(self):
        def _on_message(timecode, topic, data):
            if self._next_update == ...:
                should_update = True
            else:
                should_update = self.compare_timestamps(self._next_update, timecode)

            # Abort if payload is missing
            if not data:
                return

            data['time_formatted'] = format_iso_time(data['timecode'])

            for callback in self.__on_message_received_callbacks:
                _data = callback(data)
                if _data:
                    data = _data

            if not should_update:
                message = {
                    "timecode": timecode, "data": data, "topic": topic
                }
                self._message_queue.append(message)
                return

            self._elapsed_intervals +=1
            logging.info(f"Subscriber interval #{self._elapsed_intervals} (message: #{data['id']}, time: {data['time_formatted']})")

            for callback in self.__on_interval_callbacks:
                callback({"data": data, "queue": self._message_queue, "last_message_id": self._last_message_id})

            self._next_update = get_time_diff(timecode, self._update_interval)
            self._last_message_id = data['id']
            self._message_queue = []

        return _on_message

    @staticmethod
    def compare_timestamps(time1, time2):
        time2_dt = np.datetime64(time2, "s")
        return time2_dt >= time1
