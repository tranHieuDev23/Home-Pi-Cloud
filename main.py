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

    auth_service = AuthService(JWT_KEY)

    def __get_jwt__(req: Request):
        try:
            jwt = req.cookies.get(AUTH_COOKIE)
            return jwt
        except:
            return None

    def __get_json_response__(response, status=HTTPStatus.OK):
        if (isinstance(response, dict)):
            response_dict = response
        else:
            response_dict = dict()
            for key in response.__dict__:
                value = response.__dict__[key]
                if (value is not None):
                    response_dict[key] = value
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
        if (user is None):
            return __get_json_response__({}, HTTPStatus.FORBIDDEN)
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
        new_user, jwt = result
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
        pass

    @app.route('/api/home-control/register-commander', methods=['POST'])
    def register_commanders():
        pass

    @app.route('/api/home-control/rename-commander', methods=['POST'])
    def rename_commander():
        pass

    @app.route('/api/home-control/unregister-commander', methods=['POST'])
    def unregister_commanders():
        pass

    @app.route('/api/home-control/get-devices', methods=['POST'])
    def get_devices():
        pass

    @app.route('/api/home-control/register-device', methods=['POST'])
    def register_device():
        pass

    @app.route('/api/home-control/rename-device', methods=['POST'])
    def rename_device():
        pass

    @app.route('/api/home-control/unregister-device', methods=['POST'])
    def unregister_device():
        pass

    @app.route('/api/home-control/validate-commander', methods=['POST'])
    def validate_commander():
        pass

    @app.route('/api/home-control/validate-device', methods=['POST'])
    def validate_device():
        pass

    @app.route('/api/home-control/issue-command', methods=['POST'])
    def issue_command():
        pass

    @app.route('/api/home-control/get-status', methods=['POST'])
    def get_status():
        pass

    return app
