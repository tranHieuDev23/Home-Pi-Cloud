# Created by quangkhanh at 02/01/2021
# File: status_fetcher.py

from abc import ABCMeta, abstractmethod

from synchronization.data.iterator import Iterator


class StatusFetcher(metaclass=ABCMeta):

    @abstractmethod
    def get_updated(self) -> Iterator:
        pass

    @abstractmethod
    def start(self) -> None:
        pass
