from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/api/auth/validate', methods=['POST'])
    def validate():
        pass

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        pass

    @app.route('/api/auth/logout', methods=['POST'])
    def logout():
        pass

    @app.route('/api/home-control/get-commanders', methods=['POST'])
    def get_commanders():
        pass

    @app.route('/api/home-control/register-commander', methods=['POST'])
    def get_commanders():
        pass

    @app.route('/api/home-control/rename-commander', methods='POST')
    def rename_commander():
        pass

    @app.route('/api/home-control/unregister-commander', methods=['POST'])
    def get_commanders():
        pass

    @app.route('/api/home-control/get-devices', methods=['POST'])
    def get_devices():
        pass

    @app.route('/api/home-control/register-device', methods=['POST'])
    def get_commanders():
        pass

    @app.route('/api/home-control/rename-device', methods='POST')
    def rename_device():
        pass

    @app.route('/api/home-control/unregister-device', methods=['POST'])
    def get_commanders():
        pass

    @app.route('/api/home-control/issue-command', methods=['POST'])
    def get_commanders():
        pass

    @app.route('/api/home-control/get-status', methods=['POST'])
    def get_commanders():
        pass

    return app
