from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from .. import db
from .Model import Model


class User(db.Model, UserMixin, Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hashed = db.Column(db.String(255), nullable=False)

    lists = db.relationship("List", back_populates="user")

    def __init__(self, username, password_plaintext):
        self.username = username
        self.set_password(password_plaintext)

    def set_password(self, password_plaintext):
        if not password_plaintext:
            raise AssertionError("Password Missing")

        self.password_hashed = generate_password_hash(password_plaintext)

    def is_password_correct(self, password_plaintext):
        return check_password_hash(self.password_hashed, password_plaintext)
