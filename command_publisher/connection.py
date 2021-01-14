# Created by quangkhanh at 02/01/2021
# File: connection.py

from abc import ABCMeta, abstractmethod


class Connection(metaclass=ABCMeta):
    @abstractmethod
    def publish(self, content: str):
        pass
