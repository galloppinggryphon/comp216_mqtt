from dataclasses import dataclass
import json
import logging
from typing import Callable, Optional, Type

from app.api.mqtt_client import MQTTClient


@dataclass
class MQTTSubscriberOptions:
    log_message_received: Optional[bool] = None
    log_message_received_verbose: Optional[bool] = None
    sys_messages: Optional[bool] = None

class MQTTSubscriber(MQTTClient):
    subscriptions: set[str]
    # message_queue: Queue
    message_callback = lambda data: ...
    print_messages = False
    options: Type[MQTTSubscriberOptions]

    def __init__(self, connection_settings, id: Optional[str] = None):
        super().__init__("subscriber", connection_settings, id)
        self.subscriptions = set()
        # self.message_queue = Queue()
        self.options = MQTTSubscriberOptions
        self.mqttc.on_subscribe = self._on_subscribe
        self.mqttc.on_message = self._on_message
        logging.info(f"Create subscriber {self.client_id}")


    def subscribe(self, topic):
        self.subscriptions.add(topic)

        if self.is_connected:
            logging.info(f"Subscribing to {topic}")
            self.mqttc.subscribe(topic)

    def unsubscribe(self, topic):
        if not topic in self.subscriptions:
            logging.info(f"Error: Not subscribed to `{topic}, cannot unsubscribe.")
            return

        self.subscriptions.remove(topic)

        if self.is_connected:
            self.mqttc.unsubscribe(topic)

    def set_callback(self, callback: Callable):
        self.message_callback = callback

    def set_options(
        self,
        log_message_received=None,
        log_message_received_verbose=None,
        sys_messages=None,
    ):
        opt = self.options

        if sys_messages is not None:
            if sys_messages:
                opt.sys_messages = True
                self.subscribe("$SYS/#")
            else:
                opt.sys_messages = True
                self.unsubscribe("$SYS/#")

        if log_message_received is not None:
            if log_message_received:
                opt.log_message_received = log_message_received
            else:
                opt.log_message_received = log_message_received
        elif log_message_received_verbose is not None:
            if log_message_received_verbose:
                opt.log_message_received_verbose = log_message_received_verbose
            else:
                opt.log_message_received_verbose = log_message_received_verbose

    def _on_subscribe(self, client, userdata, mid, reason_code_list, properties):
        if reason_code_list[0].is_failure:
            logging.error(f"Broker rejected you subscription: {reason_code_list[0]}")
        else:
            logging.info(f"Broker granted the following QoS: {reason_code_list[0].value}")

    def _on_message(self, client, userdata, message):
        data = self._parse_message(message)

        if self.options.log_message_received:
            logging.info(f'Received message (topic={data["topic"]})')
        elif self.options.log_message_received_verbose:
            logging.debug(data["topic"], ":", data["payload"])

        self.message_callback(data)

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            logging.error(
                f"Failed to connect: {reason_code}."
            )  # loop_forever() will retry connection
        else:
            logging.info(f"Connected to {client.host}:{client.port}")

            if self.subscriptions:
                logging.info(f"Subscribing to {", ".join(self.subscriptions)}")
                topics = [(topic, 1) for topic in self.subscriptions]
                client.subscribe(topics)



if __name__ == "__main__":
    ...
