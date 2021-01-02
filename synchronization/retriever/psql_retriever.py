# Created by quangkhanh at 02/01/2021
# File: psql_retriever.py
from daos.connection.psql_connection_factory import PSQLConnectionFactory
from synchronization.data.info import Info
from synchronization.retriever.database_retriever import DatabaseRetriever


class PSQLRetriever(DatabaseRetriever):

    def __init__(self):
        self.__connection = PSQLConnectionFactory().get_connection()

    def update(self, info: Info) -> None:
        print(info.status)
        command = f'''
        UPDATE {info.address} SET
        status = '{info.status}'
        WHERE id = {info.id};
        '''
        self.__connection.update(command)
