# Created by quangkhanh at 02/01/2021
# File: hivemq_connection_factory.py

from broker_connection.hivemq_connection import HiveMQConnection
from broker_connection.connection import Connection
from broker_connection.connection_factory import ConnectionFactory


class HiveMQConnectionFactory(ConnectionFactory):

    def __init__(self, username, password, topic):
        self.__username = username
        self.__password = password
        self.__topic = topic
        self.__host = "localhost"
        self.__port = 1883

    def create_connection(self) -> Connection:
        return HiveMQConnection(
            username=self.__username,
            password=self.__password,
            host=self.__host,
            port=self.__port,
            topic=self.__topic
        )
