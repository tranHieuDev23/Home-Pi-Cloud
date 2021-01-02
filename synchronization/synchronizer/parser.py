# Created by quangkhanh at 02/01/2021
# File: parser.py

from abc import ABCMeta, abstractmethod

from synchronization.data.info import Info


class Parser(metaclass=ABCMeta):

    @abstractmethod
    def parse(self, content: str) -> Info:
        pass
