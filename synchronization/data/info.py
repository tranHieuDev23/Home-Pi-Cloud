# Created by quangkhanh at 02/01/2021
# File: info.py

class Info():
    __address: str
    __id: str
    __status: str

    def __init__(self, address: str, id: str, status: str):
        self.__address = address
        self.__id = id
        self.__status = status

    @property
    def address(self):
        return self.__address

    @property
    def id(self):
        return self.__id

    @property
    def status(self):
        return self.__status
