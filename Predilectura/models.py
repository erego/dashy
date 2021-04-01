from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    def __init__(self, name, email, password, is_admin=False):
        self.id = None
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def set_id(self, id_user):
        self.id = id_user

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_json(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "is_admin": self.is_admin
        }

    def __repr__(self):
        return '<User {}>'.format(self.email)

