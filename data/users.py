import datetime
import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    role = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    raiting = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    # bot = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    # bot_counter = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    documentation = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="/static/img/avatar_img/avatar_1.jpg")
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
