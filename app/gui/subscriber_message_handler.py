from datetime import datetime
import logging
from typing import Callable
import numpy as np


class SubscriberMessageHandler:
    _elapsed_intervals = 0
    _next_update: np.datetime64 = ...
    _message_queue: list
    _update_interval: int
    __on_message_received_callbacks: list[Callable]
    __on_interval_callbacks: list[Callable]

    def __init__(self, update_interval):
        self.callbacks = []
        self._message_queue = []
        self.__on_message_received_callbacks = []
        self.__on_interval_callbacks = []
        self._update_interval = update_interval
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

            data['time_formatted'] = self.format_iso_time(data['timecode']) #self.format_time(data['timecode'], "%Y-%m-%d %H:%M:%S")

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

            self._message_queue = []
            self._elapsed_intervals +=1
            logging.info(f"Subscriber interval #{self._elapsed_intervals} (message: #{data['id']}, time: {data['time_formatted']})")

            self._next_update = self.get_time_diff(timecode, self._update_interval)

            for callback in self.__on_interval_callbacks:
                callback({"data": data, "queue": self._message_queue})

        return _on_message

    @staticmethod
    def compare_timestamps(time1, time2):
        time2_dt = np.datetime64(time2, "s")
        return time2_dt >= time1

    @staticmethod
    def get_time_diff(timestamp, interval):
        time_span = interval
        date_diff = np.timedelta64(time_span, "s")
        timestamp_dt = np.datetime64(timestamp, "s")
        return timestamp_dt + date_diff

    @staticmethod
    def format_time(timestamp: int, format: str):
        return np.datetime64.item(timestamp).strftime(format)

    @staticmethod
    def format_iso_time(timestamp: int):
        return datetime.fromtimestamp(timestamp).isoformat()
