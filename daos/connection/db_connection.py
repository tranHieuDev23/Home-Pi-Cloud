# author: Khanh.Quang 
# institute: Hanoi University of Science and Technology
# file name: db_connection.py
# project name: Home-Pi-Cloud
# date: 30/12/2020

from abc import ABCMeta, abstractmethod
from typing import List, Tuple


class DBConnection(metaclass=ABCMeta):

    @abstractmethod
    def query(self, command: str) -> List[Tuple]:
        pass

    @abstractmethod
    def update(self, command: str) -> None:
        pass

    @abstractmethod
    def close(self):
        pass
