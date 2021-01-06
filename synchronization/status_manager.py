# Created by quangkhanh at 02/01/2021
# File: status_manager.py
import threading
from abc import ABCMeta

from synchronization.synchronizer.status_synchronizer import StatusSynchronizer


class StatusManager(metaclass=ABCMeta):

    _status_synchronizer: StatusSynchronizer

    def start_synchronizing(self):
        sync = threading.Thread(target=self._status_synchronizer.start)
        sync.start()
