from flask_login import UserMixin
from sqlalchemy import Column, Integer, String

from uls_app.extensions import db

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), index=True, unique=True)
    password = Column(String(512), nullable=False)
    userType = Column(String(50), nullable=False)

    def check_password(self, password):
        return password == self.password

    @property
    def is_admin(self):
        return self.userType == "admin"

    def __repr__(self):
        return "<User {}>".format(self.username)