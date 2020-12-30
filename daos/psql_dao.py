# author: Khanh.Quang 
# institute: Hanoi University of Science and Technology
# file name: psql_dao.py
# project name: Home-Pi-Cloud
# date: 30/12/2020

from daos.entity_dao import EntityDAO
from daos.connection.psql_connection_factory import PSQLConnectionFactory

from abc import ABCMeta


class PostgresDAO(EntityDAO, metaclass=ABCMeta):

    def __init__(self):
        self.connection = PSQLConnectionFactory().get_connection()