from uuid import uuid4
from daos.psql_dao import PostgresDAO
from models.status_log import StatusLog


def _make_status_log(row) -> StatusLog:
    return StatusLog(row[0], row[1], row[2], row[3], row[4])


class StatusLogDAO(PostgresDAO):

    def get(self, id):
        command = f'''
        SELECT * FROM iot_db.status_logs WHERE id = %s;
        '''
        row = self.connection.query(command, (id,))
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
        pass

    def save(self, status_log: StatusLog):
        status_log.id = uuid4()
        command = f'''
        INSERT INTO iot_db.status_logs VALUES (%s, %s, %s, %s, %s) 
            RETURNING *;
        '''
        rows = self.connection.query(command, (status_log.id, status_log.ofDevice,
                                               status_log.timestamp, status_log.fieldName, status_log.fieldValue))
        if (len(rows) == 0):
            return None
        return _make_status_log(rows[0])

    def delete(self, id: str):
        command = f'''
        DELETE FROM iot_db.status_logs WHERE id = %s;
        '''
        self.connection.update(command, (id,))
