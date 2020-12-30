# author: Khanh.Quang 
# institute: Hanoi University of Science and Technology
# file name: commander_dao.py
# project name: Home-Pi-Cloud
# date: 30/12/2020

from daos.psql_dao import PostgresDAO
from models.commander import Commander


def _make_commander(row) -> Commander:
    return Commander(id=row[0], display_name=row[1], owner=row[2])


class CommanderDAO(PostgresDAO):

    def get(self, key):
        command = f'''
        SELECT * FROM iot_db.commander WHERE id = {key};
        '''
        row = self.connection.query(command)
        if len(row) > 0:
            return _make_commander(row[0])
        else:
            return None

    def get_all(self):
        command = f'''
        SELECT * FROM iot_db.commander
        '''
        rows = self.connection.query(command)
        return [_make_commander(row) for row in rows]

    def update(self, entity: Commander):
        command = f'''
        UPDATE iot_db.commander SET 
        display_name = '{entity.display_name}', customer = '{entity.owner}'
        WHERE id = {entity.id};
        '''
        self.connection.update(command)

    def save(self, entity: Commander):
        command = f'''
        INSERT INTO iot_db.commander(display_name, customer) VALUES 
        ('{entity.display_name}', '{entity.owner}');
        '''
        self.connection.update(command)
        get_command = f'''
        SELECT * FROM iot_db.commander WHERE
        display_name = '{entity.display_name}' AND customer = '{entity.owner}'
        '''
        row = self.connection.query(get_command)
        if len(row) > 0:
            return _make_commander(row[0])
        else:
            return None

    def delete(self, entity: Commander):
        command = f'''
        DELETE FROM iot_db.commander WHERE id = {entity.id};
        '''
        self.connection.update(command)