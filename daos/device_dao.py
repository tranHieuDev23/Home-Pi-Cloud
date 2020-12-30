# author: Khanh.Quang 
# institute: Hanoi University of Science and Technology
# file name: device_dao.py
# project name: Home-Pi-Cloud
# date: 30/12/2020


from daos.psql_dao import PostgresDAO
from models.device import Device


def _make_device(row) -> Device:
    return Device(id=int(row[0]),
                  display_name=row[1],
                  type=row[2],
                  owner=row[3],
                  status=row[4])


class DeviceDAO(PostgresDAO):

    def get(self, key):
        device_command = f'''
        SELECT * FROM iot_db.device where id = '{key}';
        '''
        row = self.connection.query(device_command)
        if row.__len__() > 0:
            return _make_device(row[0])
        else:
            return None

    def get_all(self):
        command = f'''
        SELECT * FROM iot_db.device; 
        '''
        rows = self.connection.query(command)
        return [_make_device(row) for row in rows]

    def update(self, entity: Device):
        command = f'''
        UPDATE iot_db.device SET 
        display_name = '{entity.display_name}',
        type = '{entity.type}',
        customer = '{entity.owner}',
        status = '{entity.status}'
        WHERE id = '{entity.id}';
        '''
        self.connection.update(command)

    def save(self, entity: Device):
        command = f'''
        INSERT INTO iot_db.device (display_name, type, customer, status) VALUES 
        ('{entity.display_name}', '{entity.type}', '{entity.owner}', '{entity.status}');
        '''
        self.connection.update(command)
        get_command = f'''
        SELECT * FROM iot_db.device 
        WHERE customer = '{entity.owner}' AND type = '{entity.type}' AND display_name = '{entity.display_name}';
        '''
        new_row = self.connection.query(get_command)
        return _make_device(new_row[0])
        
    def delete(self, entity: Device):
        command = f'''
        DELETE FROM iot_db.device WHERE id = {entity.id}       
        '''
        self.connection.update(command)
