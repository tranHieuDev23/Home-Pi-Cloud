# Created by quangkhanh at 02/01/2021
# File: psql_retriever_factory.py

from synchronization.retriever.data_retriever_factory import DatabaseRetrieverFactory
from synchronization.retriever.database_retriever import DatabaseRetriever
from synchronization.retriever.psql_retriever import PSQLRetriever


class PSQLRetrieverFactory(DatabaseRetrieverFactory):

    def __int__(self):
        pass

    def create_database_retriever(self) -> DatabaseRetriever:
        return PSQLRetriever()