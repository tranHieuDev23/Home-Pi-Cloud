# Created by quangkhanh at 02/01/2021
# File: hivemq_publisher.py
from command_publisher.hivemq_connection_factory import HiveMQConnectionFactory
from command_publisher.publisher import Publisher


class HiveMQPublisher(Publisher):

    def __init__(self, host: str, port: int, username: str, password: str, topic: str):
        super(HiveMQPublisher, self).__init__()
        factory = HiveMQConnectionFactory(
            host, port, username, password, topic)
        self._connection = factory.create_connection()
