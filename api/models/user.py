from api import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    """
    Represents a user in the DB
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f'<User id={self.id}, email={self.email}>'

class AppleUser(db.Model):
    """
    Maps an apple user identifier to a user in the DB
    """
    __tablename__ = 'apple_users'

    id = db.Column(db.Integer, primary_key=True)
    apple_id = db.Column(db.String(255), index=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='apple_user')

    def __repr__(self):
        return f'<AppleUser id={self.id}, apple_id={self.apple_id}, user_id={self.user_id}>'