# Created by quangkhanh at 02/01/2021
# File: status_repository.py
from synchronization.data.iterator import Iterator
from synchronization.data.repository import Repository
from synchronization.data.status_iterator import StatusIterator

import threading


class StatusRepository(Repository):

    __status: list

    def __init__(self):
        self.__status = []
        self.__sem = threading.Semaphore()

    def get_iterator(self) -> Iterator:
        iterator = StatusIterator(self.__status.copy())
        self.clean()
        return iterator

    def add(self, status: str) -> None:
        self.__status.append(status)

    def clean(self):
        self.__sem.acquire()
        self.__status = []
        self.__sem.release()
