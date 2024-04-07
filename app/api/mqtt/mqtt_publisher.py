from typing import Optional
from app.api.mqtt.mqtt_subscriber import MQTTClient

class MQTTPublisher(MQTTClient):
    def __init__(self, connection_settings,  id: Optional[str] = None):
        super().__init__("publisher", connection_settings, id)

    def publish(self, topic, message):
        self.mqttc.publish(topic, payload=message)


if __name__ == "__main__":
    ...
