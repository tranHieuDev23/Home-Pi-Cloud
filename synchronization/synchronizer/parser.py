# Created by quangkhanh at 02/01/2021
# File: parser.py

from abc import ABCMeta, abstractmethod


class Parser(metaclass=ABCMeta):

    @abstractmethod
    def parse(self, content: str):
        pass
