# Created by quangkhanh at 02/01/2021
# File: status_manager.py

from abc import ABCMeta, abstractmethod

from synchronization.synchronizer.status_synchronizer import StatusSynchronizer


class StatusManager(metaclass=ABCMeta):

    _status_synchronizer: StatusSynchronizer

    def start_synchronizing(self):
        self._status_synchronizer.start()
