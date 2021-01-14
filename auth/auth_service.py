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

    def __is_blacklisted_jwt(self, jti):
        return self.__jwt_dao.get(jti) is not None

    def __parse_jwt(self, jwt: str):
        try:
            decoded_message = self.__jwt.decode(
                jwt, self.__jwt_key, do_time_check=True)
            jti = decoded_message['jti']
            if (self.__is_blacklisted_jwt(jti)):
                return None
            exp = decoded_message['exp']
            username = decoded_message['sub']
            return jti, exp, username
        except:
            return None

    def __get_jwt_from_username(self, username: str):
        jwt = self.__jwt.encode({
            'jti': str(uuid4()),
            'sub': username,
            'exp': get_int_from_datetime(
                datetime.now() + timedelta(days=30)
            )
        }, self.__jwt_key)
        return jwt

    def validate_user(self, jwt):
        result = self.__parse_jwt(jwt)
        if (result is None):
            return None
        _, _, username = result
        user = self.__user_dao.get(username)
        if (user is None):
            return None
        user.password = None
        return user

    def register_user(self, user: User):
        new_user = self.__user_dao.save(user)
        if (new_user is None):
            return None
        user.password = None
        return new_user, self.__get_jwt_from_username(new_user.username)

    def login(self, username: str, password: str):
        user = self.__user_dao.get(username)
        if (user is None):
            return None
        if (not is_equal(password, user.password)):
            return None
        user.password = None
        jwt = self.__get_jwt_from_username(username)
        return user, jwt

    def logout(self, jwt):
        jti, exp, _ = self.__parse_jwt(jwt)
        self.__jwt_dao.save((jti, exp))
