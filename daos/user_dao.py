# author: Khanh.Quang
# institute: Hanoi University of Science and Technology
# file name: customer_dao.py
# project name: Home-Pi-Cloud
# date: 30/12/2020

from daos.psql_dao import PostgresDAO
from models.user import User
from utils.hash_helper import hash_message


class UserDAO(PostgresDAO):

    def __init__(self):
        super().__init__()

    def get(self, username):
        # select customer from database
        customer_command = f'''
        SELECT * FROM iot_db.users WHERE username = %s;
        '''
        rows = self.connection.query(customer_command, (username,))
        if len(rows) < 1:
            return None
        username = rows[0][0]
        password = rows[0][1]
        display_name = rows[0][2]
        return User(username, display_name, password)

    def get_all(self):
        command = '''
        SELECT * FROM iot_db.users;
        '''
        rows = self.connection.query(command)
        return [User(username=row[0], displayName=row[2]) for row in rows]

    def update(self, user: User):
        hashed_password = hash_message(user.password)
        command = f'''
        UPDATE iot_db.users
            SET password = %s, display_name = %s
            WHERE name = %s;
        '''
        self.connection.update(
            command, (hashed_password, user.displayName, user.username))

    def save(self, user: User):
        hashed_password = hash_message(user.password)
        command = f'''
        INSERT INTO iot_db.users VALUES (%s, %s, %s) RETURNING *;
        '''
        rows = self.connection.query(
            command, (user.username, hashed_password, user.displayName))
        if (len(rows) == 0):
            return None
        username = rows[0][0]
        display_name = rows[0][2]
        return User(username, display_name)

    def delete(self, user: User):
        command = f'''
        DELETE FROM iot_db.users WHERE username = %s
        '''
        self.connection.update(command, (user.username,))
