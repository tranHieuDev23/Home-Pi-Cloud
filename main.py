from flask import Flask, request


def create_app():
    app = Flask(__name__)

    @app.route('/api/auth/validate', methods=['POST'])
    def validate():
        pass

    @app.route('/api/auth/register', methods=['POST'])
    def register():
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
    def register_commanders():
        pass

    @app.route('/api/home-control/rename-commander', methods='POST')
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

    @app.route('/api/home-control/rename-device', methods='POST')
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
