# author: Khanh.Quang
# institute: Hanoi University of Science and Technology
# file name: commander_dao.py
# project name: Home-Pi-Cloud
# date: 30/12/2020

from uuid import uuid4
from daos.psql_dao import PostgresDAO
from models.commander import Commander


def _make_commander(row) -> Commander:
    return Commander(id=row[0], display_name=row[1], owner=row[2])


class CommanderDAO(PostgresDAO):

    def get(self, key):
        command = f'''
        SELECT * FROM iot_db.commanders WHERE id = %s;
        '''
        row = self.connection.query(command, (key,))
        if len(row) > 0:
            return _make_commander(row[0])
        else:
            return None

    def get_all(self):
        command = f'''
        SELECT * FROM iot_db.commanders;
        '''
        rows = self.connection.query(command)
        return [_make_commander(row) for row in rows]

    def update(self, entity: Commander):
        command = f'''
        UPDATE iot_db.commanders SET 
            display_name = %s, of_user = %s
            WHERE id = %s;
        '''
        self.connection.update(
            command, (entity.displayName, entity.owner, entity.id))

    def save(self, entity: Commander):
        entity.id = uuid4()
        command = f'''
        INSERT INTO iot_db.commanders(id, display_name, of_user) VALUES (%s, %s, %s)
            RETURNING *;
        '''
        rows = self.connection.query(
            command, (entity.id, entity.displayName, entity.owner))
        if len(rows) == 0:
            return None
        return _make_commander(rows[0])

    def delete(self, entity: Commander):
        command = f'''
        DELETE FROM iot_db.commanders WHERE id = %s;
        '''
        self.connection.update(command, (entity.id,))

    def get_of_user(self, username: str):
        command = f'''
        SELECT * FROM iot_db.commanders WHERE of_user = %s;
        '''
        rows = self.connection.query(command, (username,))
        return [_make_commander(row) for row in rows]
