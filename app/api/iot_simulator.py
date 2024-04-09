from dataclasses import dataclass
import json
import logging
from time import sleep
from typing import Any, Callable, NamedTuple, Optional, TypeVar, cast
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
    'name', str), ('config', IoTDeviceConfig), ("client", MQTTPublisher), ("abort_signal", Optional[BoolSignal])])

@dataclass
class PublisherListItem:
    id: str
    config: IoTDeviceConfig
    client: MQTTPublisher
    abort_signal: Optional[BoolSignal]


class _IoTSimulator(metaclass=ThreadsafeSingletonMeta):
    mqtt_config: Any
    publishers: list[PublisherListItem]
    subscribers: list[SubscriberListItem]

    # Register of message handlers (methods) triggered by different subscription topics
    subscription_message_handlers: dict[str, list[Callable]]

    @property
    def running_publishers(self):
        return {pub.id: not pub.abort_signal for pub in self.publishers}

    def __init__(self):
        self.mqtt_config = {}
        self.publishers = []
        self.subscribers = []
        self.subscription_message_handlers = {}

    # Call the initialized singleton to configure it
    def __call__(self, mqtt_config):
        self.mqtt_config = mqtt_config

    def create_publisher(self, config: IoTDeviceConfig):
        pub_item = self.get_publisher(config.id)
        if pub_item:
            return pub_item.client

        pub = MQTTPublisher(self.mqtt_config, config.id)
        list_item = PublisherListItem(
            id=config.id, config=config, client=pub, abort_signal=None)
        self.publishers.append(list_item)

        return pub

    def get_publisher(self, pub_id: str) -> PublisherListItem | None:
        pub = list_find(self.publishers, False, lambda pub: pub.id == pub_id)
        return pub if pub else None

    def create_subscriber(self, topic, on_message):
        self.add_message_handler(topic, on_message)
        sub = MQTTSubscriber(self.mqtt_config)

        sub.set_callback(self._subscriber_message_handler)
        sub.set_options(log_message_received=True)
        sub.subscribe(topic)
        sub.connect(threaded_loop=True)

    def start_publisher(self, pub_id: str):
        # topic = "COMP216"
        # pub = MQTTPublisher(self.mqtt_config)
        # pub.connect()

        # print("\n", pub, "\n")

        # print(pub.mqttc.host)

        # for i in range(0, 10):
        #     print(f"Publish message #{i}")
        #     data = create_sensor_data()
        #     pub.publish(topic, data.to_json())
        #     sleep( 1)

        # pub.disconnect()

        # print(pub.mqttc.host)

        # pub = self.add_publisher(id)

        pub = self.get_publisher(pub_id)

        if not pub:
            logging.error(f"Cannot start publisher: '{pub_id}' does not exist.")
            return

        res = pub.client.connect()
        if res:
            pub.abort_signal = BoolSignal()
            self.__loop(pub)

    def __loop(self, pub: PublisherListItem):
        # Start device simulation
        abort_signal, frequency, payload_generator, topic = pub.abort_signal, pub.config.frequency, pub.config.payload_generator, pub.config.topic

        logging.info("Simulator is running")

        while abort_signal and not abort_signal.is_true:

            # TODO: This may be a place to simulate one of the failure modes

            sleep(frequency)  # Delay in seconds
            data = payload_generator()

            logging.debug("payload_generator data:")
            logging.debug(data)

            pub.client.publish(topic, data.to_json())

        pub.client.disconnect()

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
