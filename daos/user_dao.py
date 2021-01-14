# author: Khanh.Quang
# institute: Hanoi University of Science and Technology
# file name: customer_dao.py
# project name: Home-Pi-Cloud
# date: 30/12/2020

from daos.psql_dao import PostgresDAO
from models.user import User
from utils.hash_helper import hash


class UserDAO(PostgresDAO):

    def __init__(self):
        super().__init__()

    def get(self, username):
        # select customer from database
        customer_command = f'''
        SELECT * from iot_db.users where username = '{username}';
        '''
        customer_rows = self.connection.query(customer_command)
        if len(customer_rows) < 1:
            return None
        username = customer_rows[0][0]
        display_name = customer_rows[0][2]
        return User(username, display_name)

    def get_all(self):
        command = '''
        SELECT * from FROM iot_db.users;
        '''
        rows = self.connection.query(command)
        return [User(username=row[0], display_name=row[2]) for row in rows]

    def update(self, user: User):
        hashed_password = hash(user.password)
        command = f'''
        UPDATE iot_db.users
        SET password = '{hashed_password}', display_name = '{user.display_name}'
        WHERE name = '{user.username}';
        '''
        self.connection.update(command)

    def save(self, user: User):
        command = f'''
        INSERT INTO iot_db.users VALUES 
        ('{user.username}', '{user.password}', '{user.display_name}')
        '''
        self.connection.update(command)

    def delete(self, user: User):
        command = f'''
        DELETE FROM iot_db.users where name = '{user.username}'
        '''
        self.connection.update(command)
