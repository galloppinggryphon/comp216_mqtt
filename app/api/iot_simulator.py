from dataclasses import dataclass
from datetime import datetime
import json
import logging
from time import sleep
from typing import Any, Callable, Iterable, NamedTuple, Optional, TypeVar, cast
from app.api.helpers.bool_signal import BoolSignal
from app.api.helpers.iot_device_config import IoTDeviceConfig
from app.api.helpers.thread_worker import ThreadWorker
from app.api.mqtt_publisher import MQTTPublisher
from app.api.mqtt_subscriber import MQTTSubscriber
from app.api.helpers.threadsafe_singleton_meta import ThreadsafeSingletonMeta
from app.helpers.utils import list_find


@dataclass
class PublisherListItem:
    id: int
    name: str
    topic: str
    config: IoTDeviceConfig
    client: MQTTPublisher
    stop: BoolSignal
    on_complete_or_interrupted: Callable


@dataclass
class SubscriberListItem:
    id: str
    # config: IoTDeviceConfig
    client: MQTTSubscriber
    stop: BoolSignal
    topics: set[str]
    callbacks: list[Callable]
    get_publishers: Callable[..., dict[str, PublisherListItem]]


class _IoTSimulator(metaclass=ThreadsafeSingletonMeta):
    mqtt_config: Any
    publishers: list[PublisherListItem]
    subscribers: list[SubscriberListItem]

    @property
    def running_publishers(self):
        # Count how many publishers are _not_ stopped, i.e. running
        return {pub.name: not pub.stop for pub in self.publishers}

    def __init__(self):
        self.mqtt_config = {}
        self.publishers = []
        self.subscribers = []
        # self.subscription_message_handlers = {}

    # Call the initialized singleton to configure it
    def __call__(self, mqtt_config):
        self.mqtt_config = mqtt_config

    ###### SUBSCRIBERS ######
    def create_subscriber(self, sub_id: str, topics: list[str]):
        sub = MQTTSubscriber(self.mqtt_config)

        sub.set_options(log_message_received=True)
        sub.subscribe(*topics)

        list_item = SubscriberListItem(
            id=sub_id,
            # config=...,
            client=sub,
            stop=BoolSignal(True),
            topics=set(topics),
            callbacks=[],
            get_publishers=lambda: {topic: self.get_publisher_by_topic(topic) for topic in topics}
        )

        self.subscribers.append(list_item)

        logging.info(f'Created subscriber: {list_item.id}')

        return list_item

    def get_subscriber(self, sub_id: str) -> SubscriberListItem | None:
        sub = list_find(self.subscribers, False, lambda sub: sub.id == sub_id)
        return sub if sub else None

    def start_subscriber(self, sub_id: int, on_error: Callable = ...):
        sub = self.get_subscriber(sub_id)

        if not sub:
            logging.error(f"Cannot start subscriber: #'{
                          sub_id}' does not exist.")
            return

        sub.client.connect(asynchronous=True, loop=True)

        return sub

    def subscriber_add_callback(self, sub_id: str, on_message: Callable):
        sub = self.get_subscriber(sub_id)
        if not sub:
            return

        sub.client.set_callback(self._subscriber_message_handler(on_message))


    def subscriber_wait(self):
        sub = self.get_subscriber(1)  # type: ignore
        sub.worker.wait()  # type: ignore

    def stop_subscriber(self, sub_id: str):
        sub = self.get_subscriber(sub_id)  # type: ignore

        if not sub:
            logging.error(f"Cannot stop subscriber: #'{
                          sub_id}' does not exist.")
            return

        if not sub.client.is_connected:
            logging.warn(f"Cannot stop subscriber: '{
                         sub_id}' is not running.")
            return

        sub.client.disconnect()
        sub.client.loop_stop()

        return sub

    def destroy_subscriber(self, sub_id: str):
        sub = self.stop_subscriber(sub_id)

        if sub:
            del sub
            logging.info(f"Subscriber '{sub_id}' destroyed.")

    def _subscriber_message_handler(self, on_message):
        def _message_handler(data):
            payload = json.loads(data['payload'])
            timestamp = datetime.fromtimestamp(data['timestamp'])
            on_message(timestamp, data['topic'], payload)

        return _message_handler

    ###### PUBLISHERS ######

    def create_publisher(self, config: IoTDeviceConfig):
        pub_item = self.get_publisher(config.name)
        if pub_item:
            return pub_item.client

        config.configure_payload()

        pub = MQTTPublisher(self.mqtt_config, config.name)
        list_item = PublisherListItem(
            id=config.id,
            name=config.name,
            topic=config.topic,
            config=config,
            client=pub,
            stop=BoolSignal(True),
            on_complete_or_interrupted=...
        )
        self.publishers.append(list_item)

        logging.info(f'Created publisher: {list_item.name} (#{list_item.id})')

        return pub

    def get_publisher(self, pub_name: str) -> PublisherListItem | None:
        pub = list_find(self.publishers, False,
                        lambda pub: pub.name == pub_name)
        return pub if pub else None

    def get_publisher_by_id(self, pub_id: int) -> PublisherListItem | None:
        pub = list_find(self.publishers, False,
                        lambda pub: pub.id == pub_id)
        return pub if pub else None

    def get_publisher_by_topic(self, topic: str) -> PublisherListItem | None:
        pub = list_find(self.publishers, False,
                        lambda pub: pub.topic == topic)
        return pub if pub else None

    def is_publisher_running(self, pub_name: str):
        pub = self.get_publisher(pub_name)
        return False if not pub else not pub.stop.value

    # Start IoT device
    def start_publisher(self, pub_name: str, on_complete_or_interrupted: Optional[Callable] = None):
        pub = self.get_publisher(pub_name)

        if on_complete_or_interrupted:
            pub.on_complete_or_interrupted = on_complete_or_interrupted  # type: ignore

        if not pub:
            logging.error(f"Cannot start publisher: '{
                          pub_name}' does not exist.")
            pub.on_complete_or_interrupted()
            return

        def _start_publisher():
            res = pub.client.connect()  # type: ignore
            if res:
                pub.stop.reset()  # type: ignore
                self.__publisher_loop(pub)  # type: ignore
            else:
                pub.on_complete_or_interrupted()  # type: ignore

        ThreadWorker(_start_publisher, background=True)

    def stop_publisher(self, pub_name: str):
        pub = self.get_publisher(pub_name)

        if not pub:
            logging.error(f"Cannot stop publisher: '{
                          pub_name}' does not exist.")
            return

        if pub.stop.value:
            logging.warn(f"Cannot stop publisher: '{
                         pub_name}' is not running.")
            return

        pub.stop()
        pub.on_complete_or_interrupted()

    def update_publisher_config(self, device_id: int, new_config):
        pub = self.get_publisher_by_id(device_id)

        if not pub:
            return

        pub.config.title = new_config['title']
        pub.config.frequency = new_config['frequency']
        pub.config.data_config['value_range'] = new_config['value_range']

        # Regenerate device data
        pub.config.configure_payload()

        logging.info(f"Configuration saved for Device {device_id}")

    def publisher_get_payload_preview(self, pub_name: str):
        pub = self.get_publisher(pub_name)

        if not pub:
            return

        payload = pub.config.payload_generator()

        return payload

    # Run this method threaded
    def __publisher_loop(self, pub: PublisherListItem):
        frequency, payload_generator, topic = pub.config.frequency, pub.config.payload_generator, pub.config.topic
        logging.info(f"Publisher '{pub.client.client_id}' is running")

        # Short loops to maintain responsiveness
        short_sleep = 0.1
        short_cycles = 1

        if frequency <= short_sleep:
            short_sleep = short_sleep
        else:
            short_cycles = frequency / short_sleep

        sleep_counter = 0
        round = 0

        # Run until stop signal is encountered
        while not pub.stop.value:
            sleep_counter += 1
            if sleep_counter <= short_cycles:
                sleep(short_sleep)  # Delay in seconds
                continue

            # TODO: This may be a place to simulate one of the failure modes
            round += 1
            logging.info(
                f"Publisher '{pub.client.client_id}': publish {round}")

            sleep_counter = 0
            data = self.__publisher_next_payload(pub.name, payload_generator)

            if not data:
                break

            # If data is empty, skip
            if data:
                pub.client.publish(topic, data)

        logging.info(f"Publisher '{pub.client.client_id}' stopped")
        pub.client.disconnect()
        pub.stop()
        pub.on_complete_or_interrupted()


    def __publisher_next_payload(self, pub_name: str, payload_generator: Callable):
        try:
            return payload_generator()
        except(IndexError):
            logging.info(f"No more data for device {pub_name}: reached the end of data generated for the simulator.")





# Init singleton
IoTSimulator = _IoTSimulator()
