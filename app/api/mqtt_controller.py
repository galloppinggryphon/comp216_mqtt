import json
from time import sleep
from typing import Any, Callable
from app.api.mqtt.mqtt_publisher import MQTTPublisher
from app.api.mqtt.mqtt_subscriber import MQTTSubscriber
from app.api.threadsafe_singleton_meta import ThreadsafeSingletonMeta

def list_find(iterable, default=False, predicate=None):
    return next(filter(predicate, iterable), default)


class _MQTTController(metaclass=ThreadsafeSingletonMeta):
    mqtt_config: Any
    publishers: list[tuple[str, MQTTPublisher]]
    subscribers: list[MQTTSubscriber]
    subscription_message_handlers: dict[str, list[Callable]] #Register of message handlers (methods) triggered by different subscription topics

    def __init__(self):
        self.mqtt_config = {}
        self.publishers = []
        self.subscribers = []
        self.subscription_message_handlers = {}

    # Call the initialized singleton to configure it
    def __call__(self, mqtt_config):
        self.mqtt_config = mqtt_config


    def add_subscriber(self, topic, message_handler):
        self.add_message_handler(topic, message_handler)
        sub = MQTTSubscriber(self.mqtt_config.connection_settings)

        # print('\n', sub, '\n')

        sub.set_callback(self._message_handler)
        sub.set_options(log_message_received=True)
        sub.subscribe(topic)
        sub.connect(threaded_loop=True)

    def add_publisher(self, id):
        pub = list_find(self.publishers, False, lambda item_id,_: item_id == id)
        if pub:
            return self.publishers[pub][1]

        pub = MQTTPublisher(self.mqtt_config.connection_settings, id)
        self.publishers.append((id, pub))
        return pub


    def start_publisher(self, id):
        ...
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

        pub = self.add_publisher(id)
        pub.connect()

    def stop_publisher(self, id):
        ...

    def add_message_handler(self, topic: str, callback: Callable):
        self.subscription_message_handlers[topic].append(callback)

    def _message_handler(self, data):
        payload = json.loads(data['payload'])

        # Trigger message handlers based on topic
        smh = self.subscription_message_handlers
        for topic in smh:
            if topic == data['topic']:
                map(lambda fn: fn(payload), smh[topic])


# Init singleton
MQTTController = _MQTTController()
