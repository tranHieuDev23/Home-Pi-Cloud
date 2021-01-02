# Created by quangkhanh at 02/01/2021
# File: data_retriever_factory.py

from abc import ABCMeta, abstractmethod

from synchronization.retriever.database_retriever import DatabaseRetriever


class DatabaseRetrieverFactory(metaclass=ABCMeta):

    @abstractmethod
    def create_database_retriever(self) -> DatabaseRetriever:
        pass
