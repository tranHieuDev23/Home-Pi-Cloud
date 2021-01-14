# author: Khanh.Quang
# institute: Hanoi University of Science and Technology
# file name: device_dao.py
# project name: Home-Pi-Cloud
# date: 30/12/2020


from daos.psql_dao import PostgresDAO
from models.device import Device, DeviceType


def _make_device(row) -> Device:
    return Device(id=int(row[0]),
                  display_name=row[1],
                  type=DeviceType[row[2]],
                  owner=row[3])


class DeviceDAO(PostgresDAO):

    def get(self, key):
        command = f'''
        SELECT * FROM iot_db.devices where id = '{key}';
        '''
        row = self.connection.query(command)
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
        UPDATE iot_db.devices SET 
        display_name = '{device.display_name}',
        type = '{device.type.name}',
        of_user = '{device.owner}'
        WHERE id = '{device.id}';
        '''
        self.connection.update(command)

    def save(self, entity: Device):
        command = f'''
        INSERT INTO iot_db.devices (display_name, type, of_user) VALUES 
            ('{entity.display_name}', '{entity.type.name}', '{entity.owner}')
        RETURNING *;
        '''
        rows = self.connection.query(command)
        if (len(rows) == 0):
            return None
        return _make_device(rows[0])

    def delete(self, entity: Device):
        command = f'''
        DELETE FROM iot_db.devices WHERE id = {entity.id}       
        '''
        self.connection.update(command)
