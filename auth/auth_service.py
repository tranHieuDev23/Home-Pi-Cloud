import re
from daos.blacklisted_jwt_dao import BlacklistedJwtDAO
from datetime import datetime, timedelta
from models.user import User
from jwt.jwt import JWT
from jwt.jwk import OctetJWK
from jwt.utils import get_int_from_datetime
from uuid import uuid4
from daos.user_dao import UserDAO
from utils.hash_helper import is_equal


class AuthService:
    def __init__(self, jwt_key: str):
        self.__user_dao = UserDAO()
        self.__jwt_dao = BlacklistedJwtDAO()
        self.__jwt = JWT()
        self.__jwt_key = OctetJWK(jwt_key.encode())
        self.__username_regex = '^[a-zA-Z0-9]{6,}$'
        self.__password_regex = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$'

    def __parse_jwt(self, jwt: str):
        try:
            decoded_message = self.__jwt.decode(
                jwt, self.__jwt_key, do_time_check=True)
            jti = decoded_message['jti']
            if (self.__jwt_dao.is_blacklisted(jti)):
                return None
            exp = decoded_message['exp']
            username = decoded_message['sub']
            return jti, exp, username
        except:
            return None

    def __clean_user_data(self, user: User):
        user.username = user.username.strip()
        user.displayName = user.displayName.strip()
        return user

    def __is_valid_user_data(self, user: User):
        if (not bool(re.match(self.__username_regex, user.username))):
            return False
        if (not bool(re.match(self.__password_regex, user.password))):
            return False
        if (len(user.displayName) == 0):
            return False
        return True

    def __clear_sensitive_user_data(self, user: User):
        user.password = None
        user.commandTopic = None
        user.statusTopic = None
        return user

    def __generate_topic_name(self, type: str):
        topic_name = str(uuid4())
        return f'homepi/{type}/{topic_name}'

    def get_user_from_jwt(self, jwt: str):
        result = self.__parse_jwt(jwt)
        if (result is None):
            return None
        _, _, username = result
        user = self.__user_dao.get(username)
        if (user is None):
            return None
        return user

    def get_jwt_from_username(self, username: str):
        jwt = self.__jwt.encode({
            'jti': str(uuid4()),
            'sub': username,
            'exp': get_int_from_datetime(
                datetime.now() + timedelta(days=30)
            )
        }, self.__jwt_key)
        return jwt

    def validate_user(self, jwt):
        user = self.get_user_from_jwt(jwt)
        if (user is None):
            return None
        user = self.__clear_sensitive_user_data(user)
        return user

    def register_user(self, user: User):
        user = self.__clean_user_data(user)
        if (not self.__is_valid_user_data(user)):
            return None
        user.commandTopic = self.__generate_topic_name('command')
        user.statusTopic = self.__generate_topic_name('status')
        new_user = self.__user_dao.save(user)
        if (new_user is None):
            return None
        new_user = self.__clear_sensitive_user_data(new_user)
        return new_user, self.get_jwt_from_username(new_user.username), user.statusTopic

    def login(self, username: str, password: str):
        user = self.__user_dao.get(username)
        if (user is None):
            return None
        if (not is_equal(password, user.password)):
            return None
        user = self.__clear_sensitive_user_data(user)
        jwt = self.get_jwt_from_username(username)
        return user, jwt

    def logout(self, jwt):
        jti, exp, _ = self.__parse_jwt(jwt)
        self.__jwt_dao.save((jti, exp))
