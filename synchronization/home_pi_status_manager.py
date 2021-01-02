# Created by quangkhanh at 02/01/2021
# File: home_pi_status_manager.py
from synchronization.fetcher.device_status_fetcher import DeviceStatusFetcher
from synchronization.fetcher.device_status_fetcher_factory import DeviceStatusFetcherFactory
from synchronization.retriever.psql_retriever_factory import PSQLRetrieverFactory
from synchronization.status_manager import StatusManager
from synchronization.synchronizer.device_status_sync import DeviceStatusSync


class HomePiStatusManager(StatusManager):

    def __init__(self, username: str, password: str, topic: str):
        host = "localhost"
        port = 1883
        status_fetcher = DeviceStatusFetcherFactory(username, password, topic).create_fetcher()
        data_retriever = PSQLRetrieverFactory().create_database_retriever()
        self._status_synchronizer = DeviceStatusSync(status_fetcher, data_retriever)
