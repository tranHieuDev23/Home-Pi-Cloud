# Created by quangkhanh at 02/01/2021
# File: status_iterator.py

from synchronization.data.iterator import Iterator

from typing import List


class StatusIterator(Iterator):

    __index: int
    __status: list

    def __init__(self, status: List[str]):
        # print(len(status))
        self.__status = status
        self.__index = -1

    def has_next(self) -> bool:
        if self.__index < len(self.__status) - 1 and len(self.__status) > 0:
            return True
        else:
            return False

    def next(self) -> str:
        self.__index += 1
        return self.__status[self.__index]

