# Created by quangkhanh at 02/01/2021
# File: device_status_fetcher.py
from synchronization.data.iterator import Iterator
from synchronization.data.repository import Repository
from synchronization.data.status_repository import StatusRepository
from synchronization.fetcher.status_fetcher import StatusFetcher

from paho.mqtt.client import Client
import threading


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


class DeviceStatusFetcher(StatusFetcher):

    __status_repo: Repository
    __client: Client

    def __init__(self, username: str, password: str, host: str, port: int, topic: str):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__topic = topic
        self.__status_repo = StatusRepository()

    def __on_message(self, client, userdata, msg):
        status = msg.payload.decode('ascii')
        self.__status_repo.add(status)

    def start(self) -> None:
        self.__client = Client()
        self.__client.on_subscribe = on_subscribe
        self.__client.on_message = self.__on_message
        self.__client.connect(self.__host, self.__port)
        self.__client.subscribe(self.__topic, qos=2)
        sync = threading.Thread(target=self.__client.loop_forever)
        sync.start()

    def get_updated(self) -> Iterator:
        return self.__status_repo.get_iterator()
