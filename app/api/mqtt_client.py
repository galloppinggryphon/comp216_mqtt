import logging
import random
from typing import Optional
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

id_range = (1000000,9999999)


class MQTTClient:
    mqttc: mqtt.Client
    mode = ""
    blocking_loop = False
    threaded_loop = False
    connection_settings: dict
    client_id: str

    @property
    def host(self):
        return f"{self.connection_settings["host"]}:{self.connection_settings["port"]}"

    @property
    def is_connected(self):
        return self.mqttc.is_connected()

    def __init__(self, mode, connection_settings, id = None):
        self.connection_settings = connection_settings
        self.mode = mode
        self.client_id = self.create_client_id(id)

        self.mqttc = mqtt.Client(
            client_id=self.client_id, callback_api_version=CallbackAPIVersion.VERSION2
        )

        self.mqttc.on_connect = self._on_connect
        self.mqttc.on_disconnect = self._on_disconnect

    def create_client_id(self, id: Optional[str] = None):
        _id = id if id else random.randint(*id_range)
        return f"{self.mode}_{_id}"

    def connect(self, blocking_loop=False, threaded_loop=False):
        self.blocking_loop = blocking_loop
        self.threaded_loop = threaded_loop

        logging.info(f"MQTT client {self.client_id} is connecting (mode={self.mode})...")

        try:
            self.mqttc.connect(
            self.connection_settings["host"], self.connection_settings["port"]
        )
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            return False

        if blocking_loop:
            self.mqttc.loop_forever()
        elif threaded_loop:
            self.mqttc.loop_start()

        return True

    def loop_forever(self):
        logging.info("self.mqttc.loop_forever()")
        self.mqttc.loop_forever()

    def loop_start(self):
        self.mqttc.loop_start()

    def loop_stop(self):
        self.mqttc.loop_stop()

    def disconnect(self):
        self.mqttc.disconnect()

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            logging.error(
                f"Failed to connect: {reason_code}."
            )  # loop_forever() will retry connection
        else:
            logging.info(f"Connected to {client.host}:{client.port}")

    def _on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        logging.info(f"Client {self.client_id} has disconnected ({str(reason_code)})")
        client.loop_stop()

    def _parse_message(self, message: mqtt.MQTTMessage):
        obj = {
            "topic": message.topic,
            "payload": message.payload.decode(),
            "timestamp": message.timestamp,
            "qos": message.qos,
        }
        return obj

    def __repr__(self):
        return f"""<MQTTClient id={self.client_id}>
mode: {self.mode}
loop: {'blocking' if self.blocking_loop else ('threaded' if self.threaded_loop else 'no')}
is_connected: {self.is_connected}
host: {self.host}"""
