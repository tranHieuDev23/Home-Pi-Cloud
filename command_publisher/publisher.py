# Created by quangkhanh at 02/01/2021
# File: publisher.py

from abc import ABCMeta

from command_publisher.connection import Connection


class Publisher(metaclass=ABCMeta):

    _connection: Connection

    def publish(self, content: str) -> None:
        """
        Publish a content to broker topic, you should configure specific host, topic when you create a Publisher
        instance containing a Connection

        :param content: commands or anything
        :type content: string
        :return: None
        :rtype: None
        """
        self._connection.publish(content)
