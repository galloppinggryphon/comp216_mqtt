from dataclasses import dataclass
import json
import logging
import threading
from time import sleep
from typing import Any, Callable, Iterable, NamedTuple, Optional, TypeVar, cast
from app.api.helpers.bool_signal import BoolSignal
from app.api.helpers.iot_device_config import IoTDeviceConfig
from app.api.mqtt_publisher import MQTTPublisher
from app.api.mqtt_subscriber import MQTTSubscriber
from app.api.helpers.threadsafe_singleton_meta import ThreadsafeSingletonMeta


def list_find(iterable, default=False, predicate=None) -> Any:
    return next(filter(predicate, iterable), default)


SubscriberListItem = NamedTuple('SubscriberListItem', [(
    'name', str), ('config', IoTDeviceConfig), ("client", MQTTSubscriber)])
PublisherListItem_ = NamedTuple('PublisherListItem', [(
    'name', str), ('config', IoTDeviceConfig), ("client", MQTTPublisher), ("stop", Optional[BoolSignal])])


@dataclass
class PublisherListItem:
    id: str
    config: IoTDeviceConfig
    client: MQTTPublisher
    stop: BoolSignal
    on_complete_or_interrupted: Callable


class _IoTSimulator(metaclass=ThreadsafeSingletonMeta):
    mqtt_config: Any
    publishers: list[PublisherListItem]
    subscribers: list[SubscriberListItem]

    # Register of message handlers (methods) triggered by different subscription topics
    subscription_message_handlers: dict[str, list[Callable]]

    @property
    def running_publishers(self):
        # Count how many publishers are _not_ stopped, i.e. running
        return {pub.id: not pub.stop for pub in self.publishers}

    def __init__(self):
        self.mqtt_config = {}
        self.publishers = []
        self.subscribers = []
        self.subscription_message_handlers = {}

    # Call the initialized singleton to configure it
    def __call__(self, mqtt_config):
        self.mqtt_config = mqtt_config

    def create_publisher(self, config: IoTDeviceConfig):
        pub_item = self.get_publisher(config.name)
        if pub_item:
            return pub_item.client

        pub = MQTTPublisher(self.mqtt_config, config.name)
        list_item = PublisherListItem(
            id=config.name,
            config=config,
            client=pub,
            stop=BoolSignal(True),
            on_complete_or_interrupted=lambda: ... #Placeholder
        )
        self.publishers.append(list_item)

        return pub

    def get_publisher(self, pub_name: str) -> PublisherListItem | None:
        pub = list_find(self.publishers, False, lambda pub: pub.id == pub_name)
        return pub if pub else None

    def is_publisher_running(self, pub_name: str):
        pub = self.get_publisher(pub_name)
        return False if not pub else not pub.stop.value

    def create_subscriber(self, topic, on_message):
        self.add_message_handler(topic, on_message)
        sub = MQTTSubscriber(self.mqtt_config)

        sub.set_callback(self._subscriber_message_handler)
        sub.set_options(log_message_received=True)
        sub.subscribe(topic)
        sub.connect(threaded_loop=True)

    def start_publisher(self, pub_name: str, on_complete_or_interrupted: Optional[Callable] = None):
        pub = self.get_publisher(pub_name)

        if on_complete_or_interrupted:
            pub.on_complete_or_interrupted = on_complete_or_interrupted

        if not pub:
            logging.error(f"Cannot start publisher: '{
                          pub_name}' does not exist.")
            pub.on_complete_or_interrupted()
            return

        print('pub.stop', [not pub.stop for pub in self.publishers])

        def _start():
            res = pub.client.connect()
            if res:
                pub.stop.reset()
                self.__publisher_loop(pub)
            else:
                pub.on_complete_or_interrupted()

        self.__run_in_thread(_start)

    def stop_publisher(self, pub_name: str):
        pub = self.get_publisher(pub_name)

        if not pub:
            logging.error(f"Cannot stop publisher: '{pub_name}' does not exist.")
            return

        if pub.stop.value:
            logging.warn(f"Cannot stop publisher: '{pub_name}' is not running.")
            return

        pub.stop()  # type: ignore

    def __publisher_loop(self, pub: PublisherListItem):
        frequency, payload_generator, topic = pub.config.frequency, pub.config.payload_generator, pub.config.topic

        logging.info(f"Publisher '{pub.client.client_id}' is running")

        # Short loops to maintain responsiveness
        short_sleep = 0.1
        short_cycles = frequency if frequency <= short_sleep else frequency / short_sleep
        counter = 0

        # Run until stop signal is encountered
        while not pub.stop.value:
            counter += 1
            if counter <= short_cycles:
                sleep(short_sleep)  # Delay in seconds
                continue

            # TODO: This may be a place to simulate one of the failure modes

            logging.info(
                f"Publisher '{pub.client.client_id}': publish {data.id}")
            # logging.debug(data)

            counter = 0
            data = payload_generator()
            pub.client.publish(topic, data.to_json())

        logging.info(f"Publisher '{pub.client.client_id}' stopped")
        pub.client.disconnect()
        pub.stop()
        pub.on_complete_or_interrupted()

    def __run_in_thread(self, fn: Callable, args: Iterable[Any] = []):
        th = threading.Thread(target=fn, daemon=True,
                              args=args)  # Background thread
        th.start()

    def add_message_handler(self, topic: str, callback: Callable):
        self.subscription_message_handlers[topic].append(callback)

    def _subscriber_message_handler(self, data):
        payload = json.loads(data['payload'])

        # Trigger message handlers based on topic
        smh = self.subscription_message_handlers
        for topic in smh:
            if topic == data['topic']:
                map(lambda fn: fn(payload), smh[topic])


# Init singleton
IoTSimulator = _IoTSimulator()
