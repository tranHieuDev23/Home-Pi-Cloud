# Created by quangkhanh at 02/01/2021
# File: database_retriever.py

from abc import ABCMeta, abstractmethod

from synchronization.data.info import Info


class DatabaseRetriever(metaclass=ABCMeta):

    @abstractmethod
    def update(self, info: Info) -> None:
        pass
