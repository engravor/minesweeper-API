from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, types, ForeignKey
from sqlalchemy.dialects import postgresql
from app import db
from datetime import datetime


class Board(db.Model):
    __tablename__ = 'boards'

    id = Column(types.Integer, primary_key=True)
    rows = Column(types.Integer, nullable=False)
    columns = Column(types.Integer, nullable=False)
    creation_date = Column(types.DateTime, nullable=False, default=datetime.utcnow)
    mines = Column(postgresql.JSON)
    current_game_state = Column(postgresql.JSON)

    owner_id = Column(types.Integer(), ForeignKey('users.id'), nullable=False)
    owner = db.relationship("User", backref='board', lazy='joined')


class User(db.Model):
    __tablename__ = 'users'

    id = Column(types.Integer, primary_key=True)
    username = Column(types.String, nullable=False, unique=True)
    password_hash = Column(types.String, nullable=False)

    boards = db.relationship("Board")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
