# author: Khanh.Quang
# institute: Hanoi University of Science and Technology
# file name: psql_connection_factory.py
# project name: Home-Pi-Cloud
# date: 30/12/2020

from os import getenv
from daos.connection.connection_factory import ConnectionFactory
from daos.connection.postgre_connection import PostgreConnection
from dotenv import load_dotenv
load_dotenv()


class PSQLConnectionFactory(ConnectionFactory):
    __user__ = getenv('POSTGRES_USER')
    __password__ = getenv('POSTGRES_PASSWORD')
    __database__ = getenv('POSTGRES_DB')
    __host__ = getenv('POSTGRES_HOST')
    __port__ = getenv('POSTGRES_PORT')
    __connection__ = None

    def get_connection(self):
        if PSQLConnectionFactory.__connection__ is None:
            PSQLConnectionFactory.__connection__ = PostgreConnection(host=PSQLConnectionFactory.__host__,
                                                                     port=PSQLConnectionFactory.__port__,
                                                                     database=PSQLConnectionFactory.__database__,
                                                                     user=PSQLConnectionFactory.__user__,
                                                                     password=PSQLConnectionFactory.__password__)
        return PSQLConnectionFactory.__connection__
