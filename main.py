from utils.json_helper import to_dict
from homepi.homepi_service import HomePiService
from models.user import User
from auth.auth_service import AuthService
from os import getenv
from flask import Flask, request, Request, Response
from http import HTTPStatus
import json
from dotenv import load_dotenv
load_dotenv()


def create_app():
    app = Flask(__name__)

    AUTH_COOKIE = 'HomePiAuth'
    AUTH_COOKIE_MAX_AGE = 30 * 24 * 60 * 60

    JWT_KEY = getenv('JWT_KEY')
    MQTT_HOST = getenv('MQTT_HOST')
    MQTT_PORT = int(getenv('MQTT_PORT'))
    MQTT_USERNAME = getenv('MQTT_USERNAME')
    MQTT_PASSWORD = getenv('MQTT_PASSWORD')

    auth_service = AuthService(JWT_KEY)
    home_pi_service = HomePiService(
        JWT_KEY, MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD)
    home_pi_service.init()

    def __get_jwt__(req: Request):
        try:
            jwt = req.cookies.get(AUTH_COOKIE)
            return jwt
        except:
            return None

    def __get_user__(req: Request):
        jwt = __get_jwt__(req)
        if (jwt is None):
            return None
        return auth_service.get_user_from_jwt(jwt)

    def __get_json_response__(response, status=HTTPStatus.OK):
        response_dict = to_dict(response)
        return Response(
            response=json.dumps(response_dict),
            status=status,
            content_type='application/json')

    def __append__auth__cookie__(response: Response, jwt: str):
        response.set_cookie(
            AUTH_COOKIE, jwt, max_age=AUTH_COOKIE_MAX_AGE, httponly=True)

    @app.route('/api/auth/validate', methods=['POST'])
    def validate():
        jwt = __get_jwt__(request)
        if (jwt is None):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        user = auth_service.validate_user(jwt)
        return __get_json_response__(user)

    @app.route('/api/auth/register', methods=['POST'])
    def register():
        request_json = request.get_json()
        if ('username' not in request_json or 'displayName' not in request_json or 'password' not in request_json):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        username = request_json['username']
        display_name = request_json['displayName']
        password = request_json['password']
        user = User(username, display_name, password)
        result = auth_service.register_user(user)
        if (result is None):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        new_user, jwt, status_topic = result
        home_pi_service.listen_user_topic(status_topic)
        response = __get_json_response__(new_user)
        __append__auth__cookie__(response, jwt)
        return response

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        request_json = request.get_json()
        if ('username' not in request_json or 'password' not in request_json):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        username = request_json['username']
        password = request_json['password']
        result = auth_service.login(username, password)
        if (result is None):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        user, jwt = result
        response = __get_json_response__(user)
        __append__auth__cookie__(response, jwt)
        return response

    @app.route('/api/auth/logout', methods=['POST'])
    def logout():
        jwt = __get_jwt__(request)
        if (jwt is None):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        auth_service.logout(jwt)
        response = __get_json_response__({})
        response.delete_cookie(AUTH_COOKIE)
        return response

    @app.route('/api/home-control/get-commanders', methods=['POST'])
    def get_commanders():
        user = __get_user__(request)
        if (user is None):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        commanders = home_pi_service.get_commanders(user.username)
        return __get_json_response__({'commanders': commanders})

    @app.route('/api/home-control/register-commander', methods=['POST'])
    def register_commander():
        user = __get_user__(request)
        if (user is None):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        request_json = request.get_json()
        if ('commanderId' not in request_json):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        commander_id = request_json['commanderId']
        result = home_pi_service.register_commander(
            commander_id, user.username)
        if (result is None):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        commander, jwt = result
        return __get_json_response__({
            'commander': commander,
            'token': jwt
        })

    @app.route('/api/home-control/validate-commander', methods=['POST'])
    def validate_commander():
        request_json = request.get_json()
        if ('token' not in request_json):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        jwt = request_json['token']
        result = home_pi_service.validate_commander(jwt)
        if (result is None):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        _, username = result
        commander_jwt = auth_service.get_jwt_from_username(username)
        return __get_json_response__({
            'newToken': commander_jwt
        })

    @app.route('/api/home-control/rename-commander', methods=['POST'])
    def rename_commander():
        user = __get_user__(request)
        if (user is None):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        request_json = request.get_json()
        if ('commanderId' not in request_json or 'newName' not in request_json):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        commander_id = request_json['commanderId']
        new_name = request_json['newName']
        result = home_pi_service.rename_commander(
            commander_id, user.username, new_name)
        if (result is None):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        commander = result
        return __get_json_response__({
            'commander': commander
        })

    @app.route('/api/home-control/unregister-commander', methods=['POST'])
    def unregister_commander():
        user = __get_user__(request)
        if (user is None):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        request_json = request.get_json()
        if ('commanderId' not in request_json):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        commander_id = request_json['commanderId']
        result = home_pi_service.unregister_commander(
            commander_id, user.username)
        if (result is None):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        return __get_json_response__({})

    @app.route('/api/home-control/get-devices', methods=['POST'])
    def get_devices():
        user = __get_user__(request)
        if (user is None):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        devices = home_pi_service.get_devices(user.username)
        return __get_json_response__({'devices': devices})

    @app.route('/api/home-control/register-device', methods=['POST'])
    def register_device():
        user = __get_user__(request)
        if (user is None):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        request_json = request.get_json()
        if ('deviceId' not in request_json):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        device_id = request_json['deviceId']
        result = home_pi_service.register_device(
            device_id, user.username)
        if (result is None):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        device, jwt = result
        return __get_json_response__({
            'device': device,
            'token': jwt
        })

    @app.route('/api/home-control/validate-device', methods=['POST'])
    def validate_device():
        request_json = request.get_json()
        if ('token' not in request_json):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        jwt = request_json['token']
        result = home_pi_service.validate_device(jwt)
        if (result is None):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        _, command_topic, status_topic = result
        response = __get_json_response__({
            'broker': 'broker.hivemq.com',
            'port': 1883,
            'commandTopic': command_topic,
            'statusTopic': status_topic
        })
        return response

    @app.route('/api/home-control/rename-device', methods=['POST'])
    def rename_device():
        user = __get_user__(request)
        if (user is None):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        request_json = request.get_json()
        if ('deviceId' not in request_json or 'newName' not in request_json):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        device_id = request_json['deviceId']
        new_name = request_json['newName']
        result = home_pi_service.rename_device(
            device_id, user.username, new_name)
        if (result is None):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        device = result
        return __get_json_response__({
            'device': device
        })

    @app.route('/api/home-control/unregister-device', methods=['POST'])
    def unregister_device():
        user = __get_user__(request)
        if (user is None):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        request_json = request.get_json()
        if ('deviceId' not in request_json):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        device_id = request_json['deviceId']
        result = home_pi_service.unregister_device(
            device_id, user.username)
        if (result is None):
            return __get_json_response__({}, HTTPStatus.BAD_REQUEST)
        return __get_json_response__({})

    @app.route('/api/home-control/issue-command', methods=['POST'])
    def issue_command():
        request_json = request.get_json()
        if ('token' not in request_json or 'deviceName' not in request_json or 'command' not in request_json or 'params' not in request_json):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        jwt = request_json['token']
        user = auth_service.get_user_from_jwt(jwt)
        device_name = request_json['deviceName']
        command = request_json['command']
        params = request_json['params']
        target_device = home_pi_service.issue_command(
            device_name, user, command, params)
        if (target_device is None):
            return __get_json_response__({
                'success': False
            })
        return __get_json_response__({
            'success': True,
            'target': target_device
        })

    @app.route('/api/home-control/get-status', methods=['POST'])
    def get_status():
        request_json = request.get_json()
        if ('token' not in request_json or 'deviceName' not in request_json or 'fieldNames' not in request_json):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
        jwt = request_json['token']
        user = auth_service.get_user_from_jwt(jwt)
        device_name = request_json['deviceName']
        field_names = request_json['fieldNames']
        field_values = home_pi_service.get_status(
            device_name, user.username, field_names)
        if (field_values is None):
            return __get_json_response__({
                'success': False
            })
        return __get_json_response__({
            'success': True,
            'fieldValues': field_values
        })

    return app
