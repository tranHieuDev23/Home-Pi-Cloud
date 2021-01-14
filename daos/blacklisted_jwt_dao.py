# author: Khanh.Quang
# institute: Hanoi University of Science and Technology
# file name: customer_dao.py
# project name: Home-Pi-Cloud
# date: 30/12/2020

from daos.psql_dao import PostgresDAO


class BlacklistedJwtDAO(PostgresDAO):

    def __init__(self):
        super().__init__()

    def get(self, jti):
        # select customer from database
        customer_command = f'''
        SELECT * FROM iot_db.blacklisted_jwts WHERE jti = %s;
        '''
        rows = self.connection.query(customer_command, (jti,))
        if len(rows) < 1:
            return None
        jti = rows[0][0]
        exp = rows[0][1]
        return jti, exp

    def get_all(self):
        command = '''
        SELECT * FROM iot_db.blacklisted_jwts;
        '''
        rows = self.connection.query(command)
        return [(row[0], row[1]) for row in rows]

    def update(self, jwt):
        pass

    def save(self, jwt):
        jti, exp = jwt
        command = f'''
        INSERT INTO iot_db.blacklisted_jwts VALUES (%s, %s);
        '''
        self.connection.update(command, (jti, exp))

    def delete(self, jwt):
        pass

    def is_blacklisted(self, jti):
        return self.get(jti) is not None
