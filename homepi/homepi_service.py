from datetime import datetime, timedelta
from uuid import uuid4
from jwt.jwk import OctetJWK
from jwt.jwt import JWT
from jwt.utils import get_int_from_datetime
from daos.blacklisted_jwt_dao import BlacklistedJwtDAO
from models.commander import Commander
from daos.commander_dao import CommanderDAO
from daos.device_dao import DeviceDAO
from daos.status_log_dao import StatusLogDAO


class HomePiService:
    def __init__(self, jwt_key: str):
        self.__commander_dao = CommanderDAO()
        self.__device_dao = DeviceDAO()
        self.__log_dao = StatusLogDAO()
        self.__jwt_dao = BlacklistedJwtDAO()
        self.__jwt = JWT()
        self.__jwt_key = OctetJWK(jwt_key.encode())

    def __parse_jwt(self, jwt: str):
        try:
            decoded_message = self.__jwt.decode(
                jwt, self.__jwt_key, do_time_check=True)
            jti = decoded_message['jti']
            if (self.__jwt_dao.is_blacklisted(jti)):
                return None
            exp = decoded_message['exp']
            username = decoded_message['sub']
            device_id = decoded_message['did']
            return jti, exp, username, device_id
        except:
            return None

    def __get_jwt_from_username_and_id(self, username: str, device_id: str):
        jwt = self.__jwt.encode({
            'jti': str(uuid4()),
            'sub': username,
            'did': device_id,
            'exp': get_int_from_datetime(
                datetime.now() + timedelta(minutes=1)
            )
        }, self.__jwt_key)
        return jwt

    def get_commanders(self, of_username: str):
        return self.__commander_dao.get_of_user(of_username)

    def register_commander(self, commander_id: str, of_username: str):
        commander = self.__commander_dao.get(commander_id)
        if (commander is None or commander.owner is not None):
            return None
        commander.owner = of_username
        jwt = self.__get_jwt_from_username_and_id(of_username, commander.id)
        return commander, jwt

    def validate_commander(self, jwt: str):
        result = self.__parse_jwt(jwt)
        if (result is None):
            return None
        jti, exp, username, commander_id = result
        commander = self.__commander_dao.get(commander_id)
        if (commander is None or commander.owner is not None):
            return None
        commander.owner = username
        self.__commander_dao.update(commander)
        self.__jwt_dao.save((jti, exp))
        return commander

    def rename_commander(self, commander_id: str, of_username: str, new_name: str):
        commander = self.__commander_dao.get(commander_id)
        if (commander is None or commander.owner != of_username):
            return None
        commander.displayName = new_name
        self.__commander_dao.update(commander)
        return commander

    def unregister_commander(self, commander_id: str, of_username: str):
        commander = self.__commander_dao.get(commander_id)
        if (commander is None or commander.owner != of_username):
            return None
        commander.owner = None
        self.__commander_dao.update(commander)
        return commander

    def get_devices():
        pass

    def register_device():
        pass

    def rename_device():
        pass

    def unregister_device():
        pass

    def validate_device():
        pass

    def issue_command():
        pass

    def get_status():
        pass
