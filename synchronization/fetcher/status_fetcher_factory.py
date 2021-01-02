# Created by quangkhanh at 02/01/2021
# File: status_fetcher_factory.py

from abc import ABCMeta, abstractmethod

from synchronization.fetcher.status_fetcher import StatusFetcher


class StatusFetcherFactory(metaclass=ABCMeta):

    @abstractmethod
    def create_fetcher(self) -> StatusFetcher:
        pass
