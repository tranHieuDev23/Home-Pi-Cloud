# author: Khanh.Quang 
# institute: Hanoi University of Science and Technology
# file name: psql_connection_factory.py
# project name: Home-Pi-Cloud
# date: 30/12/2020

from daos.connection.connection_factory import ConnectionFactory
from daos.connection.postgre_connection import PostgreConnection


class PSQLConnectionFactory(ConnectionFactory):
    __user__ = "guest"
    __password__ = "guest"
    __database__ = "iot"
    __host__ = "127.0.0.1"
    __port__ = "5432"
    __connection__ = None

    def get_connection(self):
        if PSQLConnectionFactory.__connection__ is None:
            PSQLConnectionFactory.__connection__ = PostgreConnection(host=PSQLConnectionFactory.__host__,
                                                                     port=PSQLConnectionFactory.__port__,
                                                                     database=PSQLConnectionFactory.__database__,
                                                                     user=PSQLConnectionFactory.__user__,
                                                                     password=PSQLConnectionFactory.__password__)
        return PSQLConnectionFactory.__connection__
