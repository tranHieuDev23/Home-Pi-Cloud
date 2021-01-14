import json
from threading import Thread
from datetime import datetime, timedelta
from models.device import is_supported_command
from uuid import uuid4
from jwt.jwk import OctetJWK
from jwt.jwt import JWT
from jwt.utils import get_int_from_datetime
from Levenshtein.StringMatcher import StringMatcher
from models.user import User
from daos.blacklisted_jwt_dao import BlacklistedJwtDAO
from daos.user_dao import UserDAO
from daos.commander_dao import CommanderDAO
from daos.device_dao import DeviceDAO
from daos.status_log_dao import StatusLogDAO
from broker_connection.hivemq_publisher import HiveMQPublisher
from utils.json_helper import to_dict


class PublisherThread(Thread):
    def __init__(self, host, port, username, password, topic, message):
        super().__init__()
        self.__publisher = HiveMQPublisher(
            host, port, username, password, topic)
        self.__message = message

    def run(self):
        self.__publisher.publish(self.__message)


class HomePiService:
    def __init__(self, params):
        (jwt_key, mqtt_host, mqtt_port, mqtt_username, mqtt_password) = params
        self.__user_dao = UserDAO()
        self.__commander_dao = CommanderDAO()
        self.__device_dao = DeviceDAO()
        self.__log_dao = StatusLogDAO()
        self.__jwt_dao = BlacklistedJwtDAO()
        self.__jwt = JWT()
        self.__jwt_key = OctetJWK(jwt_key.encode())
        self.__mqtt_host = mqtt_host
        self.__mqtt_port = mqtt_port
        self.__mqtt_username = mqtt_username
        self.__mqtt_password = mqtt_password

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
        return commander, username

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

    def get_devices(self, of_username: str):
        return self.__device_dao.get_of_user(of_username)

    def register_device(self, device_id: str, of_username: str):
        device = self.__device_dao.get(device_id)
        if (device is None):
            return None
        device.owner = of_username
        jwt = self.__get_jwt_from_username_and_id(of_username, device.id)
        return device, jwt

    def validate_device(self, jwt: str):
        result = self.__parse_jwt(jwt)
        if (result is None):
            return None
        jti, exp, username, device_id = result
        device = self.__device_dao.get(device_id)
        if (device is None or device.owner is not None):
            return None
        device.owner = username
        self.__device_dao.update(device)
        self.__jwt_dao.save((jti, exp))
        user = self.__user_dao.get(username)
        return device, user.commandTopic, user.statusTopic

    def rename_device(self, device_id: str, of_username: str, new_name: str):
        device = self.__device_dao.get(device_id)
        if (device is None or device.owner != of_username):
            return None
        device.displayName = new_name
        self.__device_dao.update(device)
        return device

    def unregister_device(self, device_id: str, of_username: str):
        device = self.__device_dao.get(device_id)
        if (device is None or device.owner != of_username):
            return None
        device.owner = None
        self.__device_dao.update(device)
        return device

    def issue_command(self, device_name: str, of_user: User, command: str, params: dict):
        device_name = device_name.strip().lower()
        command = command.strip()
        if (len(device_name) == 0 or len(command) == 0):
            return None

        devices = self.__device_dao.get_of_user(of_user.username)
        if (len(devices) == 0):
            return None

        distances = [
            StringMatcher(seq1=device_name,
                          seq2=item.displayName.strip().lower()).distance()
            for item in devices
        ]
        min_distance = min(distances)
        if (min_distance > 0.2 * len(device_name)):
            return None
        min_index = distances.index(min_distance)

        device = devices[min_index]
        if (not is_supported_command(device.type, command)):
            return None

        command_topic = of_user.commandTopic
        mqtt_message = json.dumps(to_dict({
            'deviceId': device.id,
            'command': command,
            'params': params
        }))
        print(mqtt_message)
        PublisherThread(
            self.__mqtt_host,
            self.__mqtt_port,
            self.__mqtt_username,
            self.__mqtt_password,
            command_topic,
            mqtt_message
        ).start()

        return device

    def get_status():
        pass
