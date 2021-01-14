# Created by quangkhanh at 02/01/2021
# File: hivemq_connection_factory.py

from command_publisher.hivemq_connection import HiveMQConnection
from command_publisher.connection import Connection
from command_publisher.connection_factory import ConnectionFactory


class HiveMQConnectionFactory(ConnectionFactory):

    def __init__(self, host, port, username, password, topic):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.topic = topic

    def create_connection(self) -> Connection:
        return HiveMQConnection(
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            topic=self.topic
        )
