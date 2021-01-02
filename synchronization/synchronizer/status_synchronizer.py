# Created by quangkhanh at 02/01/2021
# File: status_synchronizer.py

from abc import ABCMeta, abstractmethod

from synchronization.fetcher.status_fetcher import StatusFetcher
from synchronization.retriever.database_retriever import DatabaseRetriever
from synchronization.synchronizer.parser import Parser


class StatusSynchronizer(metaclass=ABCMeta):

    _parser: Parser
    _status_fetcher: StatusFetcher
    _database_retriever: DatabaseRetriever

    def __init__(self, status_fetcher: StatusFetcher, data_retriever: DatabaseRetriever):
        self._status_fetcher = status_fetcher
        self._database_retriever = data_retriever

    @abstractmethod
    def start(self) -> None:
        pass
