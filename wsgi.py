from api import create_app
from api.routes.user import user
from api.routes.auth import auth
from flask import request

app = create_app()

# Configure blueprint routes
app.register_blueprint(auth)
app.register_blueprint(user)


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


if __name__ == '__main__':
    app.run(port=8000, debug=True)
