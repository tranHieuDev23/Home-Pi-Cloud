# Created by quangkhanh at 02/01/2021
# File: device_status_fetcher_factory.py
from synchronization.fetcher.device_status_fetcher import DeviceStatusFetcher
from synchronization.fetcher.status_fetcher import StatusFetcher
from synchronization.fetcher.status_fetcher_factory import StatusFetcherFactory


class DeviceStatusFetcherFactory(StatusFetcherFactory):

    def __init__(self, username: str, password: str, topic: str):
        self.__username = username
        self.__password = password
        self.__topic = topic
        self.__host = "localhost"
        self.__port = 1883

    def create_fetcher(self) -> StatusFetcher:
        return DeviceStatusFetcher(
            self.__username,
            self.__password,
            self.__host,
            self.__port,
            self.__topic
        )
