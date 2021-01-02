# Created by quangkhanh at 02/01/2021
# File: repository.py

from abc import ABCMeta, abstractmethod

from synchronization.data.iterator import Iterator


class Repository(metaclass=ABCMeta):

    @abstractmethod
    def get_iterator(self) -> Iterator:
        pass

    @abstractmethod
    def add(self, status: str) -> None:
        pass
