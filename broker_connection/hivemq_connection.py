# Created by quangkhanh at 02/01/2021
# File: hivemq_connection.py
import paho.mqtt.client as paho
from paho.mqtt.client import Client

from broker_connection.connection import Connection


def _on_publish(client, user_data, mid):
    print("Published message!")


class HiveMQConnection(Connection):
    __client: Client
    __username: str
    __password: str
    __topic: str
    __qos: int

    def __init__(self, username: str, password: str, host: str, port: int, topic: str):
        client = paho.Client()
        client.on_publish = _on_publish
        client.connect(host=host, port=int(port))
        client.loop_start()
        self.__client = client
        self.__username = username
        self.__password = password
        self.__topic = topic
        self.__qos = 2

    def publish(self, content: str) -> None:
        self.__client.publish(topic=self.__topic, payload=content, qos=self.__qos)
