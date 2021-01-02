# Created by quangkhanh at 02/01/2021
# File: connection_factory.py

from abc import ABCMeta, abstractmethod

from broker_connection.connection import Connection


class ConnectionFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_connection(self) -> Connection:
        pass
