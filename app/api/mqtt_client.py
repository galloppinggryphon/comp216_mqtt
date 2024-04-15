import logging
import random
from typing import Any, Optional
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

id_range = (1000000,9999999)

class MQTTClient:
    __connection_error = ""
    __is_looping = False
    mqttc: mqtt.Client
    mode = ""
    loop: bool | None = None
    asynchronous: bool | None = None
    connection_settings: dict
    client_id: str

    @property
    def host(self):
        return f"{self.connection_settings["host"]}:{self.connection_settings["port"]}"

    @property
    def is_connected(self):
        return self.mqttc.is_connected()

    @property
    def is_looping(self):
        return self.__is_looping

    @property
    def connection_error(self):
        return self.__connection_error

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
        return f"{self.mode[:3]}_{_id}"

    def connect(self, loop = False, asynchronous = False):
        self.loop = loop
        self.asynchronous = asynchronous

        logging.info(f"MQTT client {self.client_id} is connecting (mode={self.mode})...")

        host, port = self.connection_settings["host"], self.connection_settings["port"]

        try:
            if asynchronous:
                self.mqttc.connect_async(host, port)

                if loop:
                    self.loop_start()

            else:
                self.mqttc.connect(host, port)

                if loop:
                    self.loop_forever()


        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            self.__connection_error = message
            return False

        return True

    def loop_forever(self):
        logging.info("self.mqttc.loop_forever()")
        self.mqttc.loop_forever()

    def loop_start(self):
        self.mqttc.loop_start()
        self.__is_looping = True

    def loop_stop(self):
        self.mqttc.loop_stop()
        self.__is_looping = False

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

    def __repr__(self):
        return f"""[MQTTClient id={self.client_id}]
mode: {self.mode}
loop: {'blocking' if self.loop else ('threaded' if self.asynchronous else 'no')}
is_connected: {self.is_connected}
in_loop: {self.is_looping}
host: {self.host}"""
