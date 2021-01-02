# Created by quangkhanh at 02/01/2021
# File: device_status_sync.py
import time

from synchronization.fetcher.status_fetcher import StatusFetcher
from synchronization.retriever.database_retriever import DatabaseRetriever
from synchronization.synchronizer.status_parser import StatusParser

from synchronization.synchronizer.status_synchronizer import StatusSynchronizer


class DeviceStatusSync(StatusSynchronizer):

    def __init__(self, status_fetcher: StatusFetcher, data_retriever: DatabaseRetriever):
        super().__init__(status_fetcher, data_retriever)
        self._parser = StatusParser()
        self.__INTERVAL = 10

    def start(self) -> None:
        self._status_fetcher.start()
        while True:
            try:
                updated_data = self._status_fetcher.get_updated()
                while updated_data.has_next():
                    msg = updated_data.next()
                    print(msg)
                    info = self._parser.parse(msg)
                    self._database_retriever.update(info)
                time.sleep(self.__INTERVAL)
            except Exception as e:
                print(e.message)
