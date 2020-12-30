# author: Khanh.Quang 
# institute: Hanoi University of Science and Technology
# file name: customer_dao.py
# project name: Home-Pi-Cloud
# date: 30/12/2020

from daos.psql_dao import PostgresDAO
from models.customer import Customer
from models.device import Device
from models.commander import Commander


class CustomerDAO(PostgresDAO):

    def __init__(self):
        super().__init__()

    def get(self, key):
        # select customer from database
        customer_command = f'''
        SELECT * from iot_db.customer where name = '{key}';
        '''
        customer_rows = self.connection.query(customer_command)
        if len(customer_rows) < 1:
            return None
        customer_name=customer_rows[0][0]
        password=customer_rows[0][1]
        display_name=customer_rows[0][2]

        # select devices from data which are corresponding to the customer
        device_command = f'''
        SELECT * FROM iot_db.device where customer = '{customer_name}';
        '''
        device_rows = self.connection.query(device_command)
        devices = [Device(id=int(row[0]), display_name=row[1], type=row[2], owner=row[3], status=row[4])
                   for row in device_rows]

        # select commanders from data which are corresponding to the customer
        commander_command = f'''
        SELECT * FROM iot_db.commander where customer = '{customer_name}';
        '''
        commander_rows = self.connection.query(commander_command)
        commanders = [Commander(id=row[0], display_name=row[1], owner=row[2])
                      for row in commander_rows]

        return Customer(customer_name=customer_name,
                        password=password,
                        display_name=display_name,
                        devices=devices,
                        commanders=commanders)

    def get_all(self):
        command = '''
        SELECT name FROM iot_db.customer;
        '''
        rows = self.connection.query(command)
        return [self.get(row[0]) for row in rows]

    def update(self, entity: Customer):
        name = entity.customer_name
        password = entity.password
        display_name = entity.display_name
        command = f'''
        UPDATE iot_db.customer 
        SET password = '{password}', display_name = '{display_name}'
        WHERE name = '{name}';
        '''
        self.connection.update(command)

    def save(self, entity: Customer):
        command = f'''
        INSERT INTO iot_db.customer VALUES 
        ('{entity.customer_name}', '{entity.password}', '{entity.display_name}')
        '''
        self.connection.update(command)

    def delete(self, entity: Customer):
        command = f'''
        DELETE FROM iot_db.customer where name = '{entity.customer_name}'
        '''
        self.connection.update(command)
