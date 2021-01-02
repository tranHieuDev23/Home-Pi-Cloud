# Created by quangkhanh at 02/01/2021
# File: iterator.py

from abc import ABCMeta, abstractmethod


class Iterator(metaclass=ABCMeta):

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> str:
        pass
