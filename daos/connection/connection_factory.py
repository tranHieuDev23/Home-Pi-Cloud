# author: Khanh.Quang 
# institute: Hanoi University of Science and Technology
# file name: connection_factory.py
# project name: Home-Pi-Cloud
# date: 30/12/2020

from abc import ABCMeta, abstractmethod


class ConnectionFactory(metaclass=ABCMeta):

    @abstractmethod
    def get_connection(self):
        pass
