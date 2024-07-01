from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp.db'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in your code!
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    # with app.app_context():
    #     db.create_all()
    return app
