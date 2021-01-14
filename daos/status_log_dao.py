from daos.psql_dao import PostgresDAO
from models.status_log import StatusLog


def _make_status_log(row) -> StatusLog:
    return StatusLog(row[0], row[1], row[2], row[3], row[4])


class StatusLogDAO(PostgresDAO):

    def get(self, key):
        command = f'''
        SELECT * FROM iot_db.status_logs where id = '{key}';
        '''
        row = self.connection.query(command)
        if row.__len__() > 0:
            return _make_status_log(row[0])
        else:
            return None

    def get_all(self):
        command = f'''
        SELECT * FROM iot_db.status_logs; 
        '''
        rows = self.connection.query(command)
        return [_make_status_log(row) for row in rows]

    def update(self, entity: StatusLog):
        command = f'''
        UPDATE iot_db.status_logs SET 
        display_name = '{entity.display_name}',
        type = '{entity.type}',
        of_user = '{entity.owner}'
        WHERE id = '{entity.id}';
        '''
        self.connection.update(command)

    def save(self, status_log: StatusLog):
        command = f'''
        INSERT INTO iot_db.status_logs (of_device, timestamp, field_name, field_value) VALUES 
            ('{status_log.of_device}', '{status_log.timestamp}', '{status_log.field_name}', '{status_log.field_value}')
        RETURNING *;
        '''
        rows = self.connection.query(command)
        if (len(rows) == 0):
            return None
        return _make_status_log(rows[0])

    def delete(self, status_log: StatusLog):
        command = f'''
        DELETE FROM iot_db.status_logs WHERE id = {status_log.id}       
        '''
        self.connection.update(command)
