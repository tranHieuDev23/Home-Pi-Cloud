# author: Khanh.Quang
# institute: Hanoi University of Science and Technology
# file name: device_dao.py
# project name: Home-Pi-Cloud
# date: 30/12/2020


from uuid import uuid4
from daos.psql_dao import PostgresDAO
from models.device import Device, DeviceType


def _make_device(row) -> Device:
    return Device(id=row[0],
                  displayName=row[1],
                  type=DeviceType[row[2]],
                  owner=row[3])


class DeviceDAO(PostgresDAO):

    def get(self, key):
        command = f'''
        SELECT * FROM iot_db.devices WHERE id = %s;
        '''
        row = self.connection.query(command, (key,))
        if row.__len__() > 0:
            return _make_device(row[0])
        else:
            return None

    def get_all(self):
        command = f'''
        SELECT * FROM iot_db.devices; 
        '''
        rows = self.connection.query(command)
        return [_make_device(row) for row in rows]

    def update(self, device: Device):
        command = f'''
        UPDATE iot_db.devices
            SET display_name = %s, type = %s, of_user = %s
            WHERE id = %s;
        '''
        self.connection.update(
            command, (device.displayName, device.type.name, device.owner, device.id))

    def save(self, entity: Device):
        entity.id = uuid4()
        command = f'''
        INSERT INTO iot_db.devices (id, display_name, type, of_user) VALUES (%s, %s, %s, %s)
            RETURNING *;
        '''
        rows = self.connection.query(
            command, (entity.id, entity.displayName, entity.type.name, entity.owner))
        if (len(rows) == 0):
            return None
        return _make_device(rows[0])

    def delete(self, entity: Device):
        command = f'''
        DELETE FROM iot_db.devices WHERE id = %s
        '''
        self.connection.update(command, (entity.id,))

    def get_of_user(self, username: str):
        command = f'''
        SELECT * FROM iot_db.devices WHERE of_user = %s;
        '''
        rows = self.connection.query(command, (username,))
        return [_make_device(row) for row in rows]
