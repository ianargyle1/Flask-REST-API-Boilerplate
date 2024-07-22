from api import create_app
from api.routes.user import user

app = create_app()

# Configure blueprint routes
app.register_blueprint(user)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
