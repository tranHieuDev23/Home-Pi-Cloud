# author: Khanh.Quang
# institute: Hanoi University of Science and Technology
# file name: customer_dao.py
# project name: Home-Pi-Cloud
# date: 30/12/2020

from daos.psql_dao import PostgresDAO
from models.user import User
from utils.hash_helper import hash_message


def _make_user(row):
    username = row[0]
    password = row[1]
    display_name = row[2]
    command_topic = row[3]
    status_topic = row[4]
    return User(username, display_name, password, command_topic, status_topic)


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
        return _make_user(rows[0])

    def get_all(self):
        command = '''
        SELECT * FROM iot_db.users;
        '''
        rows = self.connection.query(command)
        return [_make_user(row) for row in rows]

    def update(self, user: User):
        hashed_password = hash_message(user.password)
        command = f'''
        UPDATE iot_db.users
            SET password = %s, display_name = %s, command_topic = %s, status_topic = %s
            WHERE name = %s;
        '''
        self.connection.update(
            command, (hashed_password, user.displayName, user.username, user.commandTopic, user.statusTopic))

    def save(self, user: User):
        hashed_password = hash_message(user.password)
        command = f'''
        INSERT INTO iot_db.users VALUES (%s, %s, %s, %s, %s) RETURNING *;
        '''
        rows = self.connection.query(
            command, (user.username, hashed_password, user.displayName, user.commandTopic, user.statusTopic))
        if (len(rows) == 0):
            return None
        return _make_user(rows[0])

    def delete(self, user: User):
        command = f'''
        DELETE FROM iot_db.users WHERE username = %s
        '''
        self.connection.update(command, (user.username,))
