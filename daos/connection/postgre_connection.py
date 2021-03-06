# author: Khanh.Quang
# institute: Hanoi University of Science and Technology
# file name: postgre_connection.py
# project name: Home-Pi-Cloud
# date: 30/12/2020
from typing import List, Tuple
import psycopg2

from daos.connection.db_connection import DBConnection


class PostgreConnection(DBConnection):

    def __init__(self,
                 host=None,
                 port=None,
                 database=None,
                 user=None,
                 password=None):
        try:
            self.con = psycopg2.connect(database=database,
                                        user=user,
                                        password=password,
                                        host=host,
                                        port=port)
        except Exception as e:
            print(e.message)

    def query(self, command: str, params=()) -> List[Tuple]:
        try:
            cur = self.con.cursor()
            cur.execute(command, params)
            self.con.commit()
            return cur.fetchall()
        except Exception as e:
            print(e.message)
            return []

    def update(self, command: str, params=()) -> None:
        try:
            cur = self.con.cursor()
            cur.execute(command, params)
            self.con.commit()
        except Exception as e:
            print(e.message)

    def close(self):
        self.con.close()
