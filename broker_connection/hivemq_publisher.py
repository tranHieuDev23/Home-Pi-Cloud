# Created by quangkhanh at 02/01/2021
# File: hivemq_publisher.py
from broker_connection.hivemq_connection_factory import HiveMQConnectionFactory
from broker_connection.publisher import Publisher


class HiveMQPublisher(Publisher):

    def __init__(self, host: str, port: int, username: str, password: str, topic: str):
        super(HiveMQPublisher, self).__init__()
        factory = HiveMQConnectionFactory(
            host, port, username, password, topic)
        self._connection = factory.create_connection()
