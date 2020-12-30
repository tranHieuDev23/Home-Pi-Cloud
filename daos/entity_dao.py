# author: Khanh.Quang 
# institute: Hanoi University of Science and Technology
# file name: entity_dao.py
# project name: Home-Pi-Cloud
# date: 30/12/2020

from abc import ABCMeta, abstractmethod


class EntityDAO(metaclass=ABCMeta):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def save(self, entity):
        pass

    @abstractmethod
    def delete(self, entity):
        pass
